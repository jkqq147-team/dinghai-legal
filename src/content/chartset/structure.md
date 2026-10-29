---
title: 1. 目录结构
description: 定海海图集的内容根与包装目录；多份矢量库没有 manifest 时为什么报 V3，怎样重新打包。
---

```
<任意目录名>/
  manifest.json     必需，第 2 节
  chart.mbtiles     必需，第 3、4 节
  overview.mbtiles  manifest 写了 overviewZoom 时必需，3.3
  （其他文件）      附件，原样保存，不读取
```

- 目录名不限；显示名取 manifest 的 `name`。
- App 只读 `manifest.json`、`chart.mbtiles` 和 `overview.mbtiles`。样式、图标、字体由 App 提供，生产方不提供。
- 只用普通文件和目录，不放符号链接。
- `chart.mbtiles` 是**一个**瓦片集，所有比例尺的数据已经合成在一起；`overview.mbtiles` 只补 `chart.mbtiles` 在深缩放级别有意不写的部分（[3.3](/developers/chartset/mbtiles/#3.3)）。两者合起来，同一级别、同一位置只有一套数据（[4.4](/developers/chartset/tiles/#4.4)）。

## 1.1 包装与内容识别

两种布局都可以，文件夹与 ZIP 规则相同：

```
所选文件夹或 ZIP/               所选文件夹或 ZIP/
  manifest.json                  任意包装名/
  chart.mbtiles                    manifest.json
  附件…                            chart.mbtiles
                                   附件…
```

- `manifest.json` 只在所选根和它下面一层查找。放在下面一层时，所选根下只能有这一个目录（纯包装）；旁边有任何其他项目，隐藏文件（例如 `.DS_Store`）也算，都会被拒绝（D6）。ZIP 里的 `__MACOSX`、`._` 条目不算。
- 有 `manifest.json` 的目录整个属于这份海图集：其中别的 `.mbtiles`、`.000`、嵌套 ZIP 等都是附件，原样保存，不读取。
- 一个父目录里有几份海图集时，分别选择各自的内容根导入。
- ZIP 只用普通文件和目录，不加密，不分卷。

## 1.2 多份矢量库：一个海图集只有一个 chart.mbtiles

一个定海海图集只有一个 `chart.mbtiles`，由 `manifest.json` 声明；可选的 `overview.mbtiles` 由 manifest 的 `overviewZoom` 声明。不同区域、不同比例尺的数据要先合成到这一个瓦片集里。

**V3 是什么情况**：所选文件夹或 ZIP 的根和下面一层都没有 `manifest.json`，也不是 S-57 交换集，App 在其中找到两份或更多矢量 MBTiles。App 不猜它们怎样组合：不按文件名把某一份当作 `chart.mbtiles` 或 `overview.mbtiles`，不拼合，也不只挑一份导入，所以拒绝导入（代码 V3）。只有 `chart.mbtiles` 和 `overview.mbtiles` 两个文件、没有 `manifest.json` 时，同样是 V3。

**怎样重新打包**：

- 把数据合成为一个 `chart.mbtiles`，写好 `manifest.json`（第 2 节），按本页的目录结构打包；用概览瓦片集时，在 manifest 写 `overviewZoom` 并放入 `overview.mbtiles`（[3.3](/developers/chartset/mbtiles/#3.3)）。
- 确实是几份独立的海图时，分别打包成几个海图集，各有自己的 `manifest.json` 和 `id`，分别导入。
- 只要其中一份时，把它单独放进文件夹或 ZIP 再导入（[附录 7](/developers/chartset/vector-mbtiles/)）。

有 `manifest.json` 的海图集不会报 V3。没有 manifest 时的其他拒绝代码见 [6.3](/developers/chartset/self-check/#6.3)。
