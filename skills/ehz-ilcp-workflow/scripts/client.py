#!/usr/bin/env python3
"""ILCP 审批流动态 CLI 客户端（自动从 api_docs.md 生成）"""
import logging
import os
import sys
from requests.exceptions import ConnectTimeout, ReadTimeout, HTTPError, ConnectionError as ReqConnectionError

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

import requests

from base.client import DynamicApiClient
from base.parser import ApiEndpoint
from api_parser import IlcpApiDocsParser
from auth import IlcpAuthProvider

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

API_URL = os.environ.get("API_URL", "your_api_url_here")

PARAM_MAPPING = {}

CMD_ALIASES = {
    "initiate-flow": "发起审批流",
    "get-flow-state": "获取审批流实例状态",
    "repeal-flow": "撤销审批流",
    "get-finish-record": "获取审批流完成记录",
}


class IlcpWorkflowClient(DynamicApiClient):
    """ILCP 审批流动态客户端"""

    def _request(self, ep: ApiEndpoint, payload: dict) -> dict:
        url = f"{API_URL}{ep.path}"
        try:
            resp = requests.post(url, headers=self.auth.headers(), json=payload, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except ConnectTimeout:
            return {"errorCode": 408, "errorMsg": "请求超时", "return": None}
        except ReadTimeout:
            return {"errorCode": 408, "errorMsg": "读取响应超时", "return": None}
        except ReqConnectionError:
            return {"errorCode": 503, "errorMsg": "无法连接到服务器", "return": None}
        except HTTPError as e:
            status = e.response.status_code if e.response is not None else 500
            return {"errorCode": status, "errorMsg": f"HTTP错误: {status}", "return": None}
        except ValueError:
            return {"errorCode": 502, "errorMsg": "服务器响应非 JSON 格式", "return": None}
        except Exception as e:
            return {"errorCode": 500, "errorMsg": f"未知错误: {e}", "return": None}


def main():
    api_docs = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references", "api_docs.md")

    client = IlcpWorkflowClient(
        parser_cls=IlcpApiDocsParser,
        api_docs_path=api_docs,
        skill_name="ehz-ilcp-workflow",
        auth_provider=IlcpAuthProvider(),
        param_mapping=PARAM_MAPPING,
        aliases=CMD_ALIASES,
    )
    client.run()


if __name__ == "__main__":
    main()
