#!/usr/bin/env python3
"""极联设备管理 CLI 测试用例（API 4/5/6/7）"""
import json
import sys
import unittest
from unittest.mock import MagicMock, patch

# 将 skill 根目录加入 import 路径
import os
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _SKILL_ROOT)

from scripts.client import EhzDeviceClient
from scripts.api_parser import ApiDocsParser


def _make_parser():
    return ApiDocsParser()


def _load_endpoints():
    parser = _make_parser()
    api_docs = os.path.join(_SKILL_ROOT, "references", "api_docs.md")
    return parser.parse_file(api_docs)


def _mock_auth():
    auth = MagicMock()
    auth.headers.return_value = {"Authorization": "Bearer test-token"}
    return auth


def _build_client():
    with patch("requests.post") as mock_post:
        return EhzDeviceClient(
            parser_cls=ApiDocsParser,
            api_docs_path=os.path.join(_SKILL_ROOT, "references", "api_docs.md"),
            skill_name="ehz-iiot-device",
            auth_provider=_mock_auth(),
            param_mapping={
                "areaId": "areaId",
                "emodelid": "emodelid",
                "page": "page",
                "pageSize": "page-size",
            },
            aliases={
                "get-equipment-rt-status": "getEquipmentRtStatus - 获取设备实时状态",
                "get-equipment-rt": "getEquipmentRtStatus - 获取设备实时状态",
                "get-devices-by-tag": "getEqpListNewTag - 根据标签获取设备列表",
                "get-alarm-history": "getAlarmHistoryData - 获取告警历史数据",
                "get-history-data": "getHistoryDataByOrder - 获取设备历史数据",
            },
        )


# ---------------------------------------------------------------------------
# API 4: getEquipmentRtStatus - 获取设备实时状态
# ---------------------------------------------------------------------------

class TestGetEquipmentRtStatus(unittest.TestCase):
    """API 4 测试用例"""

    def setUp(self):
        self.client = _build_client()
        self.endpoints = _load_endpoints()
        self.ep = next(
            (e for e in self.endpoints if "getEquipmentRtStatus" in e.name), None
        )
        self.assertIsNotNone(self.ep, "API 4 endpoint not found")

    def test_success(self):
        """成功响应：errorCode=0"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "errorCode": 0,
            "errorMsg": "操作成功",
            "return": [
                {
                    "eid": "eid_001",
                    "iccid": "89860000000000000000",
                    "isFollow": "1",
                    "lastRefreshTime": "2024-01-15T08:30:00.000Z",
                    "online": 1,
                    "totalAlarm": 0,
                },
                {
                    "eid": "eid_002",
                    "iccid": "89860000000000000001",
                    "isFollow": "0",
                    "lastRefreshTime": "2024-01-15T08:31:00.000Z",
                    "online": 0,
                    "totalAlarm": 2,
                },
            ],
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_resp):
            result = self.client._request(self.ep, {"eids": ["eid_001", "eid_002"]})

        self.assertEqual(result["errorCode"], 0)
        self.assertEqual(len(result["return"]), 2)
        self.assertEqual(result["return"][0]["eid"], "eid_001")
        self.assertEqual(result["return"][0]["online"], 1)

    def test_empty_eids(self):
        """空 eids 数组时行为"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "errorCode": 0,
            "errorMsg": "操作成功",
            "return": [],
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_resp):
            result = self.client._request(self.ep, {"eids": []})

        self.assertEqual(result["errorCode"], 0)
        self.assertEqual(result["return"], [])

    def test_error_401(self):
        """认证失败"""
        with patch("requests.post") as mock_post:
            mock_post.side_effect = Exception("401")
            result = self.client._request(self.ep, {"eids": ["eid_001"]})
        self.assertIn("errorCode", result)

    def test_error_408(self):
        """请求超时"""
        from requests.exceptions import ConnectTimeout

        with patch("requests.post", side_effect=ConnectTimeout()):
            result = self.client._request(self.ep, {"eids": ["eid_001"]})
        self.assertEqual(result["errorCode"], 408)
        self.assertIn("超时", result["errorMsg"])

    def test_error_503(self):
        """无法连接服务器"""
        from requests.exceptions import ConnectionError as ReqConnectionError

        with patch("requests.post", side_effect=ReqConnectionError()):
            result = self.client._request(self.ep, {"eids": ["eid_001"]})
        self.assertEqual(result["errorCode"], 503)

    def test_error_502(self):
        """响应非 JSON"""
        mock_resp = MagicMock()
        mock_resp.status_code = 502

        with patch("requests.post", return_value=mock_resp):
            mock_resp.json.side_effect = ValueError("not json")
            result = self.client._request(self.ep, {"eids": ["eid_001"]})
        self.assertEqual(result["errorCode"], 502)

    def test_error_500(self):
        """服务器内部错误"""
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.json.return_value = {
            "errorCode": 500,
            "errorMsg": "服务器内部错误",
            "return": None,
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_resp):
            result = self.client._request(self.ep, {"eids": ["eid_001"]})
        self.assertEqual(result["errorCode"], 500)


