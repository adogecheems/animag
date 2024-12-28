import time
from os import wait
from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from .. import *

DOMAIN = "https://acg.rip"
BASE_URL = "https://acg.rip/page/{}.xml?"
MAX_PAGE = 5


class AcgripRss(BasePlugin):
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
        page = 1

        params = {'term': keyword, **extra_options}

        if collected:
            log.warning("Acg.rip searcher does not support collection.")

        while True:
            log.debug(f"Processing the page of {page}")

            url = BASE_URL.format(page) + urlencode(params)
            xml = get_content(url, verify=self._verify, proxies=proxies, system_proxy=system_proxy)

            try:
                if page > MAX_PAGE:
                    break

                bs = BeautifulSoup(xml, features="xml")
                items = bs.find_all("item")

                if not items:
                    break

                for item in items:
                    title = item.find("title").string
                    torrent = item.find("link").string

                    from_time = item.find("pubDate").string
                    to_time = time.strftime(self.timefmt, time.strptime(from_time, "%a, %d %b %Y %H:%M:%S %z"))

                    log.debug(f"Successfully got the RSS item: {title}")

                    animes.append(Anime(to_time, title, None, None, torrent))

                page += 1
                time.sleep(1)

            except Exception as e:
                raise SearchParserError(
                    f"An error occurred while processing the page of {page} with error {e!r}") from e

        return animes
