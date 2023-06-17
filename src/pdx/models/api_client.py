from typing import Dict, Optional, Tuple, NamedTuple, Union
import aiohttp
import requests
import requests.adapters
import json
from pdx.exceptions import ModelError


class APIRequest(NamedTuple):
    method: str
    url: str
    headers: Optional[Dict[str, str]]
    data: bytes
    stream: bool
    timeout: Optional[Union[float, Tuple[float, float]]]


class APIClient:
    def __init__(
        self,
        api_key: str,
        api_url: str,
        proxy_url: Optional[str] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = 600,
    ):
        self.max_retries = 2

        self.api_key = api_key
        self.api_url = api_url
        self.proxy_url = proxy_url
        self.request_timeout = request_timeout
        
        self._session: Optional[requests.Session] = None
        self._setup_session()

    def _setup_session(self) -> requests.Session:
        self._session = requests.Session()
        if self.proxy_url:
            self._session.proxies = {"https": self.proxy_url}
        self._session.mount(
            "https://",
            requests.adapters.HTTPAdapter(
                max_retries=self.max_retries),
        )

    def _request_middleware(
        self,
        headers: Optional[Dict[str, str]],
        method: str,
        params: dict,
        path: str,
        request_timeout: Optional[Union[float, Tuple[float, float]]],
    ) -> APIRequest:
        pass

    def _response_middleware(self, response: Union[requests.Response, aiohttp.ClientResponse], content: str) -> dict:
        if isinstance(response, requests.Response):
            if response.status_code != 200:
                raise ModelError(response.status_code, content)
        
        if isinstance(response, aiohttp.ClientResponse):
            if response.status != 200:
                raise ModelError(response.status, content)

    def request(
        self,
        method: str,
        path: str,
        params: dict,
        headers: Optional[Dict[str, str]] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> dict:
        request = self._request_middleware(
            headers, method, params, path, request_timeout)

        _response: requests.Response = self._session.request(
            request.method,
            request.url,
            headers=request.headers,
            data=request.data,
            stream=request.stream,
            timeout=request.timeout,
        )
        content = _response.content.decode("utf-8")
        self._response_middleware(_response, content)
        json_content = json.loads(content)
        return json_content

    async def arequest(
        self,
        method: str,
        path: str,
        params: dict,
        headers: Optional[Dict[str, str]] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> dict:
        request = self._request_middleware(
            headers, method, params, path, request_timeout)
        async with aiohttp.ClientSession() as session:
            async with session.request(
                request.method,
                request.url,
                headers=request.headers,
                data=request.data,
                timeout=request.timeout,
                proxy=self.proxy_url,
            ) as _response:
                content = await _response.text()
                self._response_middleware(_response, content)
                json_content = json.loads(content)
                return json_content
