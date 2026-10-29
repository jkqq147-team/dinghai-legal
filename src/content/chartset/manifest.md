---
title: 2. manifest.json
description: manifest.json 的示例、字段、id 与替换规则和版本规则。
---

UTF-8 编码的 JSON 对象。App 不认识的字段一律忽略。

## 2.1 示例

最小样例（[`minimal-chartset.zip`](/developers/chartset/downloads/minimal-chartset.zip)）的 manifest。`source.producer` 写生产方自己的工具名称和版本：

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

除 `overviewZoom`、`converterRevision` 外，表中字段都必需。

| 字段 | 类型 | 规则 |
| --- | --- | --- |
| `format` | 字符串 | 固定为 `dinghai-chartset`。 |
| `formatVersion` | 字符串 | `"<大版本>.<小版本>"`，两段都是整数（[2.4](/developers/chartset/manifest/#2.4)）。 |
| `converterRevision` | 整数，可选 | 若提供必须是整数；写成字符串（例如 `"15"`）会被拒绝。 |
| `tileProfile` | 整数 | 瓦片剖面版本，等于 `chart.mbtiles` metadata 的 `dh_profile`。当前为 `1`。 |
| `id` | 字符串 | 海图集的逻辑身份（[2.3](/developers/chartset/manifest/#2.3)）。非空，不得以 `s57:` 开头。 |
| `name` | 字符串 | 显示名，非空。 |
| `source` | 对象 | `{"type": "external", "producer": "<生产方与工具名称、版本>"}`；`producer` 非空。 |
| `bounds` | 对象 | `west`、`south`、`east`、`north`：数据覆盖范围的外包框，WGS84 经纬度（度）。经度在 −180…180，纬度在 −90…90，`south ≤ north`。另需 `west ≤ east`。 |
| `minimumZoom`、`maximumZoom` | 整数 | `chart.mbtiles` 实际有瓦片的最浅、最深缩放级别，0–24，`minimumZoom ≤ maximumZoom`，与 metadata 的 `minzoom`、`maxzoom` 相同。 |
| `overviewZoom` | 整数，可选（格式 1.1 起） | `overview.mbtiles` 唯一的那一级，`0 ≤ overviewZoom < maximumZoom`。写了就必须有 `overview.mbtiles`；不写就没有概览瓦片集（[3.3](/developers/chartset/mbtiles/#3.3)）。 |
| `createdAt` | 字符串 | 生成时间，ISO 8601 日期加时间和时区，推荐 UTC，例如 `2026-09-30T12:00:00Z`。 |

这几个字段决定 App 读哪些数据：

- 点选只在准星落在 `bounds` 之内时读这份海图集；`bounds` 画小了，边上的物标和水深点选读不到。
- 浅于 `minimumZoom` 时不显示这份海图集；深于 `maximumZoom` 时放大最深一级显示和点选，不必为放大另写更深的级别。

## 2.3 id 与替换

导入的海图集与已安装的某份海图集 `id` 相同时，整体替换那一份；不与其他海图集拼合。

- 同一产品的新版本沿用同一 `id`；不同产品用不同 `id`。
- 建议用生产方域名加产品名，例如 `example.org:sf-bay`。

## 2.4 版本规则

- `formatVersion` 的大版本与 `tileProfile` 都是不兼容版本号。App 只读取自己支持的大版本（当前 manifest 大版本 `1`、剖面 `1`），其他版本直接拒绝。大版本一变，按旧版本生产的海图集不能再导入，也不能再打开，要按新版本的手册重新生成。
- 只新增可选字段的改动升小版本。App 读取同一大版本的任何小版本。
- `1.1` 新增可选的 `overviewZoom` 与 `overview.mbtiles`（[3.3](/developers/chartset/mbtiles/#3.3)）。不用概览瓦片集时写 `1.0` 或 `1.1` 都可以。
