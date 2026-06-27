"""base - 通用基础模块，供所有 skill 复用"""
from base.auth import AuthProvider
from base.parser import BaseMarkdownParser, ApiEndpoint, ApiParam
from base.client import DynamicApiClient

__all__ = ["AuthProvider", "BaseMarkdownParser", "ApiEndpoint", "ApiParam", "DynamicApiClient"]
