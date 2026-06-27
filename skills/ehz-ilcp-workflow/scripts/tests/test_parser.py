"""IlcpApiDocsParser 测试 - 基于 api_docs.md"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_parser import IlcpApiDocsParser

API_DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "references", "api_docs.md")


class TestIlcpApiDocsParser:
    def test_parse_file_count(self):
        parser = IlcpApiDocsParser()
        eps = parser.parse_file(API_DOCS)
        assert len(eps) == 4, f"期望4个接口，实际{len(eps)}"

    def test_ep1_initiate_flow(self):
        parser = IlcpApiDocsParser()
        eps = parser.parse_file(API_DOCS)
        ep = eps[0]
        assert ep.index == 1
        assert "发起审批流" in ep.name
        assert ep.method == "POST"
        assert "/initiateFlow" in ep.path

    def test_ep1_params(self):
        parser = IlcpApiDocsParser()
        eps = parser.parse_file(API_DOCS)
        ep = eps[0]
        names = {p.name for p in ep.parameters}
        assert "flowid" in names
        assert "initiator" in names
        assert "formFields" in names
        assert "bid" in names
        assert "suggestion" in names

    def test_ep1_required_fields(self):
        parser = IlcpApiDocsParser()
        eps = parser.parse_file(API_DOCS)
        ep = eps[0]
        flowid = next(p for p in ep.parameters if p.name == "flowid")
        assert flowid.required is True
        bid = next(p for p in ep.parameters if p.name == "bid")
        assert bid.required is False

    def test_ep1_request_example(self):
        parser = IlcpApiDocsParser()
        eps = parser.parse_file(API_DOCS)
        ep = eps[0]
        assert ep.request_example is not None
        assert "flowid" in ep.request_example
        assert ep.request_example["flowid"] == "FLOW_001"

    def test_ep1_response_example(self):
        parser = IlcpApiDocsParser()
        eps = parser.parse_file(API_DOCS)
        ep = eps[0]
        assert ep.response_example is not None
        assert ep.response_example["errorCode"] == 0
        assert "return" in ep.response_example

    def test_ep2_get_flow_state(self):
        parser = IlcpApiDocsParser()
        eps = parser.parse_file(API_DOCS)
        ep = eps[1]
        assert ep.index == 2
        assert "获取审批流实例状态" in ep.name
        assert "/getFlowState" in ep.path
        assert len(ep.parameters) >= 1
        bid = next((p for p in ep.parameters if p.name == "bid"), None)
        assert bid is not None
        assert bid.required is True
        assert ep.request_example is not None
        assert "bid" in ep.request_example

    def test_ep3_repeal_flow(self):
        parser = IlcpApiDocsParser()
        eps = parser.parse_file(API_DOCS)
        ep = eps[2]
        assert ep.index == 3
        assert "撤销审批流" in ep.name
        assert "/repealFlow" in ep.path
        params = {p.name for p in ep.parameters}
        assert "bid" in params
        assert "suggestion" in params
        assert ep.request_example is not None

    def test_ep4_get_finish_record(self):
        parser = IlcpApiDocsParser()
        eps = parser.parse_file(API_DOCS)
        ep = eps[3]
        assert ep.index == 4
        assert "获取审批流完成记录" in ep.name
        assert "/getFlowFinishRecord" in ep.path
        params = {p.name for p in ep.parameters}
        assert "initiator" in params
        assert "startTime" in params
        assert "endTime" in params
        assert ep.request_example is not None
        assert ep.request_example["initiator"] == "user001"

    def test_parse_string(self):
        parser = IlcpApiDocsParser()
        with open(API_DOCS, encoding="utf-8") as f:
            content = f.read()
        eps = parser.parse_string(content)
        assert len(eps) == 4

    def test_parse_string_empty(self):
        parser = IlcpApiDocsParser()
        eps = parser.parse_string("")
        assert eps == []

    def test_no_duplicate_params(self):
        """EP4 不应有重复的 initiator 参数"""
        parser = IlcpApiDocsParser()
        eps = parser.parse_file(API_DOCS)
        ep4 = eps[3]
        names = [p.name for p in ep4.parameters]
        initiator_count = names.count("initiator")
        assert initiator_count == 1, f"initiator 重复了 {initiator_count} 次"

    def test_description_extracted(self):
        """接口描述应被正确提取"""
        parser = IlcpApiDocsParser()
        eps = parser.parse_file(API_DOCS)
        for ep in eps:
            assert ep.description != "", f"EP{ep.index} 描述为空"
