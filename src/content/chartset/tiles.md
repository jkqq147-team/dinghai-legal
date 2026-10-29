---
title: 4. chart.mbtiles：瓦片内容
description: 瓦片的坐标系与编码、图层与属性、几何、缩放级别与用途带。
---

## 4.1 坐标系与编码

- 瓦片网格：Web Mercator（EPSG:3857）的标准 `z/x/y` 四叉树。坐标由 WGS84 经纬度投影而来。
- 编码：Mapbox Vector Tile 2.1（protobuf），每张瓦片用 gzip 压缩后写入 `tile_data`。
- `extent` 建议 `4096`，四周缓冲建议 `80` 个单位，几何裁到瓦片加缓冲范围。
- 面：外环在瓦片坐标（y 向下）中面积为正（顺时针），内环（洞）为负，遵循 MVT 2.1。
- 要素 id（MVT feature id）可选。写了的话，**同一 source-layer 里不同物标的 id 应当在整个海图集内唯一，至少在相邻瓦片与 overview 之间唯一**，不要逐瓦片从 1 重新编号：同一 source-layer 里 id 相同的要素，一次点选只报告一个。
  - 面和由它派生的边线（`dh_boundary = 1`，[4.3](/developers/chartset/tiles/#4.3)）可以共用一个 id。
  - 拆开的水深点（`SOUNDG`）不得共用 id：各用不同的 id，或都不写 feature id。

## 4.2 图层与属性

- **source-layer 名必须是大写的 S-57 物标类缩写**，与 IHO S-57 物标目录完全一致（例如 `DEPARE`、`LIGHTS`）；唯一的例外是可选的 `dh_coverage`（下一条）。目录外的层名不画，也不报告。
- **覆盖边界线 `dh_coverage`**（可选）：整个海图集数据覆盖范围的外边界，闭合的 LineString/MultiLineString，不带属性；内部各来源之间的接缝不写。
- **属性名 = S-57 属性缩写**，大写；定海派生字段除外（见下文）。属性值按 S-57 属性类型编码：

  | S-57 类型 | 瓦片中的值 | 例 |
  | --- | --- | --- |
  | E（枚举）、I（整数） | 整数 | `CATWRK: 2`、`WATLEV: 3` |
  | F（浮点） | 浮点 | `DRVAL1: 5.0`、`VALSOU: 6.5` |
  | L（列表） | 逗号分隔的字符串 | `COLOUR: "3,4,3"`；单值也写成字符串 `"4"` |
  | A、S（文本） | 字符串 | `OBJNAM: "Sample 1"`、`SIGGRP: "(1)"` |

  “值未知”的属性不要写（不要写空串或 0）。
- **深度一律米**：`DRVAL1`、`DRVAL2`、`VALDCO`、`VALSOU`、`DEPTH` 都是米制，正值向下，负值是干出高度。
- **定海派生字段**用 `dh_` 前缀；例外是 `SOUNDG` 的 `DEPTH`（[5.1](/developers/chartset/data/#5.1) A 组）。

  | 字段 | 值 | 含义 |
  | --- | --- | --- |
  | `dh_boundary` | 整数 `1` | 这条线是同层面状物标的可见边线（[4.3](/developers/chartset/tiles/#4.3)）。 |
  | `dh_drval1` | 浮点，米，可选 | 只在点状 `UWTROC`、`WRECKS`、`OBSTRN` 上：同一单元里包含或接触该点的 `DEPARE`、`DRGARE` 中最大的 `DRVAL1`，没有 `DRVAL1` 的水深区按 −1 计；没有这样的水深区就不写。 |
  | `dh_prev_valdco` | 浮点，米，可选 | 只在带 `VALDCO` 的 `DEPCNT` 上：同一单元里比它浅的 `DEPCNT` 中最大的 `VALDCO`，写 `max(更浅值, 0)`；没有更浅的写 `0`。 |
  | `dh_surface_cell` | 字符串，可选 | 数据的来源单元名。 |
  | `dh_surface_cscl` | 整数，可选 | 来源单元的编辑比例尺分母；与非空的 `dh_surface_cell` 一起提供时使用。 |

## 4.3 几何

| 几何 | MVT 类型 | 用于 |
| --- | --- | --- |
| 点 | Point | 点物标、水深点。航标类规范要求单点 Point（[5.1](/developers/chartset/data/#5.1) D 组）。 |
| 线 | LineString / MultiLineString，**不带** `dh_boundary` | 线物标：等深线、岸线、电缆、航线等。 |
| 面 | Polygon / MultiPolygon | 面物标。面本身没有可见边线。 |
| 边线 | LineString，带 `dh_boundary = 1` 和该物标的全部属性，放在**同一个** source-layer | 面状物标的可见边线。 |

边线单独写，是为了让单元接缝、被遮罩的边、只沿数据界限的边都不出现：生产方只写真正应该看见的那几段。不写边线，那个面就没有可见边界。

## 4.4 缩放级别与用途带

- 每一级显示和点选读的都是这一级（深于 `maxzoom` 时是最深一级）的瓦片，有概览瓦片集时另加 [3.3](/developers/chartset/mbtiles/#3.3) 的概览。所以**一个物标在它出现的每个缩放级别都要带齐[第 5 节](/developers/chartset/data/)要求的属性**，只放在最深一级不够。建议在 `minzoom`–`maxzoom` 之间凡有数据处都写；某一级不写某个物标，在那一级就点选不到它。
- 用途带（S-57 INTU，1 概览 … 6 靠泊）不是瓦片字段。生产方自行决定每个缩放级别用哪个比例尺的数据，原则是**同一级别、同一位置只放一套数据**：两套重叠时两套都会显示，点选也可能报告两套。有概览瓦片集时，`chart.mbtiles` 与放大后的 `overview.mbtiles` 合起来算（[3.3](/developers/chartset/mbtiles/#3.3)）。
