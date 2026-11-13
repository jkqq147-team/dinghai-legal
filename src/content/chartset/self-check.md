---
title: 6. 自检
description: 在真机定海 App 里导入海图集自检；导入被拒绝时按设备日志中的代码查原因和改法，导入成功后核对能看到的结果。
---

自检就是在 iPhone 或 iPad 上用定海 App 导入你生成的海图集，走与用户相同的导入路径。检查结果以你所用的 App 版本为准。

## 6.1 最小样例

[`minimal-chartset.zip`](/developers/chartset/downloads/minimal-chartset.zip) 是一个能被 App 导入的完整海图集（ZIP 约 18 KB）：旧金山湾口外一个虚构小岛，三档水深区、两条等深线、四个水深点、陆地面与岸线、一个带边线的锚地、一个左侧标浮标及其灯、一个沉船、一个带边线的禁锚区，以及锚地和禁锚区各一个区域符号点（`dh_area_symbol`），z10–z16。ZIP 里是包装目录 `minimal-chartset/`，内含 `manifest.json` 与 `chart.mbtiles`（[1.1](/developers/chartset/structure/#1.1)）。

它由参考生成脚本 [`generate-chartset-sample.py`](/developers/chartset/downloads/generate-chartset-sample.py) 生成，只需 Python 3 标准库：

```bash
python3 generate-chartset-sample.py --output /tmp/minimal-chartset
```

脚本输出是确定的：`manifest.json` 与样例逐字节相同，metadata 与每一张瓦片解压后的 MVT 也相同。不同 Python 版本写出的 gzip 头和 SQLite 文件头可能有个别字节不同，所以和样例比较时，比较 `manifest.json` 和解码后的瓦片内容，不比较文件字节。

先导入这个样例，确认你的设备和 App 版本能走通整个流程，再导入自己的海图集。

## 6.2 在 App 里导入

1. 把海图集文件夹或 ZIP 放到“文件” App 能访问的位置，例如 iCloud 云盘或“我的 iPhone”。测试 ZIP 时直接导入 ZIP，不以解压目录替代。
2. 在定海里打开“设置” › “离线海图”，点右上角的 +，选“从文件导入…”，再选择海图集文件夹或 ZIP。也可以在“文件” App 里用“共享”或“打开方式”把 ZIP 交给定海，或用隔空投送发给设备，在定海弹出的确认页点“导入”。
3. 导入成功后，海图集出现在“离线海图”列表里，名称取 manifest 的 `name`。被拒绝时，App 不弹窗，只在“离线海图”的任务行写一句原因，不显示错误码或“格式说明”链接；需要定位制作问题时，按 [6.3](#6.3) 查看设备日志。

同一 `id` 再导入会替换旧的那份（[2.3](/developers/chartset/manifest/#2.3)），可以反复改、反复导。

## 6.3 导入被拒绝时

不保证多个错误的报告次序。

错误码和英文诊断写入设备日志，不在任务行显示。用数据线将 iPhone 或 iPad 连接到 Mac，按设备提示允许连接并信任电脑；打开 Mac 的“控制台”App，在边栏选择设备，开始查看实时日志，再在定海中重现导入失败。搜索 `Offline chart job failed`，按日志方括号里的诊断或代码对照下表。

**manifest 与 MBTiles 校验失败**：日志方括号里是英文诊断，不随界面语言变化。例如缺少 `chart.mbtiles` 时，安装失败日志为 `Offline chart job failed [chart.mbtiles missing]: …`；方括号里的诊断和冒号后的错误详情均公开记录。任务行只显示“这份定海海图集无法使用，请向提供方获取新文件。”。

| 代码 | 原因 | 怎么改 |
| --- | --- | --- |
| `manifest.json unreadable: …` | 不是合法 JSON，或顶层不是对象，或 `format`、`formatVersion` 不是字符串。 | 写成 JSON 对象，这两个字段写字符串（[2.2](/developers/chartset/manifest/#2.2)）。 |
| `missing field format` | 没有 `format`。 | 写 `"format": "dinghai-chartset"`。 |
| `format is <值>, not dinghai-chartset` | `format` 写错。 | 同上。 |
| `missing field formatVersion` | 没有 `formatVersion`。 | 写 `"<大版本>.<小版本>"`，例如 `"1.1"`。 |
| `invalid field formatVersion: expected <major>.<minor>, found <值>` | `formatVersion` 不是两段整数。 | 同上。 |
| `formatVersion <值> unsupported, this App reads 1.x` | 大版本不是本 App 支持的版本。 | 按本 App 对应的手册重新生成（[2.4](/developers/chartset/manifest/#2.4)）。 |
| `tileProfile <值> unsupported, this App reads 1` | 剖面版本不受支持。 | 同上。 |
| `missing field <路径>` | 缺必需字段，路径如 `source.producer`、`bounds.west`。 | 补上该字段（[2.2](/developers/chartset/manifest/#2.2)）。 |
| `invalid field <路径>: …` | 字段类型或取值不对，例如 `tileProfile` 写成字符串 `"1"`、`converterRevision` 写成字符串；`source.type` 既不是 `external` 也不是 `s57` 时报 `invalid field source.type`。 | 按 [2.2](/developers/chartset/manifest/#2.2) 的类型改正；`source.type` 写 `external`。 |
| `invalid field : Expected date string to be ISO8601-formatted.` | `createdAt` 不是带时间和时区的 ISO 8601，例如只写了日期（此项不带字段路径）。 | 写成 `2026-09-30T12:00:00Z` 的形式。 |
| `invalid field name: empty` | `name` 是空串。 | 写显示名。 |
| `invalid field minimumZoom: zoom range …` | 缩放不在 0–24，或 `minimumZoom > maximumZoom`。 | 按实际瓦片级别改正。 |
| `invalid field overviewZoom: <值> not below maximumZoom <值>` | `overviewZoom` 不小于 `maximumZoom`，或是负数。 | 改成 `0 ≤ overviewZoom < maximumZoom`（[3.3](/developers/chartset/mbtiles/#3.3)）。 |
| `invalid field bounds: not a longitude/latitude box` | 经纬度越界、不是有限数，或 `south > north`。 | 按 [2.2](/developers/chartset/manifest/#2.2) 改正。 |
| `invalid field source.producer: empty` | `producer` 是空串。 | 写生产方与工具名称、版本。 |
| `invalid field id: empty or reserved s57: prefix` | `id` 为空，或以 `s57:` 开头。 | 换一个 `id`（[2.3](/developers/chartset/manifest/#2.3)）。 |
| `invalid field source.cells…`、`invalid field id: S-57 chart set id must be …` | `source.type` 是 `s57`，且 manifest 没通过 `s57` 的校验。 | `source.type` 写 `external`。 |
| `chart.mbtiles missing` | 内容根里没有 `chart.mbtiles`。 | 放入 `chart.mbtiles`（[第 1 节](/developers/chartset/structure/)）。 |
| `overview.mbtiles missing (manifest has overviewZoom)` | manifest 写了 `overviewZoom`，却没有 `overview.mbtiles`。 | 放入 `overview.mbtiles`，或删掉 `overviewZoom`。 |
| `<文件> is not a readable MBTiles (SQLite) file` | `chart.mbtiles` 或 `overview.mbtiles` 不是 SQLite 文件，或没有 `metadata` 表。 | 重新生成该文件（[第 3 节](/developers/chartset/mbtiles/)）。 |
| `<文件> metadata has no integer dh_profile` | metadata 没有 `dh_profile`，或它的值不是整数。 | 写 `dh_profile = 1`（[3.1](/developers/chartset/mbtiles/#3.1)）。 |
| `<文件> dh_profile <a> differs from manifest tileProfile <b>` | 两处版本不一致。 | 改成相同的值。 |

**其他代码**：查看日志方括号里的代码，例如 `Offline chart job failed [V3]:`；冒号后是错误详情。任务行不再显示“（代码 …）”。

| 代码 | 原因 | 怎么改 |
| --- | --- | --- |
| D1 | 所选或解压后的内容根不是文件夹。 | 选择文件夹或 ZIP。 |
| D2 | 所选根和下面一层都没有 `manifest.json`，也找不到 S-57 交换集或 `.mbtiles`；空 ZIP、`manifest.json` 放得比包装目录更深也是这样。 | 按[第 1 节](/developers/chartset/structure/)放 `manifest.json`。 |
| D3 | 没有 manifest 时找到的某个 `.mbtiles` 打不开，或没有可读的 `metadata`、`tiles`。 | 写好 `manifest.json` 打包成海图集，或修复该文件。 |
| D4 | 没有 manifest 时找到的某个 `.mbtiles` 既不是栅格也不是矢量瓦片。 | 同上。 |
| D5 | 没有 manifest，且同时有栅格和矢量 `.mbtiles`。 | 分别导入。 |
| D6 | 所选根下有多份海图集，或包装目录旁边还有其他项目（隐藏文件也算）。 | 分别选择各自的内容根；包装目录旁边不放其他项目（[1.1](/developers/chartset/structure/#1.1)）。 |
| D7 | 只在“从网址下载”时出现：下载内容不是 S-57 交换集。 | 定海海图集用“从文件导入…”导入。 |
| V1、V2 | 没有 manifest 的矢量 MBTiles 不符合[附录 7](/developers/chartset/vector-mbtiles/)。 | 见 [7.3](/developers/chartset/vector-mbtiles/#7.3)。 |
| V3 | 没有 manifest，却有两份或更多矢量 MBTiles。 | 见 [1.2](/developers/chartset/structure/#1.2)。 |
| Z1 | 文件里找不到 ZIP 的目录记录：不是 ZIP，或没有下载完整。 | 重新取得完整的文件。 |
| Z2 | ZIP 自身的记录互相矛盾或提前结束。 | 同上。 |
| Z3 | 某个文件的 CRC-32 不符。 | 同上。 |
| Z4 | 路径不安全或有歧义：绝对路径、`..`、重复路径、只差大小写或 Unicode 规范化的路径、同名文件与目录，或非普通文件条目。 | 只用普通文件和目录重新打包。 |
| Z5 | ZIP 加密，包括 AES。 | 不加密重新打包。 |
| Z6 | 分卷压缩的一部分。 | 打包成单个 ZIP。 |
| M&lt;n&gt; | 压缩方式 n 既不是 stored 也不是 DEFLATE。 | 用 stored 或 DEFLATE 重新打包。 |
| F1 | ZIP 文件本身打不开或读不出。 | 确认文件已完整下载到本机。 |
| F2 | 解压出的文件写不进设备。 | 确认存储空间充足。 |

**不带代码的常见拒绝**：

| 情况 | 怎么改 |
| --- | --- |
| manifest 的 `source.type` 是 `s57`，且通过了 `s57` 的校验。 | 写 `"type": "external"`（[2.2](/developers/chartset/manifest/#2.2)）。 |
| 可用空间不足以复制海图集。 | 腾出空间再导入。 |
| 复制失败，例如目录里有读不到的文件、符号链接或其他非普通文件。 | 只用普通文件和目录（[第 1 节](/developers/chartset/structure/)）。 |

## 6.4 导入成功后应该看到什么

导入后地图不会自动切换到这份海图集，要手动选中：

1. 在地图上点图层图标按钮，打开“地图”面板，选中刚导入的海图集。
2. 在“搜索坐标”里输入 `bounds` 内的一个点（最小样例用 `37.80, -122.62`），把地图移过去。
3. 放大到海图集显示出来（不浅于 `minimumZoom`），把准星移到要核对的位置，看读数。有些物标类要放得更深才画、才能读到（[4.4](/developers/chartset/tiles/#4.4)）。

最小样例在“离线海图”的安全水深与深水保持默认的 3 米、10 米时，应该看到：

- 三档水深区依次为浅水蓝、浅青蓝、白色；小岛是陆地色，岸线、等深线是细线；这些从样例最浅的 10 级起就有。
- 11 级起有水深数字；浮标与灯的符号 11.5 起淡入，12 级起完全显示；13 级起有等深线数值。在这之前都不画（[4.4](/developers/chartset/tiles/#4.4)）；浅于 11.5 时，灯只显示为绿色圆点。
- 锚地（东南角）和禁锚区（西北角）都只有品红虚线边界，内部不填色（边界来自 `dh_boundary` 线）。10.5 级起淡入、11 级起完全显示各自的区域符号：锚地是 `anchorage`，禁锚区是 `noAnchoring`（来自 `dh_area_symbol` 点，各在区域正中）。符号的点被先放下的文字占住时（例如 13 级起显示的锚地名称），符号画在紧挨的位置上（[4.2](/developers/chartset/tiles/#4.2)）。
- 把准星移进禁锚区（例如 `37.808534, -122.635916`），核对读数为“禁止锚泊　10–20米”。
- 沉船位于 `37.803144, -122.628527`，12 级起各级准星读数都是“Sample Wreck · 6.5米”。它在 3 米安全水深下不是孤立危险物，符号 11.5 起才淡入，更浅时不画、读不到（[4.4](/developers/chartset/tiles/#4.4)）。
- 水面 `37.799100, -122.625684` 放大后读数为“0–5米”；小岛内不显示水深。
- 样例覆盖范围外显示定海底图，不是这份海图集提供的内容。

App 导入时不检查瓦片内容，所以“导入成功，但地图上看不到 / 点选读不到”时按下表查：

| 现象 | 常见原因 |
| --- | --- |
| 整片都没有 | `tile_row` 写成了 XYZ 行号（应为 TMS，[3.2](/developers/chartset/mbtiles/#3.2)）；瓦片不是可解码的 MVT；metadata `minzoom`/`maxzoom` 与 manifest 不一致；当前缩放浅于 `minimumZoom`。 |
| 放大过 `overviewZoom` 后某片变空白 | `chart.mbtiles` 深级别不写那里的数据，`overview.mbtiles` 也没补上（[3.3](/developers/chartset/mbtiles/#3.3)）。 |
| 放大过 `overviewZoom` 后两套叠在一起或有细缝 | 概览没有按深级别的覆盖范围裁切，或裁切线又被简化（[3.3](/developers/chartset/mbtiles/#3.3)）。 |
| 某一类没有 | 当前缩放浅于 [4.4](/developers/chartset/tiles/#4.4) 表中该类的显示级别；source-layer 名不是大写 S-57 缩写；几何类型不对，例如航标写成线或面、面的边线没带 `dh_boundary`（[5.1](/developers/chartset/data/#5.1)）。 |
| 水深区颜色不对 / 没有水深数字 | `DRVAL1`/`DRVAL2`/`DEPTH` 不是数值，或单位不是米；`SOUNDG` 没拆成单点；当前缩放浅于 11 级（[4.4](/developers/chartset/tiles/#4.4)）。 |
| 符号是通用形状 | 选符号的属性缺失或值不对（[5.1](/developers/chartset/data/#5.1)），列表属性没有写成逗号串。 |
| 限制区等区域没有区域符号，或比写入的点少 | 没有 `dh_area_symbol` 层；`dh_symbol` 缺失或不是 [4.2](/developers/chartset/tiles/#4.2) 列出的值；当前缩放浅于 10.5 级或该点的 `dh_minzoom`；这一级的瓦片没写这个点；点和周围八个位置都与已放下的文字或其他区域符号相碰（[4.2](/developers/chartset/tiles/#4.2)）。 |
| 某些缩放级别点选读不到 | 浅于 [4.4](/developers/chartset/tiles/#4.4) 所列的显示级别时，该类物标本来就不显示、也点选不到；或该物标只写进了部分级别（[4.4](/developers/chartset/tiles/#4.4)）。 |
| 详情少了属性 | 属性名不是 S-57 目录里的缩写，或只写在了部分缩放级别（[5.2](/developers/chartset/data/#5.2)）。 |

## 6.5 没有命令行校验器

定海不提供不启动 App 的离线校验命令，[6.2](#6.2) 的导入路径就是校验。只想快速看版本号是否一致时，可以用 `sqlite3`：

```bash
sqlite3 chart.mbtiles "SELECT name, value FROM metadata WHERE name IN ('dh_profile','minzoom','maxzoom','bounds');"
```
