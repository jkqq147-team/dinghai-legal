---
title: 3. chart.mbtiles：文件
description: chart.mbtiles 与 overview.mbtiles 的 metadata 与 tiles 表。
---

`chart.mbtiles` 是 SQLite 数据库，遵循 MBTiles 1.3。

## 3.1 metadata

| 键 | 值 | 要求 |
| --- | --- | --- |
| `dh_profile` | `1` | 必需，整数，等于 manifest 的 `tileProfile`；导入时检查。 |
| `minzoom`、`maxzoom` | 整数 | 等于 manifest 的 `minimumZoom`、`maximumZoom`。 |
| `bounds` | `west,south,east,north` | 建议与 manifest 的 `bounds` 一致。 |
| `format` | `pbf` | MBTiles 1.3 必需。 |
| `json` | `{"vector_layers":[…]}` | [MBTiles 1.3](https://github.com/mapbox/mbtiles-spec/blob/master/1.3/spec.md) 对矢量瓦片必需：每个 source-layer 一项，必需键只有 `id` 与 `fields`（字段名 → `String`、`Number` 或 `Boolean`）；每层的 `minzoom`、`maxzoom` 可选。 |
| `name`、`type`（`overlay`）、`version`、`scheme`（`tms`）、`center` | | 按 MBTiles 1.3 填写。 |

## 3.2 tiles

- `tiles` 可以是表，也可以是视图，列为 `zoom_level`、`tile_column`、`tile_row`、`tile_data`。
- `tile_row` 是 **TMS 行号**（南边为 0）：`tile_row = 2^zoom − 1 − y`，`y` 是常见的 XYZ（北边为 0）行号。
- `(zoom_level, tile_column, tile_row)` 单张查询应能快速命中，`tiles` 是视图时也一样。
- 没有内容的瓦片不必写。
- 导入时只读 `metadata`，瓦片内容是否齐全、能否解码都不检查（[6.4](/developers/chartset/self-check/#6.4)）。

## 3.3 overview.mbtiles（可选）

大范围、小比例尺的数据（例如 S-57 用途带 1–3）一级一级写到 `maximumZoom`，会占去海图集的大部分体积。概览瓦片集让这部分数据只写一级：

- 文件结构、metadata、瓦片编码与 `chart.mbtiles` 相同（[3.1](/developers/chartset/mbtiles/#3.1)、[3.2](/developers/chartset/mbtiles/#3.2)、[第 4 节](/developers/chartset/tiles/)）；`dh_profile` 等于 manifest 的 `tileProfile`（导入时检查）；metadata `minzoom` 和 `maxzoom` 都等于 manifest 的 `overviewZoom`，只有这一级的瓦片。
- 深于 `overviewZoom` 的每一级，App 读的是 `chart.mbtiles` 的这一级加上放大到这一级的 `overview.mbtiles`；`overviewZoom` 及以浅各级只读 `chart.mbtiles`，这些级别要写齐全部数据。
- 内容：`chart.mbtiles` 在深于 `overviewZoom` 的级别有意不写、但这些级别本该有的物标，按深级别的合成结果裁好。
  - **不重叠、不留缝**：`chart.mbtiles` 深于 `overviewZoom` 的每一级，与放大到该级的 `overview.mbtiles` 合起来，同一处只有一套数据（[4.4](/developers/chartset/tiles/#4.4)）。例如深级别由大比例尺数据覆盖的地方，概览里的小比例尺数据要裁掉；没有大比例尺数据的地方，深级别 `chart.mbtiles` 不写小比例尺数据，由概览补上。
  - 裁切线只能精确到 `overviewZoom` 的网格（`extent` 4096 时，北纬 38° z12 约 1.88 米一格）。生产方应让裁切线按未简化的轮廓吸附到该网格，不要再简化。
