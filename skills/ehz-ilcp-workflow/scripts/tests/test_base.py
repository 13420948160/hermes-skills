"""Base 框架测试"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.parser import ApiParam, ApiEndpoint
from base.auth import AuthProvider


class TestApiParam:
    def test_api_param_creation(self):
        p = ApiParam(name="flowid", param_type="String", required=True, description="审批流程定义ID", default="")
        assert p.name == "flowid"
        assert p.param_type == "String"
        assert p.required is True
        assert p.description == "审批流程定义ID"
        assert p.default == ""

    def test_api_param_defaults(self):
        p = ApiParam(name="bid", param_type="String", required=False, description="业务ID")
        assert p.default == ""

    # dataclass 默认不禁用赋值，故不测试不可变性


class TestApiEndpoint:
    def test_api_endpoint_minimal(self):
        ep = ApiEndpoint(index=1, name="发起审批流")
        assert ep.index == 1
        assert ep.name == "发起审批流"
        assert ep.method == "POST"
        assert ep.parameters == []

    def test_api_endpoint_full(self):
        p = ApiParam(name="flowid", param_type="String", required=True, description="ID")
        ep = ApiEndpoint(
            index=1, name="发起审批流", method="POST",
            path="/ESBREST/faas/code/initiateFlow",
            description="发起一个新的审批流程实例",
            parameters=[p],
            request_example={"flowid": "FLOW_001"},
            response_example={"errorCode": 0},
            notes="- test note",
        )
        assert ep.index == 1
        assert ep.path == "/ESBREST/faas/code/initiateFlow"
        assert len(ep.parameters) == 1
        assert ep.request_example == {"flowid": "FLOW_001"}
        assert "test note" in ep.notes

    # dataclass 默认不禁用赋值，故不测试不可变性


class TestAuthProvider:
    def test_auth_provider_abstract(self):
        with pytest.raises(TypeError):
            AuthProvider()

    def test_auth_provider_incomplete_subclass(self):
        class Bad(AuthProvider):
            pass
        with pytest.raises(TypeError):
            Bad()

    def test_auth_provider_complete_subclass(self):
        class Good(AuthProvider):
            def ensure_token(self): return ("token", "apikey")
            def headers(self): return {"Authorization": "Bearer token"}
            def get_auth_endpoint(self): return "/auth"

        provider = Good()
        assert provider.ensure_token() == ("token", "apikey")
        assert "Authorization" in provider.headers()
        assert provider.get_auth_endpoint() == "/auth"
