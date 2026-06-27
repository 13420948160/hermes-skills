"""认证提供者基类"""
from abc import ABC, abstractmethod


class AuthProvider(ABC):
    """认证提供者抽象基类，子类实现具体认证逻辑"""

    @abstractmethod
    def ensure_token(self) -> tuple[str, str]:
        """确保有效 token，返回 (token, apikey)"""
        pass

    @abstractmethod
    def headers(self) -> dict:
        """返回认证请求头"""
        pass

    @abstractmethod
    def get_auth_endpoint(self) -> str | None:
        """返回认证接口路径，若为 None 则使用无认证模式"""
        pass
