import asyncio
import time
import requests
import aiohttp


def poll_status(api_key: str, get_url: str, timeout: int = 300, poll_interval: int = 7) -> requests.Response:
    headers = {"Authorization": f"Token {api_key}"}
    _timein = 0
    while True:
        time.sleep(7)  # wait for 7 seconds
        _r = requests.get(url=get_url, headers=headers)
        _r_data = _r.json()
        if _r_data['status'] == 'succeeded':
            return _r
        if _timein >= timeout:
            raise TimeoutError
        _timein += poll_interval


async def apoll_status(api_key: str, get_url: str, timeout: int = 300, poll_interval: int = 7) -> requests.Response:
    headers = {"Authorization": f"Token {api_key}"}
    _timein = 0
    async with aiohttp.ClientSession() as _session:
        while True:
            await asyncio.sleep(7)  # wait for 7 seconds
            async with _session.request(
                'GET',
                get_url,
                headers=headers,
            ) as _response:
                _r_data = await _response.json()
                if _r_data['status'] == 'succeeded':
                    return _response
                if _timein >= timeout:
                    raise TimeoutError
                _timein += poll_interval
