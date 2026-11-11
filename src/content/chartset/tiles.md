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

- **source-layer 名必须是大写的 S-57 物标类缩写**，与 IHO S-57 物标目录完全一致（例如 `DEPARE`、`LIGHTS`）；例外只有可选的 `dh_coverage` 和 `dh_area_symbol`（下两条）。目录外的层名不画，也不报告。
- **覆盖边界线 `dh_coverage`**（可选）：整个海图集数据覆盖范围的外边界，闭合的 LineString/MultiLineString，不带属性；内部各来源之间的接缝不写。
- **区域符号 `dh_area_symbol`**（可选）：Point 要素，带字符串字段 `dh_symbol`，可带数值字段 `dh_minzoom`（见下表）。地图为每个点画一个 `dh_symbol` 指定的区域符号：10.5 级起淡入，11 级起完全显示；写了 `dh_minzoom` 的点，浅于该级不画。符号先放在点上；在那里与已放下的文字（水深数字、名称等）或已放下的另一个区域符号相碰时，依次改放到紧挨该点的八个方向上，画在第一处不相碰的位置；九处都相碰的不画。所以生产方不必让点避开水深数字和名称，物标密集处画出的符号会比写入的点少。准星不报告这些点。按 manifest 导入的海图集，App 原样安装瓦片，不生成这一层，不写就没有区域符号（无 manifest 的矢量 MBTiles 见 [7.2](/developers/chartset/vector-mbtiles/#7.2)）。

  `dh_symbol` 取下列 8 个值之一，或在其后加 `+more`（符号旁多一个小“!”，表示 `RESTRN` 还有该符号所代表一组之外的限制，例如 `noAnchoring+more`）；缺 `dh_symbol` 或取其他值的点不画。8 个值按相碰时先放的顺序是：`noEntry`（禁止或限制进入、避航区）、`noAnchoring`（禁止或限制锚泊）、`noFishing`（禁止或限制捕鱼、拖网）、`caution`（注意）、`anchorage`（锚地）、`cable`（电缆区）、`farm`（养殖场）、`information`（信息）。

  App 从 S-57 生成海图、或为无 manifest 的矢量 MBTiles 生成这一层时（[7.2](/developers/chartset/vector-mbtiles/#7.2)），对 `RESARE`、`CTNARE`、`ACHARE`、`MIPARE`、`DMPGRD`、`SPLARE`、`MARCUL`、`CBLARE`、`PIPARE` 的面按下列顺序取第一个成立的：

  1. `RESTRN` 含 7、8、14 → `noEntry`；否则含 1、2 → `noAnchoring`；否则含 3、4、5、6 → `noFishing`。`RESTRN` 还有这一组以外的值时加 `+more`。
  2. `RESTRN` 含 1–14 以外的值，或物标类是 `CTNARE`、`MIPARE`、`SPLARE`，或 `RESARE` 的 `CATREA` 含 1、8、9、12、14、19、25 → `caution`。
  3. `ACHARE` → `anchorage`；`CBLARE` → `cable`；`MARCUL` → `farm`。
  4. 其余（`RESARE`、`DMPGRD`、`PIPARE`）：`RESTRN` 含 9–13，或物标类是 `DMPGRD`、`PIPARE`，或 `CATREA` 含 4、5、6、7、10、18、20、22、23、24、27、28 → `information`；否则 `caution`。

  点放在哪里、一个区域放几个由生产方决定：App 不检查点的位置，也不把点和某个面对应起来，写一个点就画一个符号。App 自己生成这一层时这样放，生产方可照此放置：

  - 同一物标类、属性相同（比较方式见 [4.3](/developers/chartset/tiles/#4.3)）且相接或重叠的面合成一个区域。
  - 每个区域有一个锚点：区域最大一块的不可达极点（区域内离边界最远处），能做到时离航标本体和灯至少 60 米。10 级及更深的瓦片，不细长的区域都写锚点；细长的区域优先写下面的主轴中部站位，无法生成中部站位时才用锚点。
  - 细长的区域（最大一环的最小外接矩形，可旋转，长边至少是短边的 2 倍）沿主轴设固定站位：中部站位从 10 级起写入，不受下面的 12 pt 门槛限制。11 级起，从主轴中点向两侧按该级 115 pt 的间距设候选站位（一张瓦片按 512 pt 计），候选位置离主轴端部至少留该间距的四分之一；每深一级增加候选位置，原有候选位置不动，至 18 级为止，不再按当前级别把整条主轴等分。
  - 每个站位的点只按整个区域计算，不随瓦片或当前缩放重新选。中部站位取以主轴中点为中心的条带；条带宽度取首次能在两侧容纳候选站位那一级的 115 pt（至 18 级仍容纳不了则用 18 级），且不超过主轴长度的一半。其他站位的条带，以候选位置为中心，宽度为该候选位置首次纳入那一级的 115 pt。在条带与区域相交后最大的一块里选点，让它尽量远离区域边界和条带边缘；其他站位还避开相邻的、较浅级别纳入的候选站位，以到这些点的距离减去条带宽度四分之一，与到区域边界、条带边缘的距离一起取最小值，再找这个最小值最大的点。站位不按锚点的 60 米规则避让航标本体和灯。
  - 除中部站位外，上述最小距离按显示级别换算后至少为 12 pt 才写入；某一级不够宽的站位，等到更深一级满足门槛时在同一位置加入，至 18 级仍不满足就不写。放大只增加站位，已生成的站位不换位置；实际画出的符号仍按上文避让文字和其他区域符号。
  - 不细长的区域从 11 级起另在每一级固定的世界网格上加点，网格间距 200 pt，点离区域边界至少 16 pt、离锚点至少 100 pt；几个区域重叠处，一个网格点只写给其中一个区域。
  - 最深一级的瓦片同时带更深各级（至 18 级）的点，各带 `dh_minzoom`。
  - 符号是 `caution` 的 `CTNARE`，在符号是 `noEntry`、`noAnchoring`、`noFishing`（含 `+more`）的 `RESARE` 以及 `ACHARE`、`CBLARE`、`MARCUL` 的范围内不放点。
  - 点只写在该级瓦片画出这个区域的地方；细长区域的站位若因轮廓简化略落在面外，距该瓦片所画区域的边界不超过 16 级网格的 24 个单位（该网格一张瓦片为 4096 个单位，换算到瓦片所在级别至少取 1 个单位）时也写入。同一张瓦片里相距不到 8 pt 的相同符号只写一个。
- **准星点亮区域边线**：[5.1](/developers/chartset/data/#5.1) E 组写“面”的各物标类中，准星在一个能读到、且 `RESTRN` 含 1、3、5、7、9、11、13、14、15 之一的面内时（[5.2](/developers/chartset/data/#5.2)），地图把当前画出的、同一 S-57 物标类且 `RESTRN` 取值集合相同的区域边线叠画为加粗的品红实线（日间外观用 `CHMGD` 品红，深色外观更亮），区域内部不涂；准星离开后熄灭。

  - 比较时不计 `RESTRN` 的顺序和重复值，例如 `"14,3"` 与 `"3,14,14"` 相同，其他属性不参与匹配。面不必相接，也不必属于同一物标或同一来源单元。
  - 准星同时命中几个会触发点亮的集合时，各自的边线都点亮。
  - 只点亮原有的可见边线（`dh_boundary = 1`，见 [4.3](/developers/chartset/tiles/#4.3)），不沿面补画轮廓。单元接缝、瓦片切边、被更详细单元覆盖处等裁切口本来就没有边线，点亮的轮廓在那里仍是开口。
  - 同亮只表示物标类和 `RESTRN` 相同，不表示名称、法规、适用船型或其他限制条件相同。
  - **制作方无需添加点亮字段或划定跨单元的区域身份**：触发读的是面上的 `RESTRN`，被点亮的是边线要素。按本节格式提供正确的大写 S-57 source-layer、面几何和完整的 `RESTRN`；边线按 [4.3](/developers/chartset/tiles/#4.3) 带 `dh_boundary = 1` 和该物标的全部属性（含 `RESTRN`），放在同一个 source-layer。在面和边线出现的每个缩放级别及瓦片集中保留相应属性（[4.4](/developers/chartset/tiles/#4.4)）。`RESTRN` 仍是逗号分隔的整数值字符串，单值也写成字符串；无需为点亮统一顺序或去重，App 按整数集合比较。按 manifest 导入的瓦片由制作方负责，App 原样安装，不为点亮改写。
  - 缺少可读的 `RESTRN`，或不含上述触发值的面，不会触发点亮；边线、区域符号和准星读数仍按各自约定显示。

  旧包里的 `dh_area` 会被忽略，无需为此重制、替换或重新导入；App 不再为原生 S-57 或无 manifest 的导入包生成它，已有包更新 App 后直接按上述规则点亮。点亮与区域符号互不依赖：没有 `dh_area_symbol` 层就没有区域符号，已有的符号照上文画出，大小仍是点状符号的 1.3 倍。
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
  | `dh_has_body` | 整数 `1`，可选 | 只在 `LIGHTS` 点上：同一单元里有与灯坐标完全相同的 `BOYSPP`、`BCNSPP`、`BOYSAW`、`BCNSAW`、`LITFLT`、`LITVES`、`BOYLAT`、`BCNLAT`、`BOYCAR`、`BCNCAR`、`BOYISD`、`BCNISD` 点时写 `1`；否则不写，不能仅凭附近有本体或 `FFPT` 关系写入。 |
  | `dh_surface_cell` | 字符串，可选 | 数据的来源单元名。 |
  | `dh_surface_cscl` | 整数，可选 | 来源单元的编辑比例尺分母；与非空的 `dh_surface_cell` 一起提供时使用。 |
  | `dh_symbol` | 字符串 | 只在 `dh_area_symbol` 点上：画哪个区域符号（见上文）。 |
  | `dh_minzoom` | 数值，可选 | 只在 `dh_area_symbol` 点上：从这一级起才画这个点；不写则不限。 |

## 4.3 几何

| 几何 | MVT 类型 | 用于 |
| --- | --- | --- |
| 点 | Point | 点物标、水深点。航标类规范要求单点 Point（[5.1](/developers/chartset/data/#5.1) D 组）。 |
| 线 | LineString / MultiLineString，**不带** `dh_boundary` | 线物标：等深线、岸线、电缆、航线等。 |
| 面 | Polygon / MultiPolygon | 面物标。面本身没有可见边线。 |
| 边线 | LineString，带 `dh_boundary = 1` 和该物标的全部属性，放在**同一个** source-layer | 面状物标的可见边线。 |

边线单独写，是为了让单元接缝、被遮罩的边、只沿数据界限的边都不出现：生产方只写真正应该看见的那几段。不写边线，那个面就没有可见边界。

**被单元切开的面先合并，再生成边线。** 从多个单元（`dh_surface_cell`）切出面时，同一物标类里属性相同、并且相接或重叠的几块是同一个面：先把它们合并，再从合并后的面生成 `dh_boundary = 1` 的线，单元切口（无论在瓦片内部还是沿瓦片边框）都不写成边线。比较属性时不计 `dh_` 开头的字段和 `SCAMIN`、`SCAMAX`、`TXTDSC`、`NTXTDS`、`PICREP`、`RECDAT`、`RECIND`、`SORDAT`、`SORIND`，其余属性全部相同才算同一个面。按 manifest 导入的海图集，App 照写入的边线画，不替你合并；切口写成了边线，地图上就有这条线。

## 4.4 缩放级别与用途带

- 每一级显示和点选读的都是这一级（深于 `maxzoom` 时是最深一级）的瓦片，有概览瓦片集时另加 [3.3](/developers/chartset/mbtiles/#3.3) 的概览。所以**一个物标在它出现的每个缩放级别都要带齐[第 5 节](/developers/chartset/data/)要求的属性**，只放在最深一级不够。建议在 `minzoom`–`maxzoom` 之间凡有数据处都写（可以省掉的浅级别见下文）；某一级不写某个物标，在那一级就点选不到它。
- **写进某一级，不等于在那一级就画出来、能点选。** 导入的海图集（包括按[附录 7](/developers/chartset/vector-mbtiles/)导入的矢量 MBTiles）中，下表各物标类的这些画法有显示级别：从表中级别起完全显示；标有淡入的，从前半级起由透明渐变到原有样式，再浅就不画；没有淡入的，浅于表中级别就不画。不画的时候，准星也不会经由这一画法读到该物标。这些级别是定海自己选定的，S-52 没有规定地图缩放级别。

  | 显示级别 | 淡入 | 物标类 | 画法 |
  | --- | --- | --- | --- |
  | 7 | 6.5 起 | `DEPCNT` | 线，安全等深线和干出线（`VALDCO` 为 0）除外 |
  | 8 | 7.5 起 | `RESARE` `CTNARE` `ACHARE` `MIPARE` `DMPGRD` `SPLARE` `MARCUL` `CBLARE` `PIPARE` `ACHBRT` `PILBOP` `FSHFAC` `HRBARE` `SUBTLN` `OSPARE` `FSHGRD` `CTSARE` `ICNARE` `SNDWAV` `WEDKLP` | 边线 |
  | 8 | 7.5 起 | `FAIRWY` `PRCARE` `TSSLPT` `DWRTPT` `ISTZNE` `TSSRON` `TSSCRS` `TWRTPT` `RCTLPT` `RECTRC` `FERYRT` | 边线 |
  | 8 | 7.5 起 | `TSEZNE` | 面 |
  | 8 | 7.5 起 | `TSELNE` `TSSBND` `DWRTCL` `RECTRC` `RCRTCL` `NAVLNE` `FERYRT` `MARCUL` `RDOCAL` | 线 |
  | 8 | 7.5 起 | `OBSTRN` `WRECKS` `UWTROC` | 画成孤立危险物的点（例外见表下） |
  | 8 | — | `LIGHTS` | 点，画成灯色圆点；11.5–12 淡出，由灯光符号接替 |
  | 10 | — | `SEAARE` | 带 `CATSEA` 的名称 |
  | 11 | 10.5 起 | `CBLSUB` `PIPSOL` | 线 |
  | 11 | 10.5 起 | `dh_area_symbol` | 点，画成区域符号（[4.2](/developers/chartset/tiles/#4.2)） |
  | 11 | — | `SOUNDG` | 点，画成水深数字 |
  | 11 | — | `LNDRGN` `BUAARE` | 名称 |
  | 12 | 11.5 起 | `BOYLAT` `BCNLAT` `BOYCAR` `BCNCAR` `BOYISD` `BCNISD` `BOYSAW` `BCNSAW` `BOYSPP` `BCNSPP` `LITFLT` `LITVES` `TOPMAR` `LIGHTS` | 点：航标本体、顶标和灯光符号 |
  | 12 | 11.5 起 | `DAYMAR` `RTPBCN` `RADRFL` | 点 |
  | 12 | 11.5 起 | `OBSTRN` `WRECKS` `UWTROC` | 其余的点 |
  | 12 | 11.5 起 | `LNDMRK` `SILTNK` `OFSPLF` | 点 |
  | 12 | — | `OBSTRN` `WRECKS` `UWTROC` | 点旁的水深（`VALSOU`），孤立危险物也是 |
  | 12 | — | `LIGHTS` | 灯质 |
  | 12 | — | `SEAARE` | 其余名称 |
  | 12 | — | `ROADWY` `RAILWY` `LNDELV` `FNCLNE` `SLOTOP` `VEGATN` `TUNNEL` | 线 |
  | 13 | 12.5 起 | `MORFAC` `PYLONS` `WEDKLP` `WATTUR` `HRBFAC` `SMCFAC` `ACHARE` `ACHBRT` `FOGSIG` `CGUSTA` `PRDARE` `NEWOBJ` `SNDWAV` `PILBOP` `DMPGRD` `SISTAW` `SISTAT` | 点 |
  | 13 | 12.5 起 | `RDOSTA` `RADSTA` `RDOCAL` `CRANES` `CTNARE` `SLCONS` `TS_FEB` `FORSTC` `AIRARE` `CTRPNT` `LNDELV` `SLOGRD` | 点 |
  | 13 | — | `DEPCNT` | 等深线数值 |
  | 13 | — | `ACHARE` `HRBFAC` `SMCFAC` | 名称 |
  | 14 | 13.5 起 | `BUISGL` `PILPNT` | 点 |
  | 15 | 14.5 起 | `SBDARE` | 点（底质） |
  | 15 | — | `BERTHS`，航标本体（`BOYLAT` … `LITVES` 共 12 类） | 名称 |

  孤立危险物由 App 按用户设置的安全水深判定（S-52 的孤立危险物规则），与 `VALSOU`、`WATLEV`、`CATWRK`、`CATOBS` 和 `dh_drval1`（[4.2](/developers/chartset/tiles/#4.2)）有关。其中没有 `VALSOU`、没有 `dh_drval1`、`WATLEV` 未写或为 3 的，除 `CATWRK` 为 1、2、4、5 的 `WRECKS` 和 `CATOBS` 为 6 的 `OBSTRN` 外，也到 12 级才完全显示（11.5 起淡入）。
- 表里没有的物标类和画法没有显示级别的限制，例如水深区 `DEPARE`、`DRGARE`（包括浅水图案），`LNDARE` 的面、线和点（小岛），岸线 `COALNE`，直线基线 `STSLNE`，安全等深线和干出线，架空的 `CBLOHD`、`PIPOHD`，`OBSTRN`、`WRECKS`、`UWTROC` 的面、边线和线，建筑物 `PYLONS`、`GATCON`、`OFSPLF` 的面和边线，陆上的 `SILTNK`、`LNDMRK`、`PRDARE`、`AIRARE` 的面和边线，`PONTON`、`FLODOC`、`GATCON`、`CONVYR`、`OILBAR`、`CANALS`、`RIVERS` 的线，以及 `TUNNEL` 的边线。
- 文字（水深数字、名称、灯质、危险物旁的水深、等深线数值）和 `SBDARE` 底质会互相避让，放不下的不画。水深点只画成数字，数字被让掉时，那个水深点在这一级也点选不到。
- 一类物标的每种画法都在表中时，`chart.mbtiles` 里比其中最早开始画出（有淡入的按开始淡入算）的缩放所在那一级更浅的级别，写进这类物标也不会画出、点选不到，可以不写。例如 `CBLSUB`、`PIPSOL` 10.5 起淡入：第 10 级瓦片里的在 10.5–11 之间淡入显示，第 9 级及更浅的不画。两处例外照常写：最深一级（`maxzoom`）在更深的缩放放大使用，`overview.mbtiles` 在深于 `overviewZoom` 的各级放大使用（[3.3](/developers/chartset/mbtiles/#3.3)）。`DEPCNT` 和 `OBSTRN`、`WRECKS`、`UWTROC` 还有不在表中的画法（安全等深线和干出线；面、边线和线），哪条是安全等深线、哪个点是孤立危险物又随用户设置的安全水深而变，所以浅级别也照常写。写进去的级别，仍按第一条带齐属性。
- 用途带（S-57 INTU，1 概览 … 6 靠泊）不是瓦片字段。生产方自行决定每个缩放级别用哪个比例尺的数据，原则是**同一级别、同一位置只放一套数据**：两套重叠时两套都会显示，点选也可能报告两套。有概览瓦片集时，`chart.mbtiles` 与放大后的 `overview.mbtiles` 合起来算（[3.3](/developers/chartset/mbtiles/#3.3)）。
- 某一级、某处既没有水深区面（`DEPARE`、`DRGARE` 的面）也没有陆地面时，下方的定海底图（海面、陆地与岸线）会透出；不要在这一级单独写陆地面（如 GSHHG 概览陆地），以免岸线不重合时出现两层岸线和夹在中间的杂色条。应在这一级写入真实的水深区面，或不写陆地面，整级交给定海底图。
