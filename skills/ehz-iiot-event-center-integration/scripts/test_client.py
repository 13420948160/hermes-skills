#!/usr/bin/env python3
"""极联平台事件中心集成 API 兼容性测试套件

测试策略：
- 每个接口原子化独立测试，互不影响
- 支持重试机制：同一用例最多 15 次重试，连续 15 次失败直接退出
- 生成详细测试报告，包含执行结果、通过率、失败率

API 类型：
- /ESBREST/iiot/ 前缀：success/message/code/result 格式
"""
import argparse
import json
import logging
import os
import sys
import time
import traceback
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional

# Windows 终端 UTF-8 输出兼容
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# 将 skill 根目录加入 import 路径
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _SKILL_ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(_SKILL_ROOT, ".env"))

import requests
from requests.exceptions import ConnectTimeout, ReadTimeout, ConnectionError as ReqConnectionError

# 本地导入（base/ 在 scripts/ 下，skill_root/scripts/ 加入 sys.path）
try:
    from base.parser import ApiEndpoint
    from api_parser import ApiDocsParser
    from auth import EhzAuthProvider
except ImportError:
    from scripts.base.parser import ApiEndpoint
    from scripts.api_parser import ApiDocsParser
    from scripts.auth import EhzAuthProvider

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

API_URL = os.environ.get("API_URL", "https://jilian-sit.ehzcloud.com")
IIOT_PATH_PREFIX = "/ESBREST/iiot/"
FAAS_PATH_PREFIX = "/ESBREST/faas/"
MAX_RETRIES = 15
RETRY_DELAY = 2  # 秒


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

@dataclass
class TestResult:
    """单个测试用例结果"""
    name: str
    endpoint_path: str
    method: str
    api_type: str = "iiot"
    status: str = "pending"  # pending / passed / failed / skipped
    attempt: int = 0
    elapsed_ms: int = 0
    payload: Optional[dict] = None
    response: Optional[dict] = None
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None


@dataclass
class TestReport:
    """测试报告"""
    started_at: str = ""
    finished_at: str = ""
    total_cases: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    pass_rate: float = 0.0
    fail_rate: float = 0.0
    total_elapsed_ms: int = 0
    results: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# 测试客户端（独立于 CLI client，直接测试）
# ---------------------------------------------------------------------------

