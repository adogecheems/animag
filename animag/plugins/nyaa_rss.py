import time
from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from .. import *

DOMAIN = "https://nyaa.si"
BASE_URL = "https://nyaa.si/?page=rss&"


class NyaaRss(BasePlugin):
    abstract = False

    def __init__(self,
                 parser: str = None,
                 verify: bool = False,
                 timefmt: str = r'%Y/%m/%d %H:%M') -> None:

        if parser:
            log.warning("RSS feed does not need a parser, it will be ignored.")

        super().__init__(parser, verify, timefmt)

    def search(self,
               keyword: str,
               collected: bool = False,
               proxies: Optional[dict] = None,
               system_proxy: bool = False,
               **extra_options) -> List[Anime] | None:

        animes: List[Anime] = []
        params = {'q': keyword, 'c': "1_0", **extra_options}

        if collected:
            log.warning("Nyaa RSS search does not support collection.")

        url = BASE_URL + urlencode(params)
        xml = get_content(url, verify=self._verify, proxies=proxies, system_proxy=system_proxy)

        try:
            bs = BeautifulSoup(xml, features="xml")
            items = bs.find_all("item")

            if not items:
                return None

            for item in items:
                title = item.find("title").text
                torrent = item.find("link").text

                from_time = item.find("pubDate").text
                to_time = time.strftime(self.timefmt, time.strptime(from_time, "%a, %d %b %Y %H:%M:%S %z"))

                info_hash = item.find("nyaa:infoHash").text
                magnet = f"magnet:?xt=urn:btih:{info_hash}&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"
                size = item.find("nyaa:size").text

                log.debug(f"Successfully got the RSS item: {title}")

                animes.append(Anime(to_time, title, size, magnet, torrent, info_hash))

        except Exception as e:
            raise SearchParserError(f"An error occurred while processing the RSS feed with error {e!r}") from e

        return animes
