import concurrent.futures
from typing import List, Optional

from . import PluginMeta, get_plugin
from .. import *


class Aggregator(BasePlugin):
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
               system_proxy: Optional[bool] = False,
               **extra_options) -> List[Anime] | None:
        animes: List[Anime] = []

        def run_plugin_search(plugin):
            try:
                return plugin.search(keyword, collected, proxies, system_proxy, **extra_options)
            except Exception as e:
                PluginImportError(f"Error occurred in plugin {plugin.__class__.__name__}: {e!r}")
                return []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(run_plugin_search, plugin) for plugin in PluginMeta.plugins]
            for future in concurrent.futures.as_completed(futures):
                results = future.result()
                if results:
                    animes.extend(results)

        return animes