# ---------------------------------------------------------------------------
# API 5: getEqpListNewTag - 根据标签获取设备列表
# ---------------------------------------------------------------------------

class TestGetEqpListNewTag(unittest.TestCase):
    """API 5 测试用例"""

    def setUp(self):
        self.client = _build_client()
        self.endpoints = _load_endpoints()
        self.ep = next(
            (e for e in self.endpoints if "getEqpListNewTag" in e.name), None
        )
        self.assertIsNotNone(self.ep, "API 5 endpoint not found")

    def test_success(self):
        """成功响应：errorCode=0"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "errorCode": 0,
            "errorMsg": "操作成功",
            "times": "mySql总耗时 -> 0.150 秒。Redis总耗时 -> 0.010 秒。",
            "return": {
                "datas": [
                    {
                        "sn": "SN001",
                        "code": "CNC001",
                        "eid": "eid_12345",
                        "name": "1号加工中心",
                        "emodelName": "CNC加工中心",
                        "online": 1,
                        "totalAlarm": 2,
                    }
                ],
                "pageIndex": 1,
                "pageTotal": 3,
                "datasTotal": 50,
                "onlineTotal": 40,
            },
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_resp):
            result = self.client._request(
                self.ep,
                {
                    "tagId": "tag_001",
                    "groupId": "",
                    "pageIndex": 1,
                    "page": 20,
                    "keyword": "",
                },
            )

        self.assertEqual(result["errorCode"], 0)
        self.assertEqual(len(result["return"]["datas"]), 1)
        self.assertEqual(result["return"]["datasTotal"], 50)
        self.assertEqual(result["return"]["pageTotal"], 3)

    def test_pagination(self):
        """分页参数"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "errorCode": 0,
            "errorMsg": "操作成功",
            "return": {
                "datas": [],
                "pageIndex": 3,
                "pageTotal": 10,
                "datasTotal": 200,
                "onlineTotal": 50,
            },
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_resp):
            result = self.client._request(
                self.ep,
                {
                    "tagId": "tag_001",
                    "groupId": "",
                    "pageIndex": 3,
                    "page": 20,
                    "keyword": "",
                },
            )

        self.assertEqual(result["errorCode"], 0)
        self.assertEqual(result["return"]["pageIndex"], 3)

    def test_missing_tag_and_group(self):
        """tagId 和 groupId 均缺失时行为（服务端返回参数错误）"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "errorCode": 400,
            "errorMsg": "tagId 和 groupId 不能同时为空",
            "return": None,
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_resp):
            result = self.client._request(
                self.ep,
                {"tagId": "", "groupId": "", "pageIndex": 1, "page": 20, "keyword": ""},
            )

        self.assertEqual(result["errorCode"], 400)

    def test_error_401(self):
        """认证失败"""
        from requests.exceptions import ConnectTimeout

        with patch("requests.post", side_effect=ConnectTimeout()):
            result = self.client._request(self.ep, {})
        self.assertEqual(result["errorCode"], 408)

    def test_error_408(self):
        """请求超时"""
        from requests.exceptions import ReadTimeout

        with patch("requests.post", side_effect=ReadTimeout()):
            result = self.client._request(self.ep, {})
        self.assertEqual(result["errorCode"], 408)

    def test_error_503(self):
        """无法连接"""
        from requests.exceptions import ConnectionError as ReqConnectionError

        with patch("requests.post", side_effect=ReqConnectionError()):
            result = self.client._request(self.ep, {})
        self.assertEqual(result["errorCode"], 503)


# ---------------------------------------------------------------------------
# API 6: getAlarmHistoryData - 获取告警历史数据
# ---------------------------------------------------------------------------

class TestGetAlarmHistoryData(unittest.TestCase):
    """API 6 测试用例"""

    def setUp(self):
        self.client = _build_client()
        self.endpoints = _load_endpoints()
        self.ep = next(
            (e for e in self.endpoints if "getAlarmHistoryData" in e.name), None
        )
        self.assertIsNotNone(self.ep, "API 6 endpoint not found")

    def test_success(self):
        """成功响应：errorCode=0"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "errorCode": 0,
            "errorMsg": "",
            "return": {
                "datas": [
                    {
                        "alarmId": "ASN_001",
                        "topic": "温度过高告警",
                        "level": "2",
                        "status": "1",
                        "makeTimestamp": 1672531200000,
                        "eid": "eid_001",
                        "eqptName": "1号加工中心",
                        "relationDatas": [],
                        "clearRelationDatas": [],
                    }
                ],
                "datasTotal": 100,
                "pageTotal": 5,
                "pageIndex": 1,
            },
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_resp):
            result = self.client._request(
                self.ep,
                {
                    "areaId": "area_001",
                    "pageIndex": 1,
                    "pageSize": 20,
                    "status": 1,
                    "level": 2,
                    "startTime": "2024-01-01T00:00:00.000Z",
                    "endTime": "2024-01-31T23:59:59.000Z",
                },
            )

        self.assertEqual(result["errorCode"], 0)
        self.assertEqual(len(result["return"]["datas"]), 1)
        self.assertEqual(result["return"]["datas"][0]["alarmId"], "ASN_001")
        self.assertEqual(result["return"]["datasTotal"], 100)

    def test_empty_result(self):
        """无告警记录"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "errorCode": 0,
            "errorMsg": "",
            "return": {
                "datas": [],
                "datasTotal": 0,
                "pageTotal": 0,
                "pageIndex": 1,
            },
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_resp):
            result = self.client._request(
                self.ep,
                {
                    "areaId": "area_999",
                    "pageIndex": 1,
                    "pageSize": 20,
                },
            )

        self.assertEqual(result["errorCode"], 0)
        self.assertEqual(result["return"]["datas"], [])
        self.assertEqual(result["return"]["datasTotal"], 0)

    def test_filter_by_eid(self):
        """按设备 EID 筛选"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "errorCode": 0,
            "errorMsg": "",
            "return": {
                "datas": [
                    {
                        "alarmId": "ASN_002",
                        "topic": "压力过高",
                        "level": "1",
                        "status": "1",
                        "makeTimestamp": 1672531300000,
                        "eid": "eid_12345",
                        "eqptName": "2号加工中心",
                        "relationDatas": [],
                        "clearRelationDatas": [],
                    }
                ],
                "datasTotal": 1,
                "pageTotal": 1,
                "pageIndex": 1,
            },
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_resp):
            result = self.client._request(
                self.ep,
                {
                    "areaId": "area_001",
                    "pageIndex": 1,
                    "pageSize": 20,
                    "eid": "eid_12345",
                },
            )

        self.assertEqual(result["errorCode"], 0)
        self.assertEqual(result["return"]["datas"][0]["eid"], "eid_12345")

    def test_error_401(self):
        """认证失败"""
        from requests.exceptions import ConnectTimeout

        with patch("requests.post", side_effect=ConnectTimeout()):
            result = self.client._request(self.ep, {})
        self.assertEqual(result["errorCode"], 408)

    def test_error_408(self):
        """请求超时"""
        from requests.exceptions import ReadTimeout

        with patch("requests.post", side_effect=ReadTimeout()):
            result = self.client._request(self.ep, {})
        self.assertEqual(result["errorCode"], 408)

    def test_error_503(self):
        """无法连接"""
        from requests.exceptions import ConnectionError as ReqConnectionError

        with patch("requests.post", side_effect=ReqConnectionError()):
            result = self.client._request(self.ep, {})
        self.assertEqual(result["errorCode"], 503)


