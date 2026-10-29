---
title: 3. chart.mbtiles：文件
description: chart.mbtiles 与 overview.mbtiles 的 metadata 与 tiles 表。
---

`chart.mbtiles` 是 SQLite 数据库，遵循 MBTiles 1.3。

## 3.1 metadata

| 键 | 值 | 要求 |
| --- | --- | --- |
| `dh_profile` | `1` | **App 校验**：存在、是整数、等于 manifest 的 `tileProfile`。 |
| `minzoom`、`maxzoom` | 整数 | 要求：等于 manifest 的 `minimumZoom`、`maximumZoom`。地图用的 MapLibre 从这里读缩放范围。 |
| `bounds` | `west,south,east,north` | 建议与 manifest 的 `bounds` 一致。App 不比较两者；当前 MapLibre 对 `pbf` 用它推导中心，点选范围取 manifest（[2.2](/developers/chartset/manifest/#2.2)），两者相等不是画图或点选的必要条件。 |
| `format` | `pbf` | MBTiles 1.3 必需。 |
| `json` | `{"vector_layers":[…]}` | [MBTiles 1.3](https://github.com/mapbox/mbtiles-spec/blob/master/1.3/spec.md) 对矢量瓦片必需：每个 source-layer 一项，必需键（MUST）只有 `id` 与 `fields`（字段名 → `String`、`Number` 或 `Boolean`）；每层的 `minzoom`、`maxzoom` 为可选（MAY）。App 不校验这份图层清单。 |
| `name`、`type`（`overlay`）、`version`、`scheme`（`tms`）、`center` | | 按 MBTiles 1.3 填写，App 不读。 |

## 3.2 tiles

- `tiles` 可以是表，也可以是视图，列为 `zoom_level`、`tile_column`、`tile_row`、`tile_data`。
- `tile_row` 是 **TMS 行号**（南边为 0）：`tile_row = 2^zoom − 1 − y`，`y` 是常见的 XYZ（北边为 0）行号。
- `(zoom_level, tile_column, tile_row)` 单张查询应能快速命中，`tiles` 是视图时也一样。填齐 `minzoom`／`maxzoom`，避免消费者为推导范围扫描瓦片。
- 没有内容的瓦片不必写。
- App 校验只打开 `metadata`；瓦片内容是否齐全、能否解码，导入时都不检查（[第 6.4 节](/developers/chartset/self-check/#6.4)）。

## 3.3 overview.mbtiles（可选）

大范围、小比例尺的数据（例如 S-57 用途带 1–3）放大到深缩放级别时几乎都是整片相同的水深区，按 `chart.mbtiles` 的规则一级一级写到 `maximumZoom`，会占去海图集的大部分体积。概览瓦片集让这部分数据只写一级：

- 文件结构、metadata、瓦片编码与 `chart.mbtiles` 相同（[3.1](/developers/chartset/mbtiles/#3.1)、[3.2](/developers/chartset/mbtiles/#3.2)、[第 4 节](/developers/chartset/tiles/)），`dh_profile` 与 manifest 的 `tileProfile` 相同（**App 校验**），metadata `minzoom` 和 `maxzoom` 都等于 manifest 的 `overviewZoom`，只有这一级的瓦片。
- 地图缩放 `z` 满足 `⌊z⌋ > overviewZoom` 时，App 把这一级放大画在 `chart.mbtiles` 同类图层之下；`⌊z⌋ ≤ overviewZoom` 时不画它。点选在读到的 `chart.mbtiles` 级别深于 `overviewZoom` 时，也读这一级，同一物标（4.1 的 source-layer + id）只报告一次，通常保留先查询的 `chart.mbtiles` 要素；派生边线先到、同 id 面后到时仍按 4.1 的例外替换。
- 内容规则：它装的是 **`chart.mbtiles` 在深于 `overviewZoom` 的级别有意不写、但这些级别本该显示或点选得到的物标**，按深级别的合成结果裁好：
  - `chart.mbtiles` 深于 `overviewZoom` 的每一级，与 `overview.mbtiles` 放大到该级后，**不重叠、不留缝**：同一处只有一套数据（[4.4](/developers/chartset/tiles/#4.4)）。例如深级别由大比例尺数据覆盖的地方，概览里的小比例尺数据要裁掉；没有大比例尺数据的地方，深级别 `chart.mbtiles` 不写小比例尺数据，由概览补上。
  - 裁切线只能精确到 `overviewZoom` 的网格（`extent` 4096 时，北纬 38° z12 约 1.88 米一格）。放大后的接缝误差就是这个量级，生产方应让裁切线按未简化的轮廓吸附到该网格，不要再简化。
  - 地图上不画、只供点选的大面积物标（例如 `MAGVAR`），也可以只写到 `overviewZoom` 再放进概览，深级别点选照样读得到。
- `chart.mbtiles` 在 `overviewZoom` 及以浅各级仍要写齐全部数据：这些级别 App 不画也不读概览瓦片集。
