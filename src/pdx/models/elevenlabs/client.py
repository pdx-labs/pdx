from typing import Dict, Optional, Tuple, Union
import aiohttp
import requests
import requests.adapters
import urllib.parse
import json
from pdx.models.api_client import APIClient, APIRequest
from pdx.models.elevenlabs.exceptions import handle_elevenlabs_request_error


class ElevenLabsClient(APIClient):
    def __init__(
        self,
        api_key: str,
        api_url: str = "https://api.elevenlabs.io",
        proxy_url: Optional[str] = None,
        request_timeout: Optional[Union[float,
                                        Tuple[float, float]]] = 600,
    ):
        super().__init__(api_key, api_url, proxy_url, request_timeout)

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
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key,
            **(headers or {}),
        }

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
                handle_elevenlabs_request_error(response.status_code, content)

        if isinstance(response, aiohttp.ClientResponse):
            if response.status != 200:
                handle_elevenlabs_request_error(response.status, content)
