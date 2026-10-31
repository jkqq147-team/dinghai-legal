---
title: 定海海图集接入手册 v1
description: 定海海图集的数据契约：文件结构、字段含义、App 拒绝导入的条件。
---

本文对应 manifest 格式 `1.x`（当前 `1.1`）和瓦片剖面 `1`。大版本一变，App 拒绝旧版本的海图集，按新版本重新生成（[2.4](/developers/chartset/manifest/#2.4)）。

用语：

- App 拒绝导入的条件和代码见 [6.3](/developers/chartset/self-check/#6.3)：目录与 ZIP 的结构、manifest（含 `id` 非空、不以 `s57:` 开头）、文件是否齐全、MBTiles 的 `dh_profile`。除此之外，App 导入时不检查本手册的其他要求（瓦片内容、`bounds` 是否包住数据、同一产品沿用同一 `id` 等），导入成功不等于全部瓦片都能正确显示和点选。

## 0. 速览

- 海图集是一个文件夹：`manifest.json` + `chart.mbtiles`，可选再加只有一级的概览瓦片集 `overview.mbtiles`。可导入文件夹，也可导入相同内容的 ZIP（[第 1 节](/developers/chartset/structure/)）。
- `chart.mbtiles` 是 MBTiles 1.3 矢量瓦片集：gzip 压缩的 MVT，TMS 行号，Web Mercator 网格，metadata 写 `dh_profile = 1`（[第 3 节](/developers/chartset/mbtiles/)）。
- 每个 source-layer 是一个大写 S-57 物标类缩写（可选的 `dh_coverage` 除外），属性用 S-57 属性缩写，值按 S-57 属性类型编码，深度用米（[第 4 节](/developers/chartset/tiles/)）。
- 面状物标要有可见边线时，另写一条带 `dh_boundary = 1` 的线，放在同一 source-layer（[4.3](/developers/chartset/tiles/#4.3)）。
- 最小样例与参考生成脚本见下表；自检方法见[第 6 节](/developers/chartset/self-check/)。

## 下载

| 文件 | 内容 |
| --- | --- |
| [`minimal-chartset.zip`](/developers/chartset/downloads/minimal-chartset.zip) | 最小样例海图集（[6.1](/developers/chartset/self-check/#6.1)）。 |
| [`generate-chartset-sample.py`](/developers/chartset/downloads/generate-chartset-sample.py) | 生成上述样例的参考脚本，只用 Python 标准库（[6.1](/developers/chartset/self-check/#6.1)）。 |

## 章节

1. [目录结构](/developers/chartset/structure/)：内容根、包装、多份矢量库
2. [manifest.json](/developers/chartset/manifest/)：示例、字段、id 与替换、版本规则
3. [chart.mbtiles：文件](/developers/chartset/mbtiles/)：metadata、tiles、overview.mbtiles
4. [chart.mbtiles：瓦片内容](/developers/chartset/tiles/)：坐标系与编码、图层与属性、几何、缩放级别
5. [数据清单](/developers/chartset/data/)：各物标类的几何与属性、点选报告的物标、地表类
6. [自检](/developers/chartset/self-check/)：最小样例、导入、拒绝代码、导入后的结果

附录（不属于海图集格式）：

- [附录 7. 无 manifest 的矢量 MBTiles](/developers/chartset/vector-mbtiles/)
