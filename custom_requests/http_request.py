"""
Class for sync/async requests.
"""
from typing import Any, Dict

import httpx


class HttpClient:
    def __init__(self, timeout: float = 10.0, verify_ssl: bool = True):
        self.timeout = timeout
        self.verify_ssl = verify_ssl

    def get_sync(self, url: str, headers: dict | None = None,
                 params: dict | None = None) -> Dict[str, Any]:
        """Sync GET request"""
        with httpx.Client(verify=self.verify_ssl) as client:
            response = client.get(url, headers=headers, params=params,
                                  timeout=self.timeout)
            response.raise_for_status()
            return response.json()

    async def get_async(self, url: str, headers: dict | None = None,
                        params: dict | None = None) -> Dict[str, Any]:
        """Async GET request"""
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            response = await client.get(url, headers=headers, params=params,
                                        timeout=self.timeout)
            response.raise_for_status()
            return response.json()
