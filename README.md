<h1 align="center" style="font-size: 4rem">Animag 2.0</h1>

---

## 项目概述

一个用于搜索动漫磁力链接与种子的Python库，拥有强大的可扩展性。

支持通过插件系统从不同来源搜索动画资源，并能够处理磁力链接、文件大小转换等功能。

## 主要特性

- 支持多个资源站点的搜索功能
- 可扩展的插件系统
- 文件大小单位转换
- CSV导出功能
- 磁力链接处理
- 时间格式转换
- 错误处理机制

## 安装

Animag可以使用pip轻松地安装：

```commandline
pip install animag
```

## 使用示例

```python
# 导入搜索器类
from animag import Searcher

# 创建搜索器实例
searcher = Searcher(plugin_name='dmhy',
                    no_search_errors=True)

# 搜索动画(代理仅作为演示)
searcher.search("葬送的芙莉莲",
                collected=True,
                proxies={'http': 'http://localhost:6666',
                         'https': 'http://localhost:6666'})

# 打印搜索结果
print(searcher.get_animes())

"""
示例输出(2024年12月22日的结果)：

Search completed successfully: 葬送的芙莉莲
[Anime(time='2024/10/20 12:23', title='[7³ACG\u200b] \u200b葬送的芙莉莲/Sousou no Frieren S01 | 01-28 [简繁字幕] BDrip 1080p AV1 OPUS 2.0\u200b\u200b\u200b', size='17.1GB', magnet='magnet:?xt=urn:btih:...

"""

# 转换所有结果的文件大小为GB
searcher.size_format_all('MB')

# 保存结果到CSV文件
searcher.save_csv("search_results.csv")
```

## 支持的插件

|         站点          |     插件参数名称     | 速度 | 季度全集搜索 | size | magnet | torrent |                          注意事项                           |
|:-------------------:|:--------------:|:--:|:------:|:----:|:------:|:-------:|:-------------------------------------------------------:|
|      dmhy.org       |      dmhy      | 较慢 |   ✅    |  ✅   |   ✅    |    ❎    |                            无                            |
|      dmhy.org       |    dmhy_rss    | 适中 |   ✅    |  ❎   |   ✅    |    ❎    |                            无                            |
|       nyaa.si       |      nyaa      | 快  |   ❎    |  ✅   |   ✅    |    ✅    |                            无                            |
|       nyaa.si       |    nyaa_rss    | 快  |   ❎    |  ✅   |   ✅    |    ✅    |                            无                            |
|       acg.rip       |     acgrip     | 较快 |   ❎    |  ✅   |   ❎    |    ✅    |                            无                            |
|       acg.rip       |   acgrip_rss   | 快  |   ❎    |  ❎   |   ❎    |    ✅    | 设置的最大搜索页数是5页，因为多了会被服务器阻断<br/>可以自行修改模块的`MAX_PAGE`，不建议超过9 |
| www.tokyotosho.info |   tokyotosho   | 较快 |   ❎    |  ✅   |   ✅    |    ✅    |                        需要英文/日文搜索                        |
| www.tokyotosho.info | tokyotosho_rss | 快  |   ❎    |  ✅   |   ✅    |    ✅    |                        需要英文/日文搜索                        |
|   animetosho.org    |   animetosho   | 较快 |   ❎    |  ✅   |   ✅    |    ✅    |                         需要英文搜索                          |
|   animetosho.org    | animetosho_rss | 快  |   ❎    |  ✅   |   ✅    |    ✅    |                         需要英文搜索                          |

以上所有插件都需要代理才能正常工作，确保正确配置代理设置

## 配置选项

### 搜索器初始化选项

- `plugin_name`: 插件名称，默认：'dmhy'
- `parser`: 解析器选项，RSS插件无需提供，默认：'lxml'
- `verify`: 验证选项，是否验证SSL证书，默认：True
- `timefmt`: 时间格式，默认：'%Y/%m/%d %H:%M'
- `no_search_errors`: 是否忽略搜索错误，默认：False

