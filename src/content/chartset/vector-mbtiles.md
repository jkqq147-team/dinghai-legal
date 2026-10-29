---
title: 附录 7. 无 manifest 的矢量 MBTiles
description: 附录，不属于海图集格式：没有 manifest 的单份矢量 MBTiles 怎样被识别、校验和规范化，以及 V1–V3。
---

**本附录不属于海图集格式。** 定海海图集按第 1–6 节打包；本附录只说明 App 还接受的另一种本地输入：文件夹或 ZIP 里只有一份矢量 MBTiles、没有 `manifest.json`。App 先校验并规范化成海图集，再安装。有多份矢量库时见 [1.2](/developers/chartset/structure/#1.2)。

## 7.1 识别与四项必要信息

接收两类输入：没有 manifest 的 `dh_profile=1` 瓦片集，以及用大写 S-57 物标类和属性的公开 MVT 剖面（本文称 `s57-acronym-mvt-v1`）。识别看实际 MVT 图层和属性，不看品牌、producer、generator 或文件名。有要素的图层中有任何一个不是 S-57 物标类（`dh_coverage` 除外）时整包拒绝；OpenMapTiles、Shortbread、Protomaps 等底图不从这个入口安装。

格式方面，以下任一项不满足即拒绝（V1）：metadata `format` 是矢量瓦片编码（例如 `pbf`）；写了 `dh_profile` 时等于 `1`；写了 `scheme` 时是 `tms`；写了 `projection` 时是 `EPSG:3857` 或 `3857`（不分大小写）；每层的 MVT 版本是 2；瓦片地址在 0–24 级的 Web Mercator/TMS 网格内；数据不跨 180° 经线、不越出经度范围。

除格式外只校验四项必要信息：

| 必要信息 | 规则 |
| --- | --- |
| 水深区范围 | 每个 `DEPARE` 面都有可读的 `DRVAL1`、`DRVAL2`，每个 `DRGARE` 面都有可读的 `DRVAL1`；空串按缺失处理。`DEPARE`、`DRGARE` 层里只有面和 `dh_boundary = 1` 的边线。上下限不能颠倒。整包至少有一个可读的水深区。 |
| 逐点测深 | 存在的每个 `SOUNDG` 必须是独立点并带可读的 `DEPTH`。 |
| 深度单位 | `dh_profile=1` 按米制。公开剖面以 `M_UNIT` 面中 `DUNITS=1` 的范围确认米制，须覆盖相应深度几何；非米制范围与深度几何重叠，或 `M_UNIT` 的单位或范围读不出，都拒绝。 |
| 可见面的边线 | 不校验。公开剖面的限制区、航道等面，由 App 从面环生成同层 `dh_boundary=1` 的边线，替换输入里的边线；`dh_profile=1` 的边线原样保留。 |

缺少物标种类（浮标、陆地、灯标、测深点或限制区）不拒绝。可选信息缺失或读不出（例如 `dh_prev_valdco`、`dh_drval1`、来源单元）不拒绝，在导入确认页列出。

依据：[MBTiles 1.3](https://github.com/mapbox/mbtiles-spec/blob/master/1.3/spec.md)、[MVT 2.1](https://github.com/mapbox/vector-tile-spec/tree/master/2.1)、S-57 3.1 物标／属性目录，以及 [GDAL S-57 driver](https://gdal.org/en/stable/drivers/vector/s57.html) 的类名分层、拆点与 DEPTH、列表表达。

## 7.2 一次单向规范化

- 安装前只转换一次，不修改原文件。输出是一个海图集：`manifest.json`（`external`、`tileProfile 1`）、`chart.mbtiles`（`dh_profile=1`、gzip MVT、TMS）和 `vector-import.json`（识别结果与缺少的可选信息）。
- 规范化通过后显示“导入矢量瓦片”确认页；点“取消”不安装。
- 输出的缩放与范围来自实际数据；`id` 取输入内容的指纹，同样的内容再导入替换前一次导入（[2.3](/developers/chartset/manifest/#2.3)）；`createdAt` 是本次生成时间，不是测绘日期。
- 识别通过不是海图真实、完整、最新或航行安全的认证。

## 7.3 按处理办法分错误码

| 代码 | 情况 | 怎么改 |
| --- | --- | --- |
| V1 | 格式不受支持、实际图层无法识别，或四项必要信息不足（[7.1](#7.1)）；原因写明没通过的那一项。 | 向提供方索取 S-57 交换集或定海海图集。补一个 manifest 不能绕过缺项。 |
| V2 | SQLite 数据库、表、metadata 或瓦片内容无法读取，例如 MVT 无法解码。 | 确认文件完整，或请提供方重新导出。 |
| V3 | 没有 manifest，却有两份或更多矢量 MBTiles。 | 见 [1.2](/developers/chartset/structure/#1.2)。 |