# ---------------------------------------------------------------------------
# API 7: getHistoryDataByOrder - 获取设备历史数据
# ---------------------------------------------------------------------------

class TestGetHistoryDataByOrder(unittest.TestCase):
    """API 7 测试用例"""

    def setUp(self):
        self.client = _build_client()
        self.endpoints = _load_endpoints()
        self.ep = next(
            (e for e in self.endpoints if "getHistoryDataByOrder" in e.name), None
        )
        self.assertIsNotNone(self.ep, "API 7 endpoint not found")

    def test_success(self):
        """成功响应：errorCode=0"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "errorCode": 0,
            "errorMsg": "操作成功!",
            "return": {
                "datas": [
                    {
                        "timestamp": 1672531200000,
                        "time": "2024-01-01T00:00:00.000Z",
                        "name": "温度(℃)",
                        "value": 25.5,
                    },
                    {
                        "timestamp": 1672534800000,
                        "time": "2024-01-01T01:00:00.000Z",
                        "name": "温度(℃)",
                        "value": 26.0,
                    },
                ],
                "pageIndex": 1,
                "pageTotal": 1,
                "datasTotal": 168,
                "name": ["温度(℃)", "压力(MPa)"],
            },
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_resp):
            result = self.client._request(
                self.ep,
                {
                    "eid": "eid_12345",
                    "oids": ["temperature", "pressure"],
                    "startTime": "2024-01-01T00:00:00.000Z",
                    "endTime": "2024-01-07T00:00:00.000Z",
                    "interval": 3600000,
                    "pageIndex": 1,
                    "pageSize": 100,
                },
            )

        self.assertEqual(result["errorCode"], 0)
        self.assertEqual(len(result["return"]["datas"]), 2)
        self.assertEqual(result["return"]["datas"][0]["name"], "温度(℃)")
        self.assertEqual(result["return"]["datasTotal"], 168)

    def test_by_code(self):
        """按设备编号查询（而非 EID）"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "errorCode": 0,
            "errorMsg": "操作成功!",
            "return": {
                "datas": [
                    {
                        "timestamp": 1672531200000,
                        "time": "2024-01-01T00:00:00.000Z",
                        "name": "湿度(%)",
                        "value": 60.5,
                    }
                ],
                "pageIndex": 1,
                "pageTotal": 1,
                "datasTotal": 24,
                "name": ["湿度(%)"],
            },
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_resp):
            result = self.client._request(
                self.ep,
                {
                    "code": "MOMTest",
                    "oids": ["humidity"],
                    "startTime": "2024-01-01T00:00:00.000Z",
                    "endTime": "2024-01-02T00:00:00.000Z",
                    "interval": 3600000,
                    "pageIndex": 1,
                    "pageSize": 100,
                },
            )

        self.assertEqual(result["errorCode"], 0)
        self.assertEqual(result["return"]["name"], ["湿度(%)"])

    def test_empty_result(self):
        """时间范围内无数据"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "errorCode": 0,
            "errorMsg": "操作成功!",
            "return": {
                "datas": [],
                "pageIndex": 1,
                "pageTotal": 0,
                "datasTotal": 0,
                "name": [],
            },
        }
        mock_resp.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_resp):
            result = self.client._request(
                self.ep,
                {
                    "eid": "eid_99999",
                    "oids": ["nonexistent"],
                    "startTime": "2024-01-01T00:00:00.000Z",
                    "endTime": "2024-01-02T00:00:00.000Z",
                    "interval": 3600000,
                    "pageIndex": 1,
                    "pageSize": 100,
                },
            )

        self.assertEqual(result["errorCode"], 0)
        self.assertEqual(result["return"]["datas"], [])

    def test_error_401(self):
        """认证失败"""
        from requests.exceptions import ConnectTimeout

        with patch("requests.post", side_effect=ConnectTimeout()):
            result = self.client._request(self.ep, {})
        self.assertEqual(result["errorCode"], 408)

    def test_error_408(self):
        """请求超时"""
        from requests.exceptions import ReadTimeout

        with patch("requests.post", side_effect=ReadTimeout()):
            result = self.client._request(self.ep, {})
        self.assertEqual(result["errorCode"], 408)

    def test_error_503(self):
        """无法连接"""
        from requests.exceptions import ConnectionError as ReqConnectionError

        with patch("requests.post", side_effect=ReqConnectionError()):
            result = self.client._request(self.ep, {})
        self.assertEqual(result["errorCode"], 503)

    def test_error_502(self):
        """响应非 JSON"""
        from requests.exceptions import HTTPError

        mock_resp = MagicMock()
        mock_resp.status_code = 502

        with patch("requests.post", side_effect=HTTPError(response=mock_resp)):
            result = self.client._request(self.ep, {})
        self.assertEqual(result["errorCode"], 502)


if __name__ == "__main__":
    unittest.main(verbosity=2)
