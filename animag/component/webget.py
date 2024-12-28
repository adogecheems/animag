import os
from functools import lru_cache
from typing import Optional, Dict

import requests
from requests import RequestException
from urllib3.exceptions import InsecureRequestWarning

from .. import SearchRequestError, log

DEFAULT_TIMEOUT = 10
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}


@lru_cache(maxsize=32)
def get_system_proxies() -> Dict[str, str]:
    """Get system proxy settings."""
    proxies = {}
    for protocol in ['http', 'https']:
        if proxy := os.environ.get(f'{protocol}_proxy'):
            proxies[protocol] = proxy
    return proxies


def get_content(
        url: str,
        proxies: Optional[Dict[str, str]] = None,
        system_proxy: bool = False,
        verify: bool = True,
        fake_user_agent: bool = True
) -> bytes:
    """Get content from URL."""
    if not verify:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    if system_proxy:
        proxies = get_system_proxies()

    try:
        response = requests.get(
            url,
            headers=DEFAULT_HEADERS if fake_user_agent else None,
            proxies=proxies,
            verify=verify,
            timeout=DEFAULT_TIMEOUT
        )
        log.debug(f"A request was made to {url}")

        if response.status_code not in (200, 302):
            raise SearchRequestError(f"Invalid status code {response.status_code} for URL: {url}")

        return response.content

    except RequestException as e:
        raise SearchRequestError(f"Request failed for URL {url}: {e!r}") from e
