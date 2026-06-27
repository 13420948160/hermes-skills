#!/usr/bin/env python3
"""极联平台设备管理动态 CLI 客户端（自动从 api_docs.md 生成）"""
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

API_URL = os.environ.get("API_URL", "your_api_url_here")

# 参数映射表（API param name -> CLI arg dest name）
PARAM_MAPPING = {
    "areaId": "areaId",
    "emodelid": "emodelid",
    "page": "page",
    "pageSize": "page-size",
}

# CLI 别名映射（CLI 命令 -> 端点名）
CMD_ALIASES = {
    "get-devices": "获取设备列表",
    "list-devices": "获取设备列表",
    "get-real-time-data": "获取设备实时数据",
    "set-data": "设备反控（写入数据）",
    "get-realtime": "获取设备实时数据",
    "get-equipment-rt-status": "getEquipmentRtStatus - 获取设备实时状态",
    "get-equipment-rt": "getEquipmentRtStatus - 获取设备实时状态",
    "get-devices-by-tag": "getEqpListNewTag - 根据标签获取设备列表",
    "get-alarm-history": "getAlarmHistoryData - 获取告警历史数据",
    "get-history-data": "getHistoryDataByOrder - 获取设备历史数据",
}


class EhzDeviceClient(DynamicApiClient):
    """极联平台设备管理动态客户端"""

    def _request(self, ep: ApiEndpoint, payload: dict) -> dict:
        url = f"{API_URL}{ep.path}"
        try:
            resp = requests.post(url, headers=self.auth.headers(), json=payload, timeout=10)
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
    api_docs = os.path.join(_SKILL_ROOT, "references", "api_docs.md")

    client = EhzDeviceClient(
        parser_cls=ApiDocsParser,
        api_docs_path=api_docs,
        skill_name="ehz-iiot-device",
        auth_provider=EhzAuthProvider(),
        param_mapping=PARAM_MAPPING,
        aliases=CMD_ALIASES,
    )
    client.run()


if __name__ == "__main__":
    main()
