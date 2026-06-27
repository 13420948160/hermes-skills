"""Markdown API 文档解析器基类"""
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class ApiParam:
    name: str
    param_type: str
    required: bool
    description: str
    default: str = ""


@dataclass
class ApiEndpoint:
    index: int
    name: str  # 接口名称（中文）
    method: str = "POST"
    path: str = ""
    description: str = ""
    parameters: list[ApiParam] = field(default_factory=list)
    request_example: dict | None = None
    response_example: dict | None = None
    notes: str = ""
    aliases: list[str] = field(default_factory=list)
    api_type: str = "iiot"  # 接口类型: iiot / faas


class BaseMarkdownParser(ABC):
    @abstractmethod
    def parse_file(self, path: str) -> list[ApiEndpoint]:
        """从文件路径解析 API 端点列表"""
        pass

    @abstractmethod
    def parse_string(self, content: str) -> list[ApiEndpoint]:
        """从字符串内容解析 API 端点列表"""
        pass
