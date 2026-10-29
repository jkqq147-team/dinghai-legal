---
title: 2. manifest.json
description: manifest.json 的示例、字段、id 与替换规则和版本规则。
---

UTF-8 编码的 JSON 对象。App 不认识的字段一律忽略。

## 2.1 示例

最小样例（[`minimal-chartset.zip`](/developers/chartset/downloads/minimal-chartset.zip)）的 manifest。`source.producer` 是参考生成脚本的名称和版本，生产方写自己的工具名称和版本：

```json
{
  "format": "dinghai-chartset",
  "formatVersion": "1.0",
  "tileProfile": 1,
  "id": "example.org:minimal-sample",
  "name": "最小样例海图集",
  "source": {
    "type": "external",
    "producer": "scripts/generate-chartset-sample.py 1"
  },
  "minimumZoom": 10,
  "maximumZoom": 16,
  "createdAt": "2026-10-01T00:00:00Z",
  "bounds": {
    "west": -122.640464,
    "south": 37.788322,
    "east": -122.599536,
    "north": 37.811678
  }
}
```

## 2.2 字段

除 `overviewZoom`、`converterRevision` 外，表中所有字段都必需。

| 字段 | 类型 | 规则 |
| --- | --- | --- |
| `format` | 字符串 | 固定为 `dinghai-chartset`。 |
| `formatVersion` | 字符串 | `"<大版本>.<小版本>"`，两段都是整数。当前为 `"1.1"`；不用概览瓦片集时仍可写 `"1.0"`（[2.4](/developers/chartset/manifest/#2.4)）。 |
| `tileProfile` | 整数 | `chart.mbtiles` 遵循的瓦片剖面版本，等于其 metadata `dh_profile`。当前为 `1`。 |
| `converterRevision` | 整数，可选 | `external` 来源无需提供，取值不参与判定；若提供必须是整数，字符串（例如 `"15"`）会被拒绝。 |
| `id` | 字符串 | 海图集的逻辑身份，见 [2.3](/developers/chartset/manifest/#2.3)。非空，不得以 `s57:` 开头。 |
| `name` | 字符串 | 显示名，非空。 |
| `source` | 对象 | `{"type": "external", "producer": "<生产方与工具名称、版本>"}`；`producer` 非空，便于排查问题。`type` 的另一个取值 `s57` 只由 App 自己转换 S-57 时写出，生产方不得使用。 |
| `bounds` | 对象 | `west`、`south`、`east`、`north`：数据覆盖范围的外包框，WGS84 经纬度（度）。经度在 −180…180，纬度在 −90…90，`south ≤ north`。另需 `west ≤ east`（App 不检查，但不跨 180° 经线的外包框才能正确参与点选）。 |
| `minimumZoom`、`maximumZoom` | 整数 | `chart.mbtiles` 实际有瓦片的最浅、最深缩放级别，0–24，`minimumZoom ≤ maximumZoom`，与 metadata 的 `minzoom`/`maxzoom` 相同。 |
| `overviewZoom` | 整数，可选（格式 1.1 起） | `overview.mbtiles` 唯一的那一级，`0 ≤ overviewZoom < maximumZoom`。写了就必须有 `overview.mbtiles`；不写就没有概览瓦片集，App 不读这个文件。见 [3.3](/developers/chartset/mbtiles/#3.3)。 |
| `createdAt` | 字符串 | 生成时间，ISO 8601 日期加时间和时区，推荐 UTC，例如 `2026-09-30T12:00:00Z`。只有日期（`2026-09-30`）会被拒绝。 |

`bounds`、`minimumZoom`、`maximumZoom` 不只是说明：

- 点选只在准星落在 `bounds` 之内时读这份海图集；`bounds` 画小了，边上的物标和水深点选读不到。
- 地图的数据源缩放范围取 `minimumZoom`–`maximumZoom`。浅于 `minimumZoom` 时这份海图不显示；深于 `maximumZoom` 时由 MapLibre 放大最深一级显示（overzoom），不必为放大另写更深的级别。点选读的级别同样夹在这个范围内。
- 有 `overviewZoom` 时，地图缩放深于它（`⌊z⌋ > overviewZoom`）时另把 `overview.mbtiles` 的那一级放大画在 `chart.mbtiles` 之下，点选也同时读它（[3.3](/developers/chartset/mbtiles/#3.3)）。

## 2.3 id 与替换

同一 `id` 的导入整体替换可读的已安装海图集，原来选中它时保持选中；不与其他海图集做单元拼图。

- 不可读的旧条目不参与同 `id` 的替换。
- 同一产品的新版本沿用同一 `id`；不同产品用不同 `id`。
- 建议用生产方域名加产品名，例如 `example.org:sf-bay`。

## 2.4 版本规则

- `formatVersion` 的大版本与 `tileProfile` 都是不兼容版本号。App 只读取自己支持的大版本（当前 manifest 大版本 `1`、剖面 `1`），其他版本**直接拒绝**，不做兼容转换。大版本一变，按旧版本生产的海图集不能再导入，也不能再打开，生产方要按新版本的手册重新生成。
- 只新增可选字段的改动升小版本（例如 `1.1`）。App 读取同一大版本的任何小版本，忽略自己不认识的字段。
- `1.1` 新增可选的 `overviewZoom` 与 `overview.mbtiles`（[3.3](/developers/chartset/mbtiles/#3.3)）。不用概览瓦片集的生产方照旧写 `1.0` 或 `1.1` 都可以。
- `formatVersion` 先于其他字段检查：大版本不受支持时，App 报告的是版本不受支持，而不是缺了某个字段。