### 搜索选项

- `keyword`: 搜索关键词
- `collected`: 是否收集结果
- `proxies`: 代理设置
- `system_proxy`: 是否使用系统代理
- `**extra_options`: 额外选项，会并入搜索时的查询字符串

## 核心组件

### Anime类

`Anime`类用于表示单个动画资源的信息

#### 主要属性

- `time`: 发布时间
- `title`: 标题
- `size`: 文件大小
- `magnet`: 磁力链接
- `torrent`: 种子链接
- `hash`: 磁力链接的哈希值，如果不存在magnet则其不存在

#### 主要方法

- `size_format()`: 转换文件大小单位
- `set_timefmt()`: 转换时间格式

### Searcher类

`Searcher`类是搜索功能的核心实现

#### 主要功能

- 初始化搜索插件
- 执行搜索操作
- 处理搜索结果
- 导出数据

#### 主要方法

- `search()`: 搜索动画资源
- `get_anime()`: 获取单个动画资源
- `get_animes()`: 获取所有动画资源
- `size_format_all()`: 批量转换文件大小单位
- `save_csv()`: 将搜索结果保存为CSV文件
- `set_timefmt()`: 设置时间格式

### 错误处理

库定义了多种错误类型：

- `PluginImportError`: 插件导入错误
- `SearchRequestError`: 搜索请求错误
- `SearchParseError`: 搜索结果解析错误
- `SizeFormatError`: 文件大小格式化错误
- `TimeFormatError`: 时间格式化错误
- `HashExtractError`: 磁力链接哈希提取错误
- `SaveCSVError`: CSV保存错误

## 自定义插件

Animag支持安装自己实现的搜索插件，插件类必须继承`BasePlugin`类，并实现`search()`方法。

### 示例插件

```python
# myplugin.py
# 文件名必须是小写的插件名称

from animag import BasePlugin, Anime
from typing import List, Optional


class MyPlugin(BasePlugin):
    abstract = False  # 这一行必须设置，否则不会被识别为插件

    def __init__(self,
                 parser: Optional[str] = None,
                 verify: Optional[bool] = None,
                 timefmt: Optional[str] = None):
        # 插件初始化
        pass

    def search(self, keyword: str,
               collected: Optional[bool] = None,
               proxies: Optional[dict] = None,
               system_proxy: Optional[bool] = None,
               **extra_options) -> List[Anime] | None:
        # 实现搜索逻辑
        pass
```

### 安装插件

将自定义插件安装到animag/plugins目录后，在搜索器初始化时，指定插件名称为`myplugin`即可，如果没有安装至此目录，也可以手动将模块导入至命名空间。

```python
from animag import Searcher

searcher = Searcher(plugin_name='myplugin')
```

或者是直接导入插件模块

```python
import myplugin
from animag import Searcher

searcher = Searcher(plugin_name='myplugin')
```

## 命令行接口 (CLI)

项目附赠了一个CLI工具，使用 Rich 库实现美观的控制台输出，支持交互式选择。

### 命令行参数

```commandline
animag [-h] -s SEARCH [-p PLUGIN] [-c]
```

#### 必选参数

-s, --search: 搜索关键词

#### 可选参数

- `-h`, `--help`: 显示帮助信息
- `-p`, `--plugin`: 指定搜索插件（默认：'dmhy'）
- `-c`, `--collected`: 启用季度全集搜索模式

### 使用示例

```commandline
# 基本搜索
animag -s "葬送的芙莉莲"

# 使用特定插件搜索
animag -s "葬送的芙莉莲" -p nyaa

# 搜索季度全集
animag -s "葬送的芙莉莲" -c
```

## 注意事项

1. 目前所有的插件都需要代理才能工作，确保正确配置代理设置
2. 时间格式必须符合Python的时间格式字符串规范