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
    files: Optional[Dict[str, bytes]]
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
        files: dict,
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
        files: dict = None,
        headers: Optional[Dict[str, str]] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> dict:
        request = self._request_middleware(
            headers, method, params, path, request_timeout, files)

        _response: requests.Response = self._session.request(
            request.method,
            request.url,
            headers=request.headers,
            data=request.data,
            stream=request.stream,
            timeout=request.timeout,
            files=request.files,
        )

        # content = _response.content.decode("utf-8")
        content = _response.content
        self._response_middleware(_response, content)
        return content
        # TODO: content is what is returned
        # json_content = json.loads(content)
        # return json_content
        # return _response

    async def arequest(
        self,
        method: str,
        path: str,
        params: dict,
        files: dict = None,  # TODO: implement in async
        headers: Optional[Dict[str, str]] = None,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> dict:
        request = self._request_middleware(
            headers, method, params, path, request_timeout, files)

        if files is not None:
            _data = aiohttp.FormData()
            for k, v in request.data.items():
                _data.add_field(k, str(v))
            for k, v in request.files.items():
                _data.add_field(k, v[1])
        else:
            _data = request.data
        async with aiohttp.ClientSession() as session:
            async with session.request(
                request.method,
                request.url,
                headers=request.headers,
                data=_data,
                timeout=request.timeout,
                proxy=self.proxy_url,
            ) as _response:
                # content = await _response.text()
                content = await _response.read()
                self._response_middleware(_response, content)
                return content
                # TODO: content is what is returned
                # json_content = json.loads(content)
                # return json_content
