from typing import Dict, Optional, Tuple, Union
import aiohttp
import requests
import requests.adapters
import urllib.parse
import json
from pdx.models.api_client import APIClient, APIRequest
from pdx.models.replicate.helpers import poll_status, apoll_status
from pdx.models.replicate.exceptions import handle_replicate_request_error


class ReplicateClient(APIClient):
    def __init__(
        self,
        api_key: str,
        api_url: str = "https://api.replicate.com",
        proxy_url: Optional[str] = None,
        poll_interval: int = 7,
        request_timeout: Optional[Union[float,
                                        Tuple[float, float]]] = 600,
    ):
        super().__init__(api_key, api_url, proxy_url, request_timeout)
        self.poll_interval = poll_interval

        self._setup_session()

    def _request_middleware(
        self,
        headers: Optional[Dict[str, str]],
        method: str,
        params: dict,
        path: str,
        request_timeout: Optional[Union[float, Tuple[float, float]]],
        files: dict = None,
    ) -> APIRequest:
        method = method.lower()
        abs_url = urllib.parse.urljoin(self.api_url, path)
        final_headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.api_key}",
            **(headers or {}),
        }

        data = None
        if params:
            if method in {"post"}:
                data = json.dumps(params).encode()
            else:
                raise ValueError(f"Unrecognized method: {method}")

        # TODO: Add support for stream, tell requests if to expect a stream
        stream = params.get("stream", None)
        return APIRequest(
            method,
            abs_url,
            final_headers,
            data,
            files,
            stream,
            request_timeout or self.request_timeout,
        )

    def _response_middleware(self, response: Union[requests.Response, aiohttp.ClientResponse], content: str) -> dict:
        if isinstance(response, requests.Response):
            if response.status_code != 200:
                handle_replicate_request_error(response.status_code, content)

        if isinstance(response, aiohttp.ClientResponse):
            if response.status != 200:
                handle_replicate_request_error(response.status, content)

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

        _r: requests.Response = self._session.request(
            request.method,
            request.url,
            headers=request.headers,
            data=request.data,
            stream=request.stream,
            timeout=request.timeout,
            files=request.files,
        )

        _r_json = _r.json()
        get_prediction_url = _r_json["urls"]["get"]
        _rp = poll_status(api_key=self.api_key, get_url=get_prediction_url, poll_interval=self.poll_interval)
        content = _rp.content
        self._response_middleware(_rp, content)
        return content

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
            ) as _r:
                _r_json = await _r.json()
                get_prediction_url = _r_json["urls"]["get"]
                _rp = await apoll_status(api_key=self.api_key, get_url=get_prediction_url, poll_interval=self.poll_interval)
                content = await _rp.read()
                self._response_middleware(_rp, content)
                return content
