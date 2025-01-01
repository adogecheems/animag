# Animag 2.0

---

## Project Overview

A Python library for searching anime magnet links and torrents, with strong extensibility.

Supports searching anime resources from different sources through a plugin system, and can handle magnet links, file
size conversion, and other functions.

Users of the old version should note that the project name has changed, so please reinstall it. Also, due to the
refactoring of version 2.0, some APIs may have changed. It is recommended to check the documentation.

## Main Features

- Supports search functionality across multiple resource sites
- Extensible plugin system
- File size unit conversion
- CSV export functionality
- Magnet link handling
- Time format conversion
- Error handling mechanism

## Installation

Animag can be easily installed using pip:

```commandline
pip install animag
```

## Usage Example

```python
# Import the Searcher class
from animag import Searcher

# Create a Searcher instance
searcher = Searcher(plugin_name='dmhy',
                    no_search_errors=True)

# Search for anime (proxy is for demonstration only)
searcher.search("葬送的芙莉莲",
                collected=True,
                proxies={'http': 'http://localhost:6666',
                         'https': 'http://localhost:6666'})

# Print the search results
print(searcher.get_animes())

"""
Example output (results from December 22, 2024):

Search completed successfully: 葬送的芙莉莲
[Anime(time='2024/10/20 12:23', title='[7³ACG\u200b] \u200b葬送的芙莉莲/Sousou no Frieren S01 | 01-28 [简繁字幕] BDrip 1080p AV1 OPUS 2.0\u200b\u200b\u200b', size='17.1GB', magnet='magnet:?xt=urn:btih:...

"""

# Convert all results' file sizes to GB
searcher.size_format_all('MB')

# Save results to a CSV file
searcher.save_csv("search_results.csv")
```

## Supported Plugins

|        Site         | Plugin Parameter Name |   Speed   | Full Season Search | size | magnet | torrent |                                                                                   Notes                                                                                    |
|:-------------------:|:---------------------:|:---------:|:------------------:|:----:|:------:|:-------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|      dmhy.org       |         dmhy          | Moderate  |         ✅          |  ✅   |   ✅    |    ❎    |                                                                                    None                                                                                    |
|      dmhy.org       |       dmhy_rss        | Very Fast |         ❎          |  ❎   |   ✅    |    ❎    |                                                                                    None                                                                                    |
|       nyaa.si       |         nyaa          | Very Fast |         ❎          |  ✅   |   ✅    |    ✅    |                                                                                    None                                                                                    |
|       nyaa.si       |       nyaa_rss        | Very Fast |         ❎          |  ✅   |   ✅    |    ✅    |                                                                                    None                                                                                    |
|       acg.rip       |        acgrip         | Moderate  |         ❎          |  ✅   |   ❎    |    ✅    |                                                                                    None                                                                                    |
|       acg.rip       |      acgrip_rss       |   Slow    |         ❎          |  ❎   |   ❎    |    ✅    | The maximum number of search pages is set to 5, as more will be blocked by the server. You can modify the `MAX_PAGE` in the module, but it is not recommended to exceed 9. |
| www.tokyotosho.info |      tokyotosho       | Moderate  |         ❎          |  ✅   |   ✅    |    ✅    |                                                                      Requires English/Japanese search                                                                      |
| www.tokyotosho.info |    tokyotosho_rss     |   Fast    |         ❎          |  ✅   |   ✅    |    ✅    |                                                                      Requires English/Japanese search                                                                      |
|   animetosho.org    |      animetosho       |   Fast    |         ❎          |  ✅   |   ✅    |    ✅    |                                                                          Requires English search                                                                           |
|   animetosho.org    |    animetosho_rss     |   Fast    |         ❎          |  ✅   |   ✅    |    ✅    |                                                                          Requires English search                                                                           |
All plugins require a proxy to work properly. Ensure that the proxy settings are correctly configured.

## Configuration Options

