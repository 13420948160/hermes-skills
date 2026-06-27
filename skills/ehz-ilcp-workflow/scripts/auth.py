"""ILCP 审批流认证提供者"""
import logging
import os
import time
import requests
from requests.exceptions import ConnectTimeout, ReadTimeout, ConnectionError as ReqConnectionError

from base.auth import AuthProvider

logger = logging.getLogger(__name__)

API_URL = os.environ.get("API_URL", "your_api_url_here")
ACCOUNT_ID = os.environ.get("ACCOUNT_ID", "your_account_id_here")
SECRET_ID = os.environ.get("SECRET_ID", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")
TOKEN_VALID_SECONDS = int(os.environ.get("TOKEN_VALID_SECONDS", "900"))


class IlcpAuthProvider(AuthProvider):
    """ILCP 审批流认证提供者，token 缓存于实例属性，线程安全"""

    _api_url: str = API_URL
    _account_id: str = ACCOUNT_ID
    _secret_id: str = SECRET_ID
    _secret_key: str = SECRET_KEY
    _token_valid_seconds: int = TOKEN_VALID_SECONDS

    def __init__(self):
        self.skill_name: str = "ehz-ilcp-workflow"
        self._token: str | None = None
        self._apikey: str | None = None
        self._token_expires_at: float = 0

    def ensure_token(self) -> tuple[str, str]:
        now = time.time()
        if self._token and now < self._token_expires_at:
            return self._token, self._apikey

        if not self._secret_id or not self._secret_key:
            raise RuntimeError(
                "环境变量 SECRET_ID 和 SECRET_KEY 未设置，请配置后再调用接口。"
                "示例: export SECRET_ID=your_secret_id && export SECRET_KEY=your_secret_key"
            )

        payload = {
            "AccountId": self._account_id,
            "SecretId": self._secret_id,
            "SecretKey": self._secret_key,
        }
        headers = {"Content-Type": "application/json"}
        url = f"{self._api_url}/ESBREST/faas/code/getAccessToken"

        last_err: Exception | None = None
        for attempt in range(2):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                break
            except (ConnectTimeout, ReadTimeout) as e:
                logger.warning("token 请求超时（尝试 %d/2）", attempt + 1)
                last_err = e
            except ReqConnectionError as e:
                logger.warning("token 连接失败（尝试 %d/2）: %s", attempt + 1, e)
                last_err = e
            except requests.exceptions.RequestException as e:
                logger.error("token 请求异常: %s", e)
                last_err = e
            if attempt == 0:
                time.sleep(0.5)
        else:
            raise RuntimeError(f"获取 access token 失败: {last_err}")

        if data.get("code") != 0:
            raise RuntimeError(f"获取 access token 失败: {data.get('msg', data)}")

        self._token = data["data"]["token"]
        self._apikey = data["data"]["apikey"]
        self._token_expires_at = now + self._token_valid_seconds - 30
        logger.info("token 刷新成功，有效期 %ds", self._token_valid_seconds - 30)
        return self._token, self._apikey

    def headers(self) -> dict:
        token, apikey = self.ensure_token()
        return {
            "Authorization": f"Bearer {token}",
            "Sys-Apikey": apikey,
            "Content-Type": "application/json",
        }

    def get_auth_endpoint(self) -> str | None:
        return "/ESBREST/faas/code/getAccessToken"
