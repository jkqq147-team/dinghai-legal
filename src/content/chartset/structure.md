---
title: 1. 目录结构
description: 定海海图集的内容根、包装目录与 App 的内容识别规则；多份矢量库没有 manifest 时为什么报 V3。
---

```
<任意目录名>/
  manifest.json     必需，第 2 节
  chart.mbtiles     必需，第 3、4 节
  overview.mbtiles  manifest 写了 overviewZoom 时必需，第 3.3 节
  （其他文件）      普通附件，原样保存
```

- 目录名不限；App 显示的名字取 manifest 的 `name`。
- 只有 `manifest.json`、`chart.mbtiles` 和 `overview.mbtiles` 会被读取。样式、图标、字体、`schema/` 一类的文件写了也不用：App 只按物标类和属性名用自己的样式画图。
- 文件夹内允许普通目录与普通文件，但不得含符号链接或其他非普通节点，包括额外附件；所选目录本身也不能是链接。
- `chart.mbtiles` 是**一个**瓦片集，所有比例尺的数据已经合成在一起：每个缩放级别、每个位置只有一套瓦片。`overview.mbtiles` 只补 `chart.mbtiles` 在深缩放级别有意不写的那部分（[3.3](/developers/chartset/mbtiles/#3.3)），两者合起来仍是每处一套数据。

## 1.1 包装与内容识别

以下两种布局都支持，目录输入与 ZIP 用相同规则：

```
所选目录或 ZIP/                 所选目录或 ZIP/
  manifest.json                  任意包装名/
  chart.mbtiles                    manifest.json
  普通附件…                        chart.mbtiles
                                   普通附件…
```

- “纯包装”指所选根下只有一个内容根目录，不把内容根之外的普通文件或其他目录猜作它的附件；不递归寻找第一个 manifest。`manifest.json` 只在所选根和它下面一层查找。无声明的父目录里有多份独立海图集时，App 不擅自选一个，须分别选择内容根导入。
- 包装目录旁边的任何其他项目都会让它不再是纯包装，隐藏文件（例如 Finder 留下的 `.DS_Store`）也算；ZIP 里的 `__MACOSX`／`._` 资源叉条目除外（见下文）。
- 一旦内容根有 `manifest.json`，它声明整个包。`schema/manifest.json`、`.000`、其他 `.mbtiles` 或嵌套 ZIP 等普通附件仍归此包，原样保存，不另作产品识别，也不解压嵌套 ZIP。坏 JSON、错误格式或不支持的版本／剖面会报海图集错误，不换成 S-57 或栅格重试。
- `format = dinghai-chartset` 是内容识别声明，不是全瓦片认证；安装仍检查最终候选的 manifest、`external` 来源与 MBTiles 剖面。生产方名称、品牌、地区、目录名与 ZIP 文件名不参与业务分派。
- ZIP 支持 stored／DEFLATE 和 ZIP64，不支持加密或分卷；拒绝重复路径、大小写／Unicode 规范别名、文件与目录冲突、绝对路径、`..` 逃逸和非普通节点。`__MACOSX`／`._` 资源叉条目会跳过。
- 不承诺抵御目录输入期间的任意并发文件系统替换；生产方应提供稳定的输入。App 自己的库不能作为导入源。

## 1.2 多份矢量库：一个海图集只有一个 chart.mbtiles

一个定海海图集只有一个 `chart.mbtiles`，再加上声明它的 `manifest.json`（可选再加 `overview.mbtiles`，由 manifest 的 `overviewZoom` 声明）。不同区域、不同比例尺的数据要先由生产方合成到这一个瓦片集里（第 1 节、[4.4](/developers/chartset/tiles/#4.4)）。

所选目录或 ZIP 在根部和下面一层都没有 `manifest.json`，也不是 S-57 交换集时，App 在其中逐个查找 `.mbtiles` 文件（跳过隐藏文件，也跳过更深处带 `manifest.json` 的目录）：

| 找到的 `.mbtiles` | App 怎么做 |
| --- | --- |
| 没有 | 拒绝：“里面没有定海能识别的海图。…”（代码 D2）。 |
| 一份矢量库 | 按[第 7 节](/developers/chartset/vector-mbtiles/)识别并规范化；不符合时报 V1 或 V2。 |
| 两份或更多矢量库 | 拒绝，代码 V3（下文）。 |
| 同时有栅格和矢量 | 拒绝：“所选文件夹同时包含栅格和矢量海图，请分别导入。”（代码 D5）。 |
| 其中一份打不开，或瓦片格式认不出 | 拒绝，代码 D3 或 D4（[6.3](/developers/chartset/self-check/#6.3)）。 |

两份或更多矢量库时，App 显示：

> 这里有多份矢量瓦片数据，定海无法确定它们应怎样组合。请分别选择一份完整海图，或让提供方整理成定海海图集。（代码 V3）

App 不猜这些库该怎样组合：不按文件名把其中一份当作 `chart.mbtiles`、另一份当作 `overview.mbtiles`，不拼合，也不只挑一份导入。只有 `chart.mbtiles` 和 `overview.mbtiles` 两个文件、却没有 `manifest.json` 时，同样报 V3。

生产方的处理办法：

- 把数据合成为一个 `chart.mbtiles`，写好 `manifest.json`（第 2 节），按本页的目录结构打包成一个海图集；用了概览瓦片集时，在 manifest 写 `overviewZoom` 并放入 `overview.mbtiles`（[3.3](/developers/chartset/mbtiles/#3.3)）。
- 确实是几份独立的海图时，分别打包成几个海图集，各自有自己的 `manifest.json` 和 `id`，分别导入。

有 `manifest.json` 的海图集不会报 V3：内容根里的其他 `.mbtiles` 只是附件，不会被读取。
