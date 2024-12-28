import re
import time
from typing import List, Optional
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from .. import *

BASE_URL = "https://animetosho.org/search?"


def extract_time(text, time_fmt) -> str:
    short_match = re.search(r"(Today|Yesterday)\s(\d{2}:\d{2})", text)
    if short_match:
        day_str = short_match.group(1)
        time_str = short_match.group(2)

        now = time.localtime()

        if day_str == 'Today':
            date_str = time.strftime('%d/%m/%Y', now)
        else:  # Yesterday
            yesterday = time.localtime(time.time() - 86400)
            date_str = time.strftime('%d/%m/%Y', yesterday)

        datetime_str = f"{date_str} {time_str}"
        time_tuple = time.strptime(datetime_str, '%d/%m/%Y %H:%M')
        return time.strftime(time_fmt, time_tuple)

    else:
        long_match = re.search(r"(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2})", text)
        if long_match:
            datetime_str = long_match.group(1)
            time_tuple = time.strptime(datetime_str, '%d/%m/%Y %H:%M')
            return time.strftime(time_fmt, time_tuple)


class Animetosho(BasePlugin):
    abstract = False

    def __init__(self,
                 parser: str = 'lxml',
                 verify: bool = False,
                 timefmt: str = r'%Y/%m/%d %H:%M') -> None:

        super().__init__(parser, verify, timefmt)

    def search(self,
               keyword: str,
               collected: bool = False,
               proxies: Optional[dict] = None,
               system_proxy: bool = False,
               **extra_options) -> List[Anime] | None:

        animes: List[Anime] = []
        page = 1
        params = {'q': keyword, **extra_options}

        if collected:
            log.warning("Animetosho search does not support collection.")

        while True:
            log.debug(f"Processing the page of {page}")

            params['page'] = page
            url = BASE_URL + urlencode(params)
            html = get_content(url, verify=self._verify, proxies=proxies, system_proxy=system_proxy)

            try:
                bs = BeautifulSoup(html, self._parser)
                items = bs.find_all(class_='home_list_entry')

                if not items:
                    break

                for item in items:
                    title_elem = item.find(class_='link')
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)

                    from_time = item.find(class_='date')['title']
                    to_time = extract_time(from_time, self.timefmt)

                    size = item.find(class_='size').string
                    torrent = item.find("a", class_="dllink")['href']
                    magnet = item.find("a", class_="dllink").find_next("a")['href']

                    log.debug(f"Successfully got: {title}")

                    animes.append(Anime(to_time, title, size, magnet, torrent))

                page += 1

            except Exception as e:
                raise SearchParserError(
                    f"An error occurred while processing the page of {page} with error {e!r}") from e

        return animes
