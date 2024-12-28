import time
from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from .. import *

BASE_URL = "https://dmhy.org/topics/rss/rss.xml?"


class DmhyRss(BasePlugin):
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

        params = {'keyword': keyword, **extra_options}

        log.debug(f"Processing the page of 1")

        url = BASE_URL + urlencode(params)
        xml = get_content(url, verify=self._verify, proxies=proxies, system_proxy=system_proxy)

        try:
            bs = BeautifulSoup(xml, features="xml")
            items = bs.find_all("item")

            for item in items:
                title = item.find("title").string

                from_time = item.find("pubDate").string
                to_time = time.strftime(self.timefmt, time.strptime(from_time, "%a, %d %b %Y %H:%M:%S %z"))

                magnet = item.find("enclosure")["url"]

                log.debug(f"Successfully got the RSS item: {title}")

                animes.append(Anime(to_time, title, None, magnet, None))

        except Exception as e:
            print(e)
            raise SearchParserError(
                f"An error occurred while processing the page of 1 with error {e!r}") from e

        return animes
