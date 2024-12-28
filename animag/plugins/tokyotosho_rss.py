import time
from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from .. import *

BASE_URL = "https://www.tokyotosho.info/rss.php?"


class TokyotoshoRss(BasePlugin):
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
        params = {'terms': keyword, **extra_options}

        if collected:
            log.warning("Tokyotosho RSS search does not support collection.")

        log.debug(f"Processing the page of 1")

        url = BASE_URL + urlencode(params)
        xml = get_content(url, verify=self._verify, proxies=proxies, system_proxy=system_proxy)

        try:
            bs = BeautifulSoup(xml, features="xml")
            items = bs.find_all("item")

            for item in items:
                if item.find("category").text != "Anime":
                    continue

                title = item.find("title").string
                torrent = item.find("link").string

                description = item.find("description").text
                magnet = description.split('href="')[2].split('"')[0]
                size = description.split("Size: ")[1].split("<br")[0]

                from_time = item.find("pubDate").string
                to_time = time.strftime(self.timefmt, time.strptime(from_time, "%a, %d %b %Y %H:%M:%S %Z"))

                log.debug(f"Successfully got the RSS item: {title}")

                animes.append(Anime(to_time, title, size, magnet, torrent))

        except Exception as e:
            raise SearchParserError(
                f"An error occurred while processing the page of 1 with error {e!r}") from e

        return animes
