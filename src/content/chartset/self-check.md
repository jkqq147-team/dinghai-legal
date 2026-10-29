---
title: 6. 自检
description: 在真机定海 App 里导入海图集自检；导入被拒绝时按报错对照原因，导入成功后核对应该看到的结果。
---

自检用的就是用户手里的定海 App：在 iPhone 或 iPad 上导入你生成的海图集，走与用户相同的导入路径。App 的校验就是导入路径本身，检查结果以你所用的 App 版本为准。

## 6.1 最小样例

[`minimal-chartset.zip`](/developers/chartset/downloads/minimal-chartset.zip) 是一个能被 App 导入的完整海图集（ZIP 约 17 KB，内含约 45 KB 的 `chart.mbtiles`）：旧金山湾口外一个虚构小岛，三档水深区、两条等深线、四个水深点、陆地面与岸线、一个带边线的锚地、一个左侧标浮标及其灯、一个沉船，z10–z16。ZIP 里是包装目录 `minimal-chartset/`，内含 `manifest.json` 与 `chart.mbtiles`（[1.1](/developers/chartset/structure/#1.1)）。

它由参考生成脚本 [`generate-chartset-sample.py`](/developers/chartset/downloads/generate-chartset-sample.py) 生成，只需 Python 3 标准库：

```bash
python3 generate-chartset-sample.py --output /tmp/minimal-chartset
```

脚本输出是确定的：生成的 `manifest.json` 与样例逐字节相同，`chart.mbtiles` 的 metadata 与每一张瓦片解压后的 MVT 也相同。不同 Python 版本写出的文件可能有个别字节不同：瓦片 gzip 头里的一个字节（OS 字段），以及 SQLite 文件头里记录的 SQLite 库版本号。所以和样例比较时，比较 `manifest.json` 和解码后的瓦片内容，不比较文件字节。

先导入这个样例，确认你的设备和 App 版本能走通整个流程，再导入自己的海图集。

## 6.2 在 App 里导入

1. 把海图集目录或 ZIP 放到设备上“文件” App 能访问的位置，例如 iCloud 云盘或“我的 iPhone”。测试 ZIP 时直接导入 ZIP，不以解压目录替代。
2. 在定海里打开“设置” › “离线海图”，点右上角的 +（添加海图），选“从文件导入…”，再选择海图集目录或 ZIP。也可以在“文件” App 里用“共享”或“打开方式”把 ZIP 交给定海，或用隔空投送发给设备，在定海弹出的确认页点“导入”。
3. 导入成功后，海图集出现在“离线海图”列表里，名称取 manifest 的 `name`。被拒绝时，App 弹出“无法使用这个离线海图”并给出原因，按 [6.3](#6.3) 对照。

- 同一 `id` 再导入会按 [2.3](/developers/chartset/manifest/#2.3) 替换可读的旧条目，可以反复改、反复导。
- 导入不会选中这份海图集，也不会移动地图；核对显示效果的步骤见 [6.4](#6.4)。
- 手册里的 App 提示按中文界面书写，其他语言界面下的措辞可能不同。方括号里的内容和“（代码 …）”中的代码不随语言变化。

## 6.3 导入被拒绝时

清单或 MBTiles 校验失败时，提示“这不是可用的定海海图集。”并附方括号原因，目录与 ZIP 一致。下表供生产方排错，不保证多个错误的报告次序；导入只检查声明、manifest 与 MBTiles 剖面，不认证全部瓦片。

| 方括号里的内容 | 原因与处理 |
| --- | --- |
| `manifest.json unreadable: …` | 不是合法 JSON，或顶层不是对象，或 `format`/`formatVersion` 不是字符串。 |
| `missing field format` | 没有 `format`。 |
| `format is <值>, not dinghai-chartset` | `format` 写错。 |
| `missing field formatVersion` | 没有 `formatVersion`。 |
| `invalid field formatVersion: expected <major>.<minor>, found <值>` | `formatVersion` 不是 `"整数.整数"`。写成数字 `1.0` 而不是字符串时报 `manifest.json unreadable: … Expected value of type String. Path: formatVersion …`。 |
| `formatVersion <值> unsupported, this App reads 1.x` | 大版本不是本 App 支持的版本：按本 App 对应的手册重新生成（[2.4](/developers/chartset/manifest/#2.4)）。 |
| `missing field <路径>` | 缺必需字段，路径如 `source.producer`、`bounds.west`。 |
| `invalid field <路径>: …` | 字段类型或取值不对，例如 `tileProfile` 写成字符串 `"1"`、`source.type` 不是 `external`/`s57`。 |
| `invalid field : Expected date string to be ISO8601-formatted.` | `createdAt` 不是带时间和时区的 ISO 8601（此项不带字段路径）。 |
| `tileProfile <值> unsupported, this App reads 1` | 剖面版本不受支持：按本手册重新生成（[2.4](/developers/chartset/manifest/#2.4)）。 |
| `invalid field name: empty` | `name` 是空串。 |
| `invalid field minimumZoom: zoom range …` | 缩放不在 0–24，或 `minimumZoom > maximumZoom`。 |
| `invalid field overviewZoom: <值> not below maximumZoom <值>` | `overviewZoom` 不小于 `maximumZoom`，或是负数；先于 `bounds`、`source` 校验。 |
| `invalid field bounds: not a longitude/latitude box` | 经纬度越界、不是有限数，或 `south > north`。 |
| `invalid field source.producer: empty` | `producer` 是空串。 |
| `invalid field id: empty or reserved s57: prefix` | `id` 为空，或以 `s57:` 开头。 |
| `invalid field source.cells…` 或 `invalid field id: S-57 chart set id must be …` | `"type": "s57"` 且清单本身未通过相应校验，例如没有 included 单元或 id 不匹配。即使清单合法也不能再导入（下表）；外部生产方应使用 `external`。 |
| `chart.mbtiles missing` | 没有 `chart.mbtiles`。 |
| `overview.mbtiles missing (manifest has overviewZoom)` | manifest 写了 `overviewZoom`，目录里却没有 `overview.mbtiles`。 |
| `<文件> is not a readable MBTiles (SQLite) file` | `chart.mbtiles` 或 `overview.mbtiles` 不是 SQLite 文件，或没有 `metadata` 表。 |
| `<文件> metadata has no integer dh_profile` | metadata 没有 `dh_profile`，或它的值读出来不是整数（例如 `1.0`）。 |
| `<文件> dh_profile <a> differs from manifest tileProfile <b>` | 两处版本不一致。 |

没有方括号、提示是其他句子时，对照下表。以“（代码 …）”结尾的提示，代码不随界面语言变化：

| App 提示 | 原因 |
| --- | --- |
| `这是定海由 S-57 转换生成的海图集，不能再导入。请导入 S-57 交换集（原件）。` | 合法 `s57` manifest 的海图集通过打开与校验后，仍被导入路径拒绝；这不是 `source.cells` 校验错误。 |
| `存储空间不足，还需 … 可用空间。` | 可用空间不足以复制海图集，`…` 为仍缺少的容量。 |
| `无法将离线海图包复制到应用存储。` | 复制失败，例如目录里有读不到的文件、符号链接或其他非普通文件（[第 1 节](/developers/chartset/structure/)）。 |
| `请选择一个海图数据文件夹。（代码 D1）` | 解压或选择后得到的内容根不是文件夹。 |
| `里面没有定海能识别的海图。请导入 S-57 交换集、含 manifest.json 的定海海图集或栅格 MBTiles，文件夹或 zip 均可。（代码 D2）` | 所选根和下面一层都没有 `manifest.json`，也找不到 S-57 交换集或 `.mbtiles`；空 ZIP 也是这样。`manifest.json` 放得比包装目录更深时也会这样（[1.1](/developers/chartset/structure/#1.1)）。 |
| `无法读取 MBTiles 文件：…。（代码 D3）` | 没有 manifest 时找到的某个 `.mbtiles` 打不开，或没有可读的 `metadata`、`tiles`。 |
| `暂不支持这个海图瓦片格式：…。（代码 D4）`，或 `无法识别这个海图瓦片格式。（代码 D4）` | 没有 manifest 时找到的某个 `.mbtiles` 既不是栅格也不是矢量瓦片。 |
| `所选文件夹同时包含栅格和矢量海图，请分别导入。（代码 D5）` | 没有 manifest，且同时有栅格和矢量 `.mbtiles`。 |
| `所选容器不是单个海图集的纯包装；请选择其中一份海图集。（代码 D6）` | 无声明根下有多份独立海图集，或内容根之外还有其他项目（隐藏文件也算）；分别选择内容根（[1.1](/developers/chartset/structure/#1.1)）。 |
| `下载内容不是 S-57 交换集；定海海图集请从文件导入。（代码 D7）` | 只在“从网址下载”（含“NOAA 海图…”）时出现：下载入口只接受 S-57 交换集。定海海图集请用“从文件导入…”导入。 |
| 以“（代码 V1）”“（代码 V2）”“（代码 V3）”结尾的提示 | 没有 manifest 的矢量 MBTiles，见 [7.3](/developers/chartset/vector-mbtiles/#7.3)；多份矢量库没有 manifest 时报 V3，见 [1.2](/developers/chartset/structure/#1.2)。 |
| 以“（代码 Z1）”…“（代码 Z6）”、“（代码 M…）”或“（代码 F1）”“（代码 F2）”结尾的提示 | ZIP 无法解压，见下表。 |

ZIP 无法解压时的提示：

| 代码 | App 提示 | 原因 |
| --- | --- | --- |
| Z1 | 这个文件不是 ZIP 压缩包，或者没有下载完整。请重新获取文件后再试。 | 文件里找不到 ZIP 的目录记录。 |
| Z2 | 这个压缩包已损坏或不完整。请重新获取文件后再试。 | ZIP 自身的记录互相矛盾或提前结束。 |
| Z3 | 压缩包里的文件校验不一致，内容已损坏。请重新获取文件后再试。 | 某个文件的 CRC-32 不符。 |
| Z4 | 压缩包里有不安全或重复的文件路径，已停止解压。请在电脑上解压后重新打包为普通 zip。 | 路径不安全或有歧义（[1.1](/developers/chartset/structure/#1.1)）。 |
| Z5 | 这个压缩包有密码，请先在电脑上解压，再重新打包为普通 zip。 | 加密，包括 AES。 |
| Z6 | 这是分卷压缩包的一部分。请在电脑上合并解压后，重新打包为单个普通 zip。 | 分卷压缩。 |
| M&lt;n&gt; | 这个压缩包用了不支持的压缩方式，请在电脑上解压后重新打包为普通 zip。 | 压缩方式 n 既不是 stored 也不是 DEFLATE。 |
| F1 | 无法读取这个压缩包文件。请确认文件已完整下载到本机后再试。 | ZIP 文件本身打不开或读不出。 |
| F2 | 无法把解压出的文件保存到本机。请确认存储空间充足后再试。 | 解压出的文件写不进设备。 |

无 manifest 的矢量 MBTiles 仅在符合[第 7 节](/developers/chartset/vector-mbtiles/)时，经过全量验证和安装前规范化后接受；不是任意矢量瓦片补上 manifest 就能使用。

## 6.4 导入成功后应该看到什么

导入不会选中海图集，也不会移动地图。在地图上点“地图显示”按钮，在“离线海图”下选中刚导入的海图集；再在“搜索坐标”里输入 `bounds` 内的一个点（例如最小样例的 `37.80, -122.62`），或在“离线海图”列表里打开这份海图集，点“在地图上显示”，或手动把地图移过去，缩放到 `minimumZoom` 以上，应该看到：

- 水深区分档上色，陆地是陆地色，岸线、等深线是细线，安全等深线加粗（需要 `dh_prev_valdco`）；
- z11 起稀疏的水深数字，越放大越密；z8 起孤立危险（洋红圆底；仅靠保守缺省成为孤立危险的 z12 起，见 [5.1](/developers/chartset/data/#5.1) F 组），z12 起其余危险物与航标符号；z13 起等深线数值；
- 锚地等限制区只有品红虚线边线（来自 `dh_boundary` 线）；
- 移动准星到点物标上，读数显示物标名称（没有名称时写中文类名）与同款图标（地图上画成孤立危险的危险物，读数也是孤立危险图标），点开详情看属性；到水面上显示所在水深区的区间水深；到陆地上不显示水深。

最小样例小岛位于 37.80° N、122.62° W；约 z14，“离线海图”里的安全水深与深水保持默认的 3 米、10 米时，三圈水深依次为浅水蓝、浅青蓝、白色。沉船位于 `37.803144, -122.628527`，z10、z12、z16 点选均应读出“Sample Wreck · 6.5米”；水面 `37.799100, -122.625684` 在 z16 应读出“0–5米”，无名小岛中心不显示水深。覆盖外背景不是这份海图集提供的内容。

App 导入时不检查瓦片内容，所以“导入成功，但地图上看不到 / 点选读不到”时按下表查：

| 现象 | 常见原因 |
| --- | --- |
| 整片都没有 | `tile_row` 写成了 XYZ 行号（应为 TMS，[3.2](/developers/chartset/mbtiles/#3.2)）；瓦片不是可解码的 MVT；metadata `minzoom`/`maxzoom` 与 manifest 不一致；当前缩放浅于 `minimumZoom`。未 gzip 不必然导致缺图，当前容忍行为见 [4.1](/developers/chartset/tiles/#4.1)。 |
| 放大过 `overviewZoom` 后某片变空白 | `chart.mbtiles` 深级别不写那里的数据，`overview.mbtiles` 也没补上（[3.3](/developers/chartset/mbtiles/#3.3)）。 |
| 放大过 `overviewZoom` 后两套叠在一起或有细缝 | 概览没有按深级别的覆盖范围裁切，或裁切线又被简化（[3.3](/developers/chartset/mbtiles/#3.3)）。 |
| 某一类没有 | source-layer 名不是大写 S-57 缩写；几何类型不对（例如航标写成线或面，面的边线没带 `dh_boundary`）；低于该类的起始缩放（[5.1](/developers/chartset/data/#5.1)）。MultiPoint 航标当前仍会画多个符号，但不符合单点规范要求（[5.1](/developers/chartset/data/#5.1) D 组）。 |
| 水深区颜色不对 / 没有水深数字 | `DRVAL1`/`DRVAL2`/`DEPTH` 不是数值，或单位不是米；`SOUNDG` 没拆成单点。 |
| 符号是通用形状 | 选符号的属性缺失或值不对（[5.1](/developers/chartset/data/#5.1) D、F 组），列表属性没有写成逗号串。 |
| 某些缩放级别点选读不到 | 该物标只写进了部分级别（[4.4](/developers/chartset/tiles/#4.4)）。 |
| 边上的物标点选读不到 | manifest `bounds` 没有包住全部数据（[2.2](/developers/chartset/manifest/#2.2)）。 |
| 详情少了属性 | 属性名不是 S-57 目录里的缩写，或只写在了部分缩放级别；external `DEPARE` 面本来就只显示区间水深，不显示其他目录属性（[5.2](/developers/chartset/data/#5.2)）。 |

## 6.5 没有命令行校验器

定海不提供不启动 App 的离线校验命令：App 的校验就是导入路径本身，[6.2](#6.2) 走的正是这条路径。只想快速看版本号是否一致时，可以用 `sqlite3`：

```bash
sqlite3 chart.mbtiles "SELECT name, value FROM metadata WHERE name IN ('dh_profile','minzoom','maxzoom','bounds');"
```
