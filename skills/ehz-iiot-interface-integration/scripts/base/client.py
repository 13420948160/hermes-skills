"""动态 API CLI 客户端基类"""
import argparse
import json
import logging
import re
import sys
from abc import abstractmethod
from typing import Type

from base.parser import BaseMarkdownParser, ApiEndpoint, ApiParam

logger = logging.getLogger(__name__)


class DynamicApiClient:
    def __init__(
        self,
        parser_cls: Type[BaseMarkdownParser],
        api_docs_path: str,
        skill_name: str,
        auth_provider,
        param_mapping: dict = None,
        aliases: dict = None,
    ):
        self.parser = parser_cls()
        self.endpoints = self.parser.parse_file(api_docs_path)
        self.auth = auth_provider
        self.skill_name = skill_name
        self.param_mapping = param_mapping or {}
        self.aliases = aliases or {}  # {cli_cmd: endpoint_name}
        self.argparser = argparse.ArgumentParser(description=skill_name)
        self.subparsers = self.argparser.add_subparsers(dest="command", help="可用命令")
        # 将 skill_name 注入 auth provider（供日志等使用）
        if hasattr(self.auth, "skill_name"):
            self.auth.skill_name = skill_name
        self._build_argparser()

    def _to_cmd_name(self, name: str) -> str:
        """中文名称转 CLI 命令名：'获取设备列表' -> 'get-device-list'"""
        name = re.sub(r"^[\d\.]+\s*", "", name)
        return re.sub(r"[\W_]+", "-", name).lower()

    def _to_cli_param(self, name: str) -> str:
        """API 参数名转 CLI 参数名：table_id -> table-id, pageSize -> page-size"""
        # 先过滤掉 [] 和 . 等特殊字符（如 inParam[].code -> inParamcode）
        mapped = self.param_mapping.get(name, name)
        s1 = re.sub(r"[\[\]\.]+", "", mapped)
        s2 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", s1)
        s3 = re.sub("([a-z0-9])([A-Z])", r"\1-\2", s2).lower()
        return s3.replace("_", "-")

    def _create_subparser(self, ep: ApiEndpoint):
        cmd = self._to_cmd_name(ep.name)
        # 收集该端点的 CLI 别名（通过端点名或 cmd 名匹配）
        aliases = [
            a
            for a, n in self.aliases.items()
            if n == ep.name or self._to_cmd_name(n) == cmd
        ]
        sub = self.subparsers.add_parser(cmd, help=ep.description, aliases=aliases)

        for p in ep.parameters:
            cli = self._to_cli_param(p.name)
            default = self._parse_default(p.default)
            if default is None:
                default = ""
            sub.add_argument(
                f"--{cli}",
                default=default,
                help=f"[{p.param_type}] {p.description}",
                dest=p.name,
            )

    def _parse_default(self, s: str):
        if s in ("", "空", "无", None):
            return None
        if s.lower() == "true":
            return True
        if s.lower() == "false":
            return False
        if s.isdigit():
            return int(s)
        try:
            return float(s)
        except (ValueError, TypeError):
            return s

    def _build_argparser(self):
        for ep in self.endpoints:
            self._create_subparser(ep)

    def _deduplicate_params_by_cli_name(self, params: list) -> list:
        """当多个 API 参数映射到同一 CLI 参数名时，只保留第一个（避免 argparse dest 冲突）"""
        seen: dict[str, bool] = {}
        result = []
        for p in params:
            cli_name = self._to_cli_param(p.name)
            if cli_name not in seen:
                seen[cli_name] = True
                result.append(p)
        return result

    @abstractmethod
    def _request(self, ep: ApiEndpoint, payload: dict) -> dict:
        """子类实现：发送请求"""
        pass

    def _build_cmd_map(self) -> dict[str, ApiEndpoint]:
        """构建命令名到端点的映射（含别名）"""
        cmd_map: dict[str, ApiEndpoint] = {}
        for ep in self.endpoints:
            cmd_map[self._to_cmd_name(ep.name)] = ep
        for alias, ep_ref in self.aliases.items():
            for ep in self.endpoints:
                if ep.name == ep_ref or self._to_cmd_name(ep.name) == self._to_cmd_name(ep_ref):
                    cmd_map[alias] = ep
                    break
        return cmd_map

    def _resolve_endpoint(self, args: argparse.Namespace) -> ApiEndpoint | None:
        """根据命令行参数解析目标端点"""
        cmd_map = self._build_cmd_map()
        return cmd_map.get(args.command)

    def _infer_param_type(self, p: ApiParam) -> type | None:
        """从 ApiParam.param_type 字符串推断 Python 类型"""
        t = p.param_type.lower()
        if "int" in t:
            return int
        if "float" in t or "double" in t or "number" in t:
            return float
        if "bool" in t:
            return bool
        return None

    def _get_param_info(self, api_name: str, ep: ApiEndpoint) -> tuple[ApiParam | None, type | None]:
        """根据参数名从端点中查找参数定义及其推断类型"""
        for p in ep.parameters:
            if p.name == api_name:
                return p, self._infer_param_type(p)
        return None, None

    def _coerce_value(self, raw_val, api_name: str, ep: ApiEndpoint, parsed_defaults: dict) -> any:
        """将用户输入值转换为正确的 Python 类型"""
        param, type_hint = self._get_param_info(api_name, ep)
        if param and "array" in param.param_type.lower() and isinstance(raw_val, str):
            return [v.strip() for v in raw_val.split(",") if v.strip()]

        if api_name in parsed_defaults:
            default_val = parsed_defaults[api_name]
            if isinstance(default_val, bool):
                return str(raw_val).lower() in ("true", "1", "yes")
            if isinstance(default_val, int):
                return int(raw_val)
            if isinstance(default_val, float):
                return float(raw_val)
            return raw_val

        if type_hint == int:
            return int(raw_val)
        if type_hint == float:
            return float(raw_val)
        if type_hint == bool:
            return str(raw_val).lower() in ("true", "1", "yes")
        return raw_val

    def _build_payload(self, args: argparse.Namespace, ep: ApiEndpoint) -> dict:
        """以 API 定义的参数为骨架，从 CLI args 构建请求 payload"""
        reverse_map = {v: k for k, v in self.param_mapping.items()}
        raw = {k: v for k, v in vars(args).items() if k not in ("command",)}

        parsed_defaults = {}
        for p in ep.parameters:
            if p.default not in ("", "空", "无", None):
                parsed_defaults[p.name] = self._parse_default(p.default)

        payload = {}
        for p in ep.parameters:
            api_name = p.name
            cli_dest = reverse_map.get(api_name, api_name)
            raw_val = raw.get(cli_dest)

            if raw_val is not None and raw_val != "":
                payload[api_name] = self._coerce_value(raw_val, api_name, ep, parsed_defaults)
            elif api_name in parsed_defaults:
                payload[api_name] = parsed_defaults[api_name]
            elif raw_val == "":
                payload[api_name] = ""

        return payload

    def run(self):
        args = self.argparser.parse_args()
        if not args.command:
            self.argparser.print_help()
            sys.exit(0)

        ep = self._resolve_endpoint(args)
        if not ep:
            print(json.dumps({"errorCode": 404, "errorMsg": f"命令未找到: {args.command}"}, ensure_ascii=False, indent=2))
            sys.exit(1)

        logger.debug("调用端点: %s, payload: %s", ep.name, args)
        payload = self._build_payload(args, ep)
        result = self._request(ep, payload)
        print(json.dumps(result, ensure_ascii=False, indent=2))
