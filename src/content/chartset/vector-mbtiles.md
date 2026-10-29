---
title: 7. 本地导入无 manifest 的矢量 MBTiles
description: 没有 manifest 的单一矢量 MBTiles 怎样被识别、校验和规范化，以及 V1–V3 报错。
---

这是新增的本地入口，不改变已有 manifest、S-57 交换集、栅格包或下载的规则。仍选择文件夹或 ZIP，其中只有一个明确的矢量 MBTiles；不新增 PMTiles、直接选择单个 `.mbtiles`、多库拼合或任意格式下载。有多份矢量库时 App 不组合它们，见 [1.2](/developers/chartset/structure/#1.2)。

## 7.1 识别与四项必要信息

首批接收两类：缺 manifest 的 `dh_profile=1` 裸库，以及大写 S-57 对象类／属性的公开 MVT 剖面（本文称 `s57-acronym-mvt-v1`）。GDAL、Greenroom enc-mapbox-converter、openwaters enc-tiles 是公开生产工具的例子，不是品牌白名单，不保证其所有输出都能通过。

识别依据是实际 MVT 图层和属性、MBTiles 的 Web Mercator/TMS 网格，以及当前支持的 MVT 版本 2。品牌、producer、generator、文件名不参与识别。实际地理图层认不出时整包拒绝，不按命中比例放行；OpenMapTiles、Shortbread、Protomaps 等底图不从这个入口安装。`json/vector_layers` 不代替实际内容；它缺失或陈旧，但实际数据可读时，输出清单从瓦片重建。

格式方面，以下任一项不满足即整包拒绝（V1）：metadata `format` 是矢量瓦片编码（例如 `pbf`）；写了 `dh_profile` 时等于 `1`；写了 `scheme` 时是 `tms`；写了 `projection` 时是 `EPSG:3857` 或 `3857`（不分大小写）；每层的 MVT 版本是 2；瓦片地址在 0–24 级的 Web Mercator/TMS 网格内；数据不跨 180° 经线、不越出经度范围。

除格式外只校验以下四项必要信息，不把分析稿中的候选打分、OBJL 矛盾检查或 DSID 辅助结构分类当作准入条件：

| 必要信息 | 读取规则 |
| --- | --- |
| 水深区范围 | 每个 `DEPARE` 面都须同时有可读的 `DRVAL1/DRVAL2`，每个 `DRGARE` 面都须有可读的 `DRVAL1`，缺一项即整包拒绝并指出字段；空串按缺失处理。`DEPARE`、`DRGARE` 层里除面和 `dh_boundary = 1` 的边线外不能有其他几何。数值字符串可转为有限数值；上下限不能颠倒，不补 0；整包没有可读水深区也拒绝。 |
| 逐点测深 | 存在的每个 `SOUNDG` 必须是独立点并带可读 `DEPTH`。所有 `SOUNDG` 点的 feature id 在安装前清除，这样共用原始物标 id 的拆点不会被点选去重吞掉不同深度（[4.1](/developers/chartset/tiles/#4.1)）；不把一个多点属性猜成每点深度。 |
| 深度单位 | `dh_profile=1` 有独立的米制合同；公开剖面以 `M_UNIT.DUNITS=1` 的实际范围确认米制，须覆盖相应深度几何。重叠的非米制声明不能被 profile 键盖过；`M_UNIT` 的单位或范围读不出时也拒绝。正值向下，负值为干出。 |
| 可见面的边线 | 公开 S-57 剖面的限制区、航道等面在规范化时，由整数面环生成同层 `dh_boundary=1` 的线，替换输入另外提供的私有边线，避免重复。只用一条剔除规则：两个端点同时满足 `x≤0`、`x≥extent`、`y≤0`、`y≥extent` 四者之一的边不生成，包含 buffer=0 的框边及框外 buffer 裁切边；其余边保持原坐标，在剔除处断开，不重新连边。已知代价：真实边界量化后恰与某级瓦片框线重合时，该段在该缩放级也不显示，不再额外判别。不做几何覆盖判定，也不因缺少输入边线拒绝。`dh_profile=1` 是生产方负责边线的格式，原样接收其边线，不检查、不重建。 |

海区没有浮标、陆地、灯标、测深点或限制区，不因此拒绝；有水深区且单位明确即可，不另要求凑齐物标种类。可选属性只做可读的类型规范化；不能解释的可选值不用来补造数值或颜色，也不因此拒绝整包。公开剖面的要素 id 在安装前全部清除；`dh_profile=1` 只清除 `SOUNDG` 的 id，其余 id 原样保留，须符合 [4.1](/developers/chartset/tiles/#4.1)。这一清除只发生在本节的无 manifest 入口；带 manifest 的海图集不经过规范化，id 原样使用。

依据：[MBTiles 1.3](https://github.com/mapbox/mbtiles-spec/blob/master/1.3/spec.md)、[MVT 2.1](https://github.com/mapbox/vector-tile-spec/tree/master/2.1)、S-57 3.1 对象／属性目录，以及 [GDAL S-57 driver](https://gdal.org/en/stable/drivers/vector/s57.html) 的类名分层、拆点与 DEPTH、列表表达。

## 7.2 一次单向规范化

```text
借入裸库（只读）
  → 自有暂存区：逐瓦片读取、校验必要信息并改写属性
  → manifest.json（当前 external / tileProfile 1）
    chart.mbtiles（dh_profile=1、gzip MVT、TMS）
    vector-import.json（v1 识别结果与可选功能缺项）
  → “导入矢量瓦片”确认页：定海样式预览、识别结果与功能说明，“取消”或“导入”
  → 现有安装提交
  → 现有定海日夜样式、符号、离线字体与准星读取同一份瓦片
```

- 只在安装前转换一次，不重试另一种格式，不加运行时 schema 适配、配置开关或原始库回退。保留 MVT 的 extent 和源面整数几何；公开剖面的派生边线只在剔除同侧框边处分段，再编码整数线，不投影、不重新量化。
- 规范化通过后先显示确认页；点“取消”不安装。失败或取消删除自有暂存，不提交目录册，不修改借入原件或已安装条目。
- 输出缩放与范围来自实际数据；逻辑 id 用输入内容指纹，不按文件名覆盖旧图，同样内容再导入替换前一次导入（[2.3](/developers/chartset/manifest/#2.3)）。`createdAt` 是本次生成时间，不是测绘日期。
- 识别结果只由本次安装写入；合法 manifest 包里的同名附件 `vector-import.json` 仍原样保存，不作为 App 验证结果读取。
- 缺 `dh_prev_valdco` 的线不能作为加粗安全等深线；缺 `dh_drval1` 的危险物沿用保守规则；缺来源／编辑比例尺就不显示相应事实。可选等深线数值或其他可选属性无法读取时也在确认页和海图详情的功能说明中写明，不把它们升级为必要条件。
- 不读取外部 style、sprite 或网络字体。识别通过不是海图真实、完整、最新或航行安全的认证；面轮廓生成的线不等于恢复原始 S-57 的遮罩或拓扑，也不可能恢复源文件遗漏的物标。

## 7.3 按处理办法分错误码

弹窗显示具体原因、处理办法和“（代码 Vn）”，并提供“好”“格式说明”。不是每个检查分一个码。

| 代码 | App 提示 | 情况 |
| --- | --- | --- |
| V1 | 这份矢量数据目前不能作为定海海图导入：<原因>。为避免漏画或误读，已停止导入。请向提供方索取完整的 S-57 交换集或定海海图集后再导入。 | 格式不受支持（[7.1](#7.1)）、实际图层无法识别，或四项必要信息不足。原因写明没通过的那一项，例如“测深点缺少可读取的逐点深度（SOUNDG.DEPTH，每个点须独立保存）”“深度单位未明确（DEPARE 没有 M_UNIT.DUNITS 米制范围）”“DEPARE.DRVAL2 缺少可读取的水深数值”“没有可读取的水深区数据”。不靠补 manifest 绕过缺项。 |
| V2 | 有些矢量瓦片无法读取，导入已停止。原因：<原因>。请确认文件已完整取得，或让提供方重新导出后再试。 | SQLite 数据库、表、metadata 或瓦片内容无法读取，例如 MVT 无法解码。 |
| V3 | 这里有多份矢量瓦片数据，定海无法确定它们应怎样组合。请分别选择一份完整海图，或让提供方整理成定海海图集。 | 没有 manifest，却有两份或更多矢量 MBTiles；见 [1.2](/developers/chartset/structure/#1.2)。 |
