'''
The following code is adopted from the Anthropic Python SDK, which is under 
MIT License.
https://github.com/anthropics/anthropic-sdk-python/blob/main/LICENSE

Copyright 2022 Anthropic, PBC.

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in the 
Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the 
following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.
'''

from typing import Dict, Optional, Tuple, NamedTuple, Union
import aiohttp
import requests
import requests.adapters
import urllib.parse
import json
from pdx.models.anthropic import constants
from pdx.models.anthropic.exceptions import handle_anthropic_request_error
from pdx.models.api_client import APIClient, APIRequest


class AnthropicClient(APIClient):
    def __init__(
        self,
        api_key: str,
        api_url: str = "https://api.anthropic.com",
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
    ) -> APIRequest:
        method = method.lower()
        abs_url = urllib.parse.urljoin(self.api_url, path)
        final_headers: dict[str, str] = {
            "Accept": "application/json",
            "Anthropic-SDK": 'dev',
            "Anthropic-Version": "2023-01-01",
            "X-API-Key": self.api_key,
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
                final_headers["Content-Type"] = "application/json"
            else:
                raise ValueError(f"Unrecognized method: {method}")
        # If we're requesting a stream from the server, let's tell requests to expect the same
        stream = params.get("stream", None)
        return APIRequest(
            method,
            abs_url,
            final_headers,
            data,
            stream,
            request_timeout or self.request_timeout,
        )

    def _response_middleware(self, response: Union[requests.Response, aiohttp.ClientResponse], content: str) -> dict:
        if isinstance(response, requests.Response):
            if response.status_code != 200:
                handle_anthropic_request_error(response.status_code, content)

        if isinstance(response, aiohttp.ClientResponse):
            if response.status != 200:
                handle_anthropic_request_error(response.status, content)
