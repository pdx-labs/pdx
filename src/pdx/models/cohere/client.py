from typing import Dict, Optional, Tuple, NamedTuple, Union
import aiohttp
import requests
import requests.adapters
import urllib.parse
import json
from pdx.models.cohere.exceptions import handle_cohere_request_error
from pdx.models.api_client import APIClient, APIRequest


class CohereClient(APIClient):
    def __init__(
        self,
        api_key: str,
        api_url: str = "https://api.cohere.ai",
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
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}",
            **(headers or {}),
        }

        data = None
        if params:
            if method in {"get"}:
                encoded_params = urllib.parse.urlencode(
                    [(k, v) for k, v in params.items() if v is not None]
                )
                abs_url += "&%s" % encoded_params
            elif method in {"post", "put"}:
                data = json.dumps(params).encode()
                final_headers["content-type"] = "application/json"
            else:
                raise ValueError(f"Unrecognized method: {method}")
        # If we're requesting a stream from the server, let's tell requests to expect the same
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
                handle_cohere_request_error(response.status_code, content)

        if isinstance(response, aiohttp.ClientResponse):
            if response.status != 200:
                handle_cohere_request_error(response.status, content)
