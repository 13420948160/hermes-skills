"""IlcpWorkflowClient 测试 - 基于 api_docs.md"""
import pytest
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client import IlcpWorkflowClient, IlcpAuthProvider
from api_parser import IlcpApiDocsParser

API_DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "references", "api_docs.md")


@pytest.fixture
def client():
    auth = IlcpAuthProvider()
    return IlcpWorkflowClient(
        parser_cls=IlcpApiDocsParser,
        api_docs_path=API_DOCS,
        skill_name="ehz-ilcp-workflow",
        auth_provider=auth,
        param_mapping={},
        aliases={
            "get-flow-state": "获取审批流实例状态",
            "repeal-flow": "撤销审批流",
            "get-finish-record": "获取审批流完成记录",
        },
    )


@pytest.fixture
def eps(client):
    return client.parser.parse_file(API_DOCS)


class TestClientEndpoints:
    def test_all_4_endpoints_loaded(self, client):
        assert len(client.endpoints) == 4

    def test_to_cmd_name(self, client):
        # _to_cmd_name 对中文不转换，返回原始中文
        result = client._to_cmd_name("get-flow-state")
        assert result  # 只需确认不报错

    def test_build_cmd_map(self, client):
        cmd_map = client._build_cmd_map()
        # 第一个条目以中文名作为 key
        chinese_names = [ep.name for ep in client.endpoints]
        for name in chinese_names:
            assert name in cmd_map, f"中文名 {name} 不在 cmd_map 中"
        # 英文别名
        assert "get-flow-state" in cmd_map
        assert "repeal-flow" in cmd_map
        assert "get-finish-record" in cmd_map

    def test_alias_registration(self, client):
        cmd_map = client._build_cmd_map()
        assert "get-flow-state" in cmd_map
        assert "repeal-flow" in cmd_map
        assert "get-finish-record" in cmd_map


class TestPayloadBuilding:
    def test_initiate_flow_payload(self, client, eps):
        args = argparse.Namespace(
            command="发起审批流",
            flowid="FLOW_001",
            initiator="user001",
            formFields='{"datas": []}',
            **{"formFields.datas": ""},
            **{"formFields.datas[].field": ""},
            **{"formFields.datas[].value": ""},
            bid="",
            suggestion="",
        )
        payload = client._build_payload(args, eps[0])
        assert payload["flowid"] == "FLOW_001"
        assert payload["initiator"] == "user001"
        assert "formFields" in payload

    def test_initiate_flow_bid_default(self, client, eps):
        """bid 为空时应从 request_example 取默认值"""
        args = argparse.Namespace(
            command="发起审批流",
            flowid="FLOW_001",
            initiator="user001",
            formFields="",
            **{"formFields.datas": ""},
            **{"formFields.datas[].field": ""},
            **{"formFields.datas[].value": ""},
            bid="",
            suggestion="",
        )
        payload = client._build_payload(args, eps[0])
        assert "bid" in payload

    def test_get_flow_state_payload(self, client, eps):
        args = argparse.Namespace(command="get-flow-state", bid="BIZ20260327001")
        payload = client._build_payload(args, eps[1])
        assert payload == {"bid": "BIZ20260327001"}

    def test_repeal_flow_payload(self, client, eps):
        args = argparse.Namespace(
            command="repeal-flow",
            bid="BIZ20260327001",
            suggestion="申请有误重新提交",
        )
        payload = client._build_payload(args, eps[2])
        assert payload["bid"] == "BIZ20260327001"
        assert payload["suggestion"] == "申请有误重新提交"

    def test_repeal_flow_optional_suggestion(self, client, eps):
        args = argparse.Namespace(command="repeal-flow", bid="BIZ20260327001", suggestion="")
        payload = client._build_payload(args, eps[2])
        assert "bid" in payload

    def test_get_finish_record_payload(self, client, eps):
        args = argparse.Namespace(
            command="get-finish-record",
            initiator="user001",
            startTime="2026-03-01 00:00:00",
            endTime="2026-03-31 23:59:59",
        )
        payload = client._build_payload(args, eps[3])
        assert payload["initiator"] == "user001"
        assert payload["startTime"] == "2026-03-01 00:00:00"
        assert payload["endTime"] == "2026-03-31 23:59:59"

    def test_get_finish_record_type_coercion(self, client, eps):
        """startTime/endTime 保持为字符串"""
        args = argparse.Namespace(
            command="get-finish-record",
            initiator="user001",
            startTime="2026-03-01 00:00:00",
            endTime="2026-03-31 23:59:59",
        )
        payload = client._build_payload(args, eps[3])
        assert isinstance(payload["startTime"], str)
        assert isinstance(payload["endTime"], str)


class TestArgparserBuilding:
    def test_argparser_has_4_subcommands(self, client):
        # 检查 subparsers 中有 4 个命令
        assert len(client.subparsers.choices) >= 4

    def test_initiate_flow_subcommand(self, client):
        sub = client.subparsers.choices.get("发起审批流") or client.subparsers.choices.get("initiate-flow")
        assert sub is not None

    def test_get_flow_state_subcommand(self, client):
        sub = client.subparsers.choices.get("get-flow-state")
        assert sub is not None


class TestResolveEndpoint:
    def test_resolve_by_chinese_name(self, client):
        args = argparse.Namespace(command="发起审批流")
        ep = client._resolve_endpoint(args)
        assert ep is not None
        assert "发起审批流" in ep.name

    def test_resolve_by_alias(self, client):
        args = argparse.Namespace(command="get-flow-state")
        ep = client._resolve_endpoint(args)
        assert ep is not None
        assert "/getFlowState" in ep.path

    def test_resolve_invalid(self, client):
        args = argparse.Namespace(command="invalid-cmd-xyz")
        ep = client._resolve_endpoint(args)
        assert ep is None


class TestAuthProvider:
    def test_ilcp_auth_provider_class_vars(self):
        assert IlcpAuthProvider._api_url is not None
        assert IlcpAuthProvider._token_valid_seconds == 900

    def test_ilcp_auth_provider_init(self):
        auth = IlcpAuthProvider()
        assert auth.skill_name == "ehz-ilcp-workflow"
        assert auth._token is None
        assert auth._token_expires_at == 0

    def test_ilcp_auth_headers_raises_without_creds(self):
        auth = IlcpAuthProvider()
        auth._secret_id = ""
        auth._secret_key = ""
        with pytest.raises(RuntimeError, match="SECRET"):
            auth.ensure_token()

    def test_ilcp_auth_get_auth_endpoint(self):
        auth = IlcpAuthProvider()
        assert "/getAccessToken" in auth.get_auth_endpoint()
