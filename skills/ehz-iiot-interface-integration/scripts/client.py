#!/usr/bin/env python3
"""极联平台接口管理集成动态 CLI 客户端（自动从 api_docs.md 生成）"""
import logging
import os
import sys
from requests.exceptions import ConnectTimeout, ReadTimeout, HTTPError, ConnectionError as ReqConnectionError

# 将 skill 根目录加入 import 路径
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _SKILL_ROOT)

# 自动加载 .env 文件（Windows / Linux / Mac 全平台兼容）
from dotenv import load_dotenv
load_dotenv(os.path.join(_SKILL_ROOT, ".env"))

import requests

from base.client import DynamicApiClient
from base.parser import ApiEndpoint
from api_parser import ApiDocsParser
from auth import EhzAuthProvider

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

API_URL = os.environ.get("API_URL", "https://jilian-sit.ehzcloud.com")

# 参数映射表（API param name -> CLI arg dest name，下划线自动转 hyphen）
PARAM_MAPPING = {
    "isCopy": "is-copy",
}

# CLI 别名映射（CLI 命令 -> 端点名）
CMD_ALIASES = {
    # 应用接入列表
    "app-list": "获取API管理应用接入列表",
    "get-app-list": "获取API管理应用接入列表",
    # 接口服务列表
    "app-interface-list": "根据标识符查询接口服务列表",
    "get-app-interface-list": "根据标识符查询接口服务列表",
    # 接口文档
    "get-interface-doc": "获取单个接口文档",
    "interface-doc": "获取单个接口文档",
    # 调用接口服务
    "debug-app-interface": "调用API管理接口服务",
    "call-app-interface": "调用API管理接口服务",
}


class EhzInterfaceIntegrationClient(DynamicApiClient):
    """极联平台接口管理集成动态客户端，支持两种 API 类型"""

    # /ESBREST/iiot/ 前缀使用 success/message/code/result 格式
    IIOT_PATH_PREFIX = "/ESBREST/iiot/"
    # /ESBREST/faas/ 前缀使用 errorCode/errorMsg/return 格式，请求需要包装 {apikey, request}
    FAAS_PATH_PREFIX = "/ESBREST/faas/"
    # /ESBREST/edge/ 前缀使用 errorCode/errorMsg/return 格式，但请求不需要包装
    EDGE_PATH_PREFIX = "/ESBREST/edge/"

    def _is_faas_api(self, path: str) -> bool:
        """判断是否为 faas 类型接口（需要 apikey 包装）"""
        return path.startswith(self.FAAS_PATH_PREFIX)

    def _is_edge_api(self, path: str) -> bool:
        """判断是否为 edge 类型接口（不需要包装，直接 JSON body）"""
        return path.startswith(self.EDGE_PATH_PREFIX)

    def _is_get_method(self, method: str) -> bool:
        """判断是否为 GET 请求"""
        return method.upper() == "GET"

    def _request(self, ep: ApiEndpoint, payload: dict) -> dict:
        url = f"{API_URL}{ep.path}"

        try:
            if self._is_faas_api(ep.path):
                # faas 类型：POST，参数包装在 {apikey, request} 中
                wrapped_payload = {
                    "apikey": "",
                    "request": payload,
                }
                resp = requests.post(url, headers=self.auth.headers(), json=wrapped_payload, timeout=10)
                resp.raise_for_status()
                return resp.json()
            elif self._is_edge_api(ep.path):
                # edge 类型：POST，直接 JSON body（不用 apikey 包装）
                resp = requests.post(url, headers=self.auth.headers(), json=payload, timeout=10)
                resp.raise_for_status()
                return resp.json()
            elif self._is_get_method(ep.method):
                # iiot GET 类型：参数放 query string
                resp = requests.get(url, headers=self.auth.headers(), params=payload, timeout=10)
                resp.raise_for_status()
                return resp.json()
            else:
                # iiot POST 类型：简单 JSON body
                resp = requests.post(url, headers=self.auth.headers(), json=payload, timeout=10)
                resp.raise_for_status()
                return resp.json()
        except ConnectTimeout:
            return self._error_response(408, "请求超时")
        except ReadTimeout:
            return self._error_response(408, "读取响应超时")
        except ReqConnectionError:
            return self._error_response(503, "无法连接到服务器")
        except HTTPError as e:
            status = e.response.status_code if e.response is not None else 500
            return self._error_response(status, f"HTTP错误: {status}")
        except ValueError:
            return self._error_response(502, "服务器响应非 JSON 格式")
        except Exception as e:
            return self._error_response(500, f"未知错误: {e}")

    def _error_response(self, code: int, msg: str) -> dict:
        """统一错误响应，同时兼容两种格式"""
        return {
            "success": False,
            "message": msg,
            "code": code,
            "errorCode": code,
            "errorMsg": msg,
            "return": None,
        }

    # 过滤掉空值参数，避免后台将空字符串转为错误
    def _build_payload(self, args, ep):
        payload = super()._build_payload(args, ep)
        return {k: v for k, v in payload.items() if v not in ("", None, [], {})}


def main():
    api_docs = os.path.join(_SKILL_ROOT, "references", "api_docs.md")

    client = EhzInterfaceIntegrationClient(
        parser_cls=ApiDocsParser,
        api_docs_path=api_docs,
        skill_name="ehz-iiot-interface-integration",
        auth_provider=EhzAuthProvider(),
        param_mapping=PARAM_MAPPING,
        aliases=CMD_ALIASES,
    )
    client.run()


if __name__ == "__main__":
    main()