### Searcher Initialization Options

- `plugin_name`: Plugin name, default: 'dmhy'
- `parser`: Parser option, not required for RSS plugins, default: 'lxml'
- `verify`: Verification option, whether to verify SSL certificates, default: True
- `timefmt`: Time format, default: '%Y/%m/%d %H:%M'
- `no_search_errors`: Whether to ignore search errors, default: False

### Search Options

- `keyword`: Search keyword
- `collected`: Whether to collect results
- `proxies`: Proxy settings
- `system_proxy`: Whether to use system proxy
- `**extra_options`: Additional options, which will be merged into the query string during search

## Core Components

### Anime Class

The `Anime` class is used to represent information about a single anime resource.

#### Main Attributes

- `time`: Release time
- `title`: Title
- `size`: File size
- `magnet`: Magnet link
- `torrent`: Torrent link
- `hash`: Hash value of the magnet link, does not exist if there is no magnet link

#### Main Methods

- `size_format()`: Convert file size unit
- `set_timefmt()`: Convert time format

### Searcher Class

The `Searcher` class is the core implementation of the search functionality.

#### Main Functions

- Initialize search plugins
- Execute search operations
- Process search results
- Export data

#### Main Methods

- `search()`: Search for anime resources
- `get_anime()`: Get a single anime resource
- `get_animes()`: Get all anime resources
- `size_format_all()`: Batch convert file size units
- `save_csv()`: Save search results to a CSV file
- `set_timefmt()`: Set time format

### Error Handling

The library defines various error types:

- `PluginImportError`: Plugin import error
- `SearchRequestError`: Search request error
- `SearchParseError`: Search result parsing error
- `SizeFormatError`: File size formatting error
- `TimeFormatError`: Time formatting error
- `HashExtractError`: Magnet link hash extraction error
- `SaveCSVError`: CSV save error

## Custom Plugins

Animag supports installing custom search plugins. The plugin class must inherit from the `BasePlugin` class and
implement the `search()` method.

### Example Plugin

```python
# myplugin.py
# The file name must be the lowercase plugin name

from animag import BasePlugin, Anime
from typing import List, Optional


class MyPlugin(BasePlugin):
    abstract = False  # This line must be set, otherwise it will not be recognized as a plugin

    def __init__(self,
                 parser: Optional[str] = None,
                 verify: Optional[bool] = None,
                 timefmt: Optional[str] = None):
        # Plugin initialization
        pass

    def search(self, keyword: str,
               collected: Optional[bool] = None,
               proxies: Optional[dict] = None,
               system_proxy: Optional[bool] = None,
               **extra_options) -> List[Anime] | None:
        # Implement search logic
        pass
```

### Installing Plugins

After installing the custom plugin in the `animag/plugins` directory, specify the plugin name as `myplugin` when
initializing the searcher. If not installed in this directory, you can manually import the module into the namespace.

```python
from animag import Searcher

searcher = Searcher(plugin_name='myplugin')
```

Or directly import the plugin module:

```python
import myplugin
from animag import Searcher

searcher = Searcher(plugin_name='myplugin')
```

## Command Line Interface (CLI)

The project includes a CLI tool, implemented using the Rich library for beautiful console output, supporting interactive
selection.

### Command Line Arguments

```commandline
animag [-h] -s SEARCH [-p PLUGIN] [-c]
```

#### Required Arguments

-s, --search: Search keyword

#### Optional Arguments

- `-h`, `--help`: Show help information
- `-p`, `--plugin`: Specify search plugin (default: 'dmhy')
- `-c`, `--collected`: Enable full season search mode

### Usage Example

```commandline
# Basic search
animag -s "葬送的芙莉莲"

# Search using a specific plugin
animag -s "葬送的芙莉莲" -p nyaa

# Search for full season
animag -s "葬送的芙莉莲" -c
```

## Notes

1. The time format must comply with Python's time format string specification.