class TestRunner:
    """事件中心集成 API 测试运行器"""

    def __init__(self, api_url: str = None, dry_run: bool = False):
        self.api_url = api_url or os.environ.get("API_URL", API_URL)
        self.dry_run = dry_run
        self.auth = EhzAuthProvider()
        self.report = TestReport()

    def _auth_headers(self) -> dict:
        """获取认证请求头"""
        return self.auth.headers()

    def _is_get_method(self, method: str) -> bool:
        return method.upper() == "GET"

    def _do_request(self, ep: ApiEndpoint, payload: dict) -> tuple[dict, int]:
        """执行单个请求，返回 (response, elapsed_ms)"""
        url = f"{self.api_url}{ep.path}"
        headers = self._auth_headers()
        start = time.time()

        try:
            if ep.api_type == "faas":
                # faas 类型：POST，参数包装在 {apikey, request} 中
                wrapped_payload = {"apikey": "", "request": payload}
                resp = requests.post(url, headers=headers, json=wrapped_payload, timeout=10)
            elif self._is_get_method(ep.method):
                resp = requests.get(url, headers=headers, params=payload, timeout=10)
            else:
                resp = requests.post(url, headers=headers, json=payload, timeout=10)

            resp.raise_for_status()
            elapsed_ms = int((time.time() - start) * 1000)
            return resp.json(), elapsed_ms

        except ConnectTimeout:
            return {"success": False, "code": 408, "message": "请求超时"}, int((time.time() - start) * 1000)
        except ReadTimeout:
            return {"success": False, "code": 408, "message": "读取响应超时"}, int((time.time() - start) * 1000)
        except ReqConnectionError as e:
            return {"success": False, "code": 503, "message": f"无法连接到服务器: {e}"}, int((time.time() - start) * 1000)
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else 500
            return {"success": False, "code": status, "message": f"HTTP错误: {status}"}, int((time.time() - start) * 1000)
        except Exception as e:
            return {"success": False, "code": 500, "message": str(e)}, int((time.time() - start) * 1000)

    def _validate_response(self, resp: dict, api_type: str) -> tuple[bool, str]:
        """验证响应格式是否正确，返回 (is_valid, error_message)"""
        if api_type == "faas":
            if "errorCode" not in resp:
                return False, f"faas 类型响应缺少 errorCode 字段，实际: {list(resp.keys())}"
            return True, ""
        else:
            # iiot 类型
            if "success" not in resp and "code" not in resp:
                return False, f"iiot 类型响应缺少必要字段 success/code，实际: {list(resp.keys())}"
            return True, ""

    def _extract_params(self, ep: ApiEndpoint) -> dict:
        """从请求示例或参数默认值构建测试 payload"""
        payload = {}

        # 优先使用 request_example
        if ep.request_example and isinstance(ep.request_example, dict):
            for k, v in ep.request_example.items():
                if v is not None:
                    payload[k] = v

        # faas 类型：处理 msgs/topic/type 必填参数
        if ep.api_type == "faas":
            for p in ep.parameters:
                if p.name == "msgs" and p.name not in payload:
                    payload[p.name] = {"name": "test", "value": 123}
                elif p.name == "topic" and p.name not in payload:
                    import uuid
                    payload[p.name] = f"TEST-TOPIC-{int(time.time())}-{uuid.uuid4().hex[:8]}"
                elif p.name == "type" and p.name not in payload:
                    payload[p.name] = "kafka"
        else:
            # iiot 类型：处理必填参数
            for p in ep.parameters:
                if p.name not in payload:
                    default = p.default.strip() if p.default else ""
                    if default:
                        if default.lower() in ("true", "false"):
                            payload[p.name] = default.lower() == "true"
                        elif default.isdigit():
                            payload[p.name] = int(default)
                        else:
                            payload[p.name] = default
                    elif p.required:
                        if p.name == "name":
                            import uuid
                            payload[p.name] = f"测试事件中心-{uuid.uuid4().hex[:8]}"
                        elif p.name == "type":
                            payload[p.name] = "cron"
                        elif p.name == "topic":
                            import uuid
                            payload[p.name] = f"TEST-TOPIC-{int(time.time())}-{uuid.uuid4().hex[:8]}"
                        elif p.name == "id":
                            if "EventDefine" in ep.path:
                                payload[p.name] = "2019323421428367361"
                            elif "eventAction" in ep.path:
                                payload[p.name] = "2031651500437225473"
                            else:
                                payload[p.name] = "2019323421428367361"
                        elif p.name == "ids":
                            payload[p.name] = "2031651500437225473"
                        elif p.name == "defineName":
                            payload[p.name] = "测试事件中心功能"
                        elif p.name == "defineTopic":
                            payload[p.name] = "TEST-MASTER-IOT-yhtest"
                        elif p.name == "actionStatus":
                            payload[p.name] = "1"
                        elif p.name == "actionType":
                            payload[p.name] = "http"
                        elif p.name == "actionName":
                            import uuid
                            payload[p.name] = f"测试动作-{uuid.uuid4().hex[:8]}"
                        elif p.name == "actionAlias":
                            import uuid
                            payload[p.name] = f"action-alias-{uuid.uuid4().hex[:8]}"

        # GET 请求不需要空 payload
        if self._is_get_method(ep.method) and not payload:
            payload = {}

        return payload

    def _run_single_test(self, ep: ApiEndpoint) -> TestResult:
        """执行单个测试用例，支持重试"""
        result = TestResult(
            name=ep.name,
            endpoint_path=ep.path,
            method=ep.method,
            api_type=ep.api_type,
        )

        payload = self._extract_params(ep)
        result.payload = payload
        logger.info("[%s] 开始测试: %s (%s) payload=%s", ep.method, ep.name, ep.api_type, payload)

        consecutive_failures = 0

        for attempt in range(1, MAX_RETRIES + 1):
            result.attempt = attempt
            try:
                resp, elapsed_ms = self._do_request(ep, payload)
                result.elapsed_ms = elapsed_ms
                result.response = resp

                # 验证响应格式
                is_valid, val_err = self._validate_response(resp, ep.api_type)

                if is_valid:
                    # 根据 API 类型检查成功标志
                    if ep.api_type == "faas":
                        passed = resp.get("errorCode") == 0
                        if not passed:
                            is_valid = False
                            val_err = f"faas 接口调用失败: errorCode={resp.get('errorCode')}, errorMsg={resp.get('errorMsg')}"
                    else:
                        passed = resp.get("success") is True or resp.get("code") == 200
                        if not passed:
                            is_valid = False
                            val_err = f"iiot 接口调用失败: success={resp.get('success')}, code={resp.get('code')}, message={resp.get('message')}"

                if is_valid:
                    result.status = "passed"
                    logger.info("[PASS] %s 成功 (第 %d 次尝试, %dms)", ep.name, attempt, elapsed_ms)
                    return result
                else:
                    result.error_message = val_err
                    consecutive_failures += 1
                    logger.warning("[%s] %s 失败 (第 %d/%d 次): %s", ep.api_type.upper(), ep.name, attempt, MAX_RETRIES, val_err)

            except Exception as e:
                result.elapsed_ms = 0
                result.error_message = str(e)
                result.stack_trace = traceback.format_exc()
                consecutive_failures += 1
                logger.warning("[FAIL] %s 异常 (第 %d/%d 次): %s", ep.name, attempt, MAX_RETRIES, e)

            # 超过连续失败次数限制，退出
            if consecutive_failures >= MAX_RETRIES:
                result.status = "failed"
                logger.error("[EXIT] %s 连续 %d 次失败，退出测试", ep.name, MAX_RETRIES)
                return result

            # 等待后重试
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

        # 所有重试用尽
        result.status = "failed"
        return result

    def run_all(self, endpoints: list[ApiEndpoint], selected_names: list[str] = None) -> TestReport:
        """运行所有或指定测试用例"""
        self.report.started_at = datetime.now().isoformat()
        self.report.total_cases = len(endpoints)

        targets = [ep for ep in endpoints
                   if selected_names is None or ep.name in selected_names
                   or any(sn in ep.name for sn in selected_names)]

        if not targets:
            logger.warning("没有匹配到任何测试用例 selected_names=%s", selected_names)
            self.report.skipped = len(endpoints)
            return self.report

        for ep in targets:
            result = self._run_single_test(ep)
            self.report.results.append(asdict(result))
            self.report.total_elapsed_ms += result.elapsed_ms

            if result.status == "passed":
                self.report.passed += 1
            elif result.status == "failed":
                self.report.failed += 1
            else:
                self.report.skipped += 1

        self.report.finished_at = datetime.now().isoformat()

        if self.report.total_cases > 0:
            total_done = self.report.passed + self.report.failed
            if total_done > 0:
                self.report.pass_rate = round(self.report.passed / total_done * 100, 2)
                self.report.fail_rate = round(self.report.failed / total_done * 100, 2)

        return self.report

    def print_report(self, report: TestReport, output_file: str = None):
        """打印并可选保存测试报告"""
        lines = []
        sep = "=" * 80
        lines.append(sep)
        lines.append("极联平台事件中心集成 API 兼容性测试报告")
        lines.append(sep)
        lines.append(f"测试时间  : {report.started_at} ~ {report.finished_at}")
        lines.append(f"总用例数  : {report.total_cases}")
        lines.append(f"通过      : {report.passed} ({report.pass_rate}%)")
        lines.append(f"失败      : {report.failed} ({report.fail_rate}%)")
        lines.append(f"跳过      : {report.skipped}")
        lines.append(f"总耗时    : {report.total_elapsed_ms}ms")
        lines.append(sep)

        for r in report.results:
            status_icon = {"passed": "[PASS]", "failed": "[FAIL]", "skipped": "[-]", "pending": "[?]"}.get(r["status"], "[?]")
            lines.append(f"\n[{status_icon}] {r['status'].upper():7s} | {r['name']}")
            lines.append(f"    接口  : {r['method']} {r['endpoint_path']} ({r['api_type']})")
            if r.get("payload"):
                payload_str = json.dumps(r["payload"], ensure_ascii=False)
                if len(payload_str) > 200:
                    payload_str = payload_str[:200] + "...(已截断)"
                lines.append(f"    请求  : {payload_str}")
            lines.append(f"    尝试  : {r['attempt']} 次")
            lines.append(f"    耗时  : {r['elapsed_ms']}ms")

            if r["status"] == "failed":
                lines.append(f"    错误  : {r['error_message']}")
                if r.get("stack_trace"):
                    lines.append(f"    堆栈  :\n{r['stack_trace']}")

            if r["response"]:
                # 截断过长的响应
                resp_str = json.dumps(r["response"], ensure_ascii=False, indent=2)
                if len(resp_str) > 500:
                    resp_str = resp_str[:500] + "\n    ... (已截断)"
                lines.append(f"    响应  :\n    {resp_str.replace(chr(10), chr(10) + '    ')}")

        lines.append(sep)

        output = "\n".join(lines)
        try:
            print(output)
        except UnicodeEncodeError:
            print(output.encode("ascii", "replace").decode("ascii"))

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output)
            # 同时保存 JSON 格式报告
            json_file = output_file.rsplit(".", 1)[0] + ".json"
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(asdict(report), f, ensure_ascii=False, indent=2)
            logger.info("报告已保存: %s", output_file)
            logger.info("JSON报告已保存: %s", json_file)

        # 如果有任何失败，输出退出提示
        if report.failed > 0:
            try:
                print(f"\n存在 {report.failed} 个测试用例失败，请检查日志。")
            except UnicodeEncodeError:
                print(f"\n{report.failed} test(s) failed, please check logs.")

    def verify_endpoints_loaded(self) -> list[ApiEndpoint]:
        """验证端点解析是否正确"""
        api_docs = os.path.join(_SKILL_ROOT, "references", "api_docs.md")
        parser = ApiDocsParser()
        endpoints = parser.parse_file(api_docs)
        logger.info("解析到 %d 个端点:", len(endpoints))
        for ep in endpoints:
            logger.info("  [%d] %s %s (%s)", ep.index, ep.method, ep.path, ep.api_type)
        return endpoints


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="极联平台事件中心集成 API 兼容性测试")
    parser.add_argument("--url", default=API_URL, help=f"API 地址 (默认: {API_URL})")
    parser.add_argument("--dry-run", action="store_true", help="仅解析接口，不发送请求")
    parser.add_argument("--output", "-o", metavar="FILE", help="保存报告到文件")
    parser.add_argument("--select", "-s", metavar="NAME", nargs="+",
                        help="仅运行指定名称的测试用例（支持模糊匹配）")
    parser.add_argument("--list", action="store_true", help="列出所有测试用例")
    args = parser.parse_args()

    runner = TestRunner(api_url=args.url, dry_run=args.dry_run)

    # 先解析接口清单
    endpoints = runner.verify_endpoints_loaded()

    if args.list:
        print("\n可用测试用例:")
        for ep in endpoints:
            print(f"  [{ep.index}] {ep.name} ({ep.api_type}) - {ep.method} {ep.path}")
        return

    if args.dry_run:
        print("dry_run 模式，仅解析接口，不执行测试")
        return

    # 运行测试
    report = runner.run_all(endpoints, selected_names=args.select)

    # 输出报告
    runner.print_report(report, output_file=args.output)

    # 退出码：0=全部通过，1=有失败
    sys.exit(0 if report.failed == 0 else 1)


if __name__ == "__main__":
    main()
