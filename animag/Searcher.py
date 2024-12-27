import copy
import csv
import time
from typing import List, Dict, Any

from . import *
from . import plugins


class Searcher:
    def __init__(self, plugin_name: str = 'dmhy',
                 parser: Optional[str] = None,
                 verify: Optional[bool] = None,
                 timefmt: Optional[str] = None,
                 no_search_errors: bool = False) -> None:
        """
        Initialize a Searcher object.

        Args:
            plugin_name: The name of the plugin, default is 'dmhy'.
            parser: The name of the parser to be used.
            verify: Whether to enable verification.
            timefmt: The format for time representation.
            no_search_errors: If True, suppresses search errors.

        Raises:
            ValueError: If the provided time format is invalid.
            PluginImportError: If the specified plugin cannot be found.
        """
        self.timefmt: Optional[str] = None
        self.animes: List[Anime] | None = None
        self.anime: Anime | None = None

        if no_search_errors:
            log.warning("Search errors will not be raised.")
            self.search = no_errors(self.search)

        self.plugin = self._load_plugin(plugin_name, parser, verify, timefmt)
        log.debug("New searcher object created.")

    def _load_plugin(self, plugin_name: str,
                     parser: Optional[str],
                     verify: Optional[bool],
                     timefmt: Optional[str]) -> Any:
        """Load and configure the specified search plugin."""
        kwargs: Dict[str, Any] = {}

        if parser is not None:
            kwargs['parser'] = parser
        if verify is not None:
            kwargs['verify'] = verify
        if timefmt is not None:
            self.set_timefmt(timefmt)
            kwargs['timefmt'] = self.timefmt

        plugin = plugins.get_plugin(plugin_name)(**kwargs)

        log.info(f"Successfully loaded plugin: {plugin_name}")
        return plugin

    def set_timefmt(self, to_timefmt: str) -> None:
        """
        Set and validate the time format.

        Args:
            to_timefmt: The time format string to set.

        Raises:
            TimeFormatError: If the provided time format is invalid.
        """
        try:
            time.strftime(to_timefmt, time.localtime())
        except Exception as e:
            raise TimeFormatError(f"Invalid time format {to_timefmt}: {e!r}") from e

        if self.animes is not None:
            from_timefmt = r'%Y/%m/%d %H:%M' if self.timefmt is None else self.timefmt

            for anime in self.animes:
                anime.set_timefmt(from_timefmt, to_timefmt)

        self.timefmt = to_timefmt

    def search(self, keyword: str,
               collected: Optional[bool] = None,
               proxies: Optional[dict] = None,
               system_proxy: Optional[bool] = None,
               **extra_options) -> List[Anime] | None:
        """
        Search for anime using the specified keyword.

        Args:
            keyword: The keyword to search for.
            collected: Whether to collect results.
            proxies: Proxy settings to use for the search.
            system_proxy: Whether to use the system's proxy settings.
            **extra_options: Additional search options provided as keyword arguments.

        Returns:
            A list of found anime or None if the search fails.

        Raises:
            SearchRequestError: If the search request fails.
            SearchParseError: If parsing the search result fails.
        """
        self.animes = None

        kwargs = {
            'keyword': keyword,
            **({} if collected is None else {'collected': collected}),
            **({} if not proxies else {'proxies': proxies}),
            **({} if system_proxy is None else {'system_proxy': system_proxy}),
            **extra_options
        }

        try:
            self.animes = self.plugin.search(**kwargs)
        except Exception as e:
            log.error(f"Search failed for '{keyword}': {e!r}")
            raise
        else:
            log.info(f"Search completed successfully: {keyword}")

        return self.animes

    def get_animes(self) -> List[Anime]:
        """
        Retrieve the list of anime from the search results.

        Returns:
            A list of Anime objects.

        Raises:
            ValueError: If there are no search results available.
        """
        if self.animes is None:
            raise ValueError("No search results available.")

        return self.animes

    def get_anime(self, index: int) -> Anime:
        """
        Retrieve the anime at the specified index in the search results.

        Args:
            index: The index of the anime to retrieve.

        Returns:
            The Anime object at the specified index.

        Raises:
            ValueError: If there are no search results available.
            IndexError: If the provided index is out of range.
        """
        if self.animes is None:
            raise ValueError("No search results available.")

        if index < 0 or index >= len(self.animes):
            raise IndexError(f"Index {index} out of range.")

        return self.animes[index]

    def size_format_all(self, unit: str = 'MB') -> List[Anime]:
        """
        Convert the size of all anime in the search results to the specified unit.

        Args:
            unit: The target size unit for conversion, default is 'MB'.

        Returns:
            A list of Anime objects with their sizes formatted in the specified unit.

        Raises:
            ValueError: If there are no search results available.
            SizeFormatError: If size formatting fails.
        """
        if self.animes is None:
            raise ValueError("No search results available.")

        try:
            formatted_animes = copy.deepcopy(self.animes)
            for anime in formatted_animes:
                anime.size_format(unit)
        except:
            raise
        else:
            self.animes = formatted_animes

        return self.animes

    def save_csv(self, filename: str) -> None:
        """
        Save the search results to a CSV file.

        Args:
            filename: The name of the CSV file where results will be saved.

        Raises:
            ValueError: If there are no search results available.
            SaveCSVError: If saving to the CSV file fails.
        """
        if self.animes is None:
            raise ValueError("No search results available.")

        fieldnames = ["time", "title", "size", "magnet", "torrent"]

        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for anime in self.animes:
                    writer.writerow({
                        "time": anime.time if anime.time else "Unknown",
                        "title": anime.title if anime.title else "Unknown",
                        "size": anime.size if anime.size else "Unknown",
                        "magnet": anime.magnet if anime.magnet else "Unknown",
                        "torrent": anime.torrent if anime.torrent else "Unknown"
                    })

        except Exception as e:
            raise SaveCSVError(f"Failed to save CSV file '{filename}': {e!r}") from e


if __name__ == "__main__":
    import doctest

    doctest.testmod()
