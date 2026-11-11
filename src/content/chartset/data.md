---
title: 5. 数据清单
description: 各物标类的几何类型与必须、可选的属性；点选报告的物标与地表类。
---

术语：

- **必须**：缺了这一项，这一类物标不能正确使用。
- **可选**：有就用，括号里是用途；没有也能显示、能点选，格内注明的例外除外。
- “名称”指 `NOBJNM` 或 `OBJNAM`。
- 几何：“面”是 Polygon，“边线”是带 `dh_boundary = 1` 的线（[4.3](/developers/chartset/tiles/#4.3)），“线”是不带 `dh_boundary` 的线；MVT 类型见 4.3。

## 5.1 物标类与属性

地图只画本节列出的类和 `dh_coverage`、`dh_area_symbol`（[4.2](/developers/chartset/tiles/#4.2)）；准星只报告地图上已绘制且符合点选资格的物标，其他目录内未绘制的物标不会报告（[5.2](/developers/chartset/data/#5.2)）。

**A. 水深与水域**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `DEPARE` | 面 | `DRVAL1`、`DRVAL2` | — |
| `DRGARE` | 面、边线 | `DRVAL1` | `DRVAL2`（水深） |
| `DEPCNT` | 线 | `VALDCO` | `dh_prev_valdco`（安全等深线） |
| `SOUNDG` | 点，**每个水深点一个点要素** | `DEPTH` | — |
| `CANALS` `RIVERS` | 面、线 | — | — |
| `DOCARE` `LOKBSN` `LAKARE` | 面 | — | — |

- `DEPARE` 缺上下限、`DRGARE` 缺下限，表示水深未知，不是实测安全水深。
- `SOUNDG` 的水深写在派生字段 `DEPTH`（米），不是 S-57 的 3D 坐标；一个多点测深物标须拆成多个点要素，每点带自己的 `DEPTH`，id 规则见 [4.1](/developers/chartset/tiles/#4.1)。
- 负值表示干出高度，不应由生产方改成绝对值。

**B. 陆地与岸线**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `LNDARE` | 面、线、点 | — | 名称（读数） |
| `COALNE` | 线 | — | — |
| `STSLNE` | 线 | — | — |
| `BUAARE` `RUNWAY` | 面、边线 | — | `CONVIS`（醒目）；`BUAARE` 名称（标注） |
| `PRDARE` `AIRARE` | 面、边线、点 | — | `CONVIS`（面和边线醒目） |
| `BUISGL` | 面、边线、点 | — | `CONVIS`（醒目） |
| `ROADWY` `RAILWY` `FNCLNE` `SLOTOP` `VEGATN` | 线 | — | `CONVIS`（醒目） |
| `LNDELV` | 线、点 | — | `CONVIS`（线醒目） |
| `TUNNEL` | 线、边线 | — | `CONVIS`（线醒目） |
| `LNDRGN` | 点、线、面 | — | 名称（标注；没有名称时不显示） |

**C. 港口与建筑**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `HULKES` `DRYDOC` | 面、边线 | — | — |
| `PONTON` `FLODOC` `DAMCON` `DYKCON` `CAUSWY` `BRIDGE` `GATCON` | 面、边线、线 | — | — |
| `SLCONS` | 面、边线、线、点 | — | — |
| `CONVYR` `OILBAR` | 线 | — | — |
| `HRBFAC` | 点、线、面 | — | `CATHAF`（符号）；名称（标注；线、面没有名称时不显示） |
| `SMCFAC` | 点、线、面 | — | 名称（标注；线、面没有名称时不显示） |
| `BERTHS` | 点、线、面 | — | 名称（标注；没有名称时不显示） |
| `MORFAC` | 点 | — | `CATMOR`（符号）；`COLOUR`、`COLPAT`（颜色） |
| `PILPNT` | 点 | — | — |
| `PYLONS` | 面、边线、点 | — | `CATPYL`（点的符号） |
| `OFSPLF` | 面、边线、点 | — | — |
| `LNDMRK` | 面、边线、点 | — | `CATLMK`（点的符号）；`CONVIS`（醒目） |
| `SILTNK` | 面、边线、点 | — | `CATSIL`（点的符号）；`CONVIS`（醒目） |
| `WATTUR` `FOGSIG` | 点 | — | — |
| `CGUSTA` `NEWOBJ` `SISTAW` `SISTAT` `CRANES` `TS_FEB` `FORSTC` `CTRPNT` `SLOGRD` | 点 | — | — |

**D. 航标**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `BOYLAT` `BCNLAT` `BOYCAR` `BCNCAR` `BOYISD` `BCNISD` `BOYSAW` `BCNSAW` `BOYSPP` `BCNSPP` `LITFLT` `LITVES` | 单点 Point | — | `BOYSHP`、`BCNSHP`（形状）；`CATLAM`、`CATCAM`（类别）；`COLOUR`、`COLPAT`（颜色）；`MARSYS`（浮标制度）；名称（标注） |
| `TOPMAR` | 单点 Point | — | `TOPSHP`（形状）；`COLOUR`（颜色） |
| `LIGHTS` | 单点 Point | — | `COLOUR`（颜色）；`LITCHR`、`SIGGRP`、`SIGPER`（灯质）；`dh_has_body`（灯光位置） |
| `DAYMAR` `RTPBCN` `RADRFL` `RDOSTA` `RADSTA` | 点 | — | — |

- 真实颜色已知时写 `COLOUR`。
- 顶标、灯与浮标本体同位置时，分别写在各自的图层（`TOPMAR`、`LIGHTS`），与 S-57 一致。
- 灯与本体同位置（条件见 [4.2](/developers/chartset/tiles/#4.2)）时，App 转换 S-57 会在 `LIGHTS` 点上写入 `dh_has_body = 1`，外部生产方可选择写入以将灯光画在本体灯头处，也可不写；缺少该字段时，灯画成以自身位置为中心的灯色圆点。
- `DAYMAR`、`RTPBCN`、`RADRFL`、`RDOSTA`、`RADSTA` 与航标本体、灯或顶标坐标完全相同时，准星把它们读作这座航标的一部分（[5.2](/developers/chartset/data/#5.2)）。

**E. 航路、限制区、管线**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `FAIRWY` `PRCARE` `TSSLPT` `DWRTPT` `ISTZNE` `TSSRON` `TSSCRS` `TWRTPT` `RCTLPT` | 面、边线 | — | — |
| `TSEZNE` | 面 | — | — |
| `TSELNE` `TSSBND` `DWRTCL` `RCRTCL` `NAVLNE` | 线 | — | — |
| `RECTRC` | 线、边线 | — | — |
| `FERYRT` | 线、面、边线 | — | — |
| `RESARE` `MIPARE` `SPLARE` `CBLARE` `PIPARE` `FSHFAC` `HRBARE` `SUBTLN` `OSPARE` `FSHGRD` `CTSARE` `ICNARE` | 面、边线 | — | 见表下 |
| `MARCUL` | 面、边线、线 | — | 见表下 |
| `CTNARE` `DMPGRD` `SNDWAV` `WEDKLP` `ACHBRT` | 面、边线、点 | — | 见表下 |
| `ACHARE` | 面、边线、点 | — | 名称（标注）；见表下 |
| `PILBOP` | 边线、点 | — | — |
| `RDOCAL` | 线、点 | — | — |
| `CBLSUB` `PIPSOL` `CBLOHD` `PIPOHD` | 线 | — | — |

- 本组写“面”的类，除 `TSEZNE` 外面本身不画，看得见的是边线，准星点亮时也只亮边线（[4.2](/developers/chartset/tiles/#4.2)）；准星靠面读到这个区域（[5.2](/developers/chartset/data/#5.2)），只写边线的读不到。
- `RESARE`、`CTNARE`、`ACHARE`、`MIPARE`、`DMPGRD`、`SPLARE`、`MARCUL`、`CBLARE`、`PIPARE` 的面：`RESTRN`、`CATREA` 决定区域符号（规则见 [4.2](/developers/chartset/tiles/#4.2)），也决定准星“此处还有”里这个区域那一行的图标。海图集的区域符号要生产方写进 `dh_area_symbol`；无 manifest 的矢量 MBTiles 由 App 生成（[7.2](/developers/chartset/vector-mbtiles/#7.2)）。
- 本组写“面”的类：`RESTRN` 含禁止事项时，准星可由这个区域领先；准星“此处还有”里这个区域那一行带它的关键属性：`ACHARE` 的 `CATACH`、`MARCUL` 的 `CATMFA`、`FSHFAC` 的 `CATFIF`、`MIPARE` 的 `CATMPA`，没有时用 `RESTRN`；其他类先 `RESTRN`，再 `CATREA`（[5.2](/developers/chartset/data/#5.2)）。
- 本组写“面”的类：准星进入能读到、`RESTRN` 含禁止事项的面时，当前画出的同类、`RESTRN` 取值集合相同的区域边线一起点亮，内部不涂，不需要新增派生字段（[4.2](/developers/chartset/tiles/#4.2)、[5.2](/developers/chartset/data/#5.2)）。

**F. 危险物**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `WRECKS` | 面、边线、线、点 | — | `WATLEV`（水位）；`CATWRK`（符号）；`VALSOU`（水深）；点上 `dh_drval1`（周围水深） |
| `OBSTRN` | 面、边线、线、点 | — | `WATLEV`（水位）；`CATOBS`（符号）；`VALSOU`（水深）；点上 `dh_drval1`（周围水深） |
| `UWTROC` | 面、边线、线、点 | — | `WATLEV`（水位）；`VALSOU`（水深）；点上 `dh_drval1`（周围水深） |
| `SBDARE` | 点 | — | `NATSUR`（底质；没有 `NATSUR` 时不显示） |

提供 `VALSOU` 时用实际米制深度；周围水深的派生字段 `dh_drval1` 见 [4.2](/developers/chartset/tiles/#4.2)，不能把危险物本身的深度写成周围水域深度。

**G. 名称**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `SEAARE` | 点、线、面 | — | 名称（标注；没有名称时不显示）；`CATSEA`（类别） |

## 5.2 点选会报告的物标

- **资格**：只报告 S-57 目录内的地理物标；元物标（`M_*`）、集合物标（`C_*`）、制图物标不报告。5.3 的七类仅源几何为面时是地表，其余有效地理物标可报告。`dh_boundary = 1` 的边线不读：面只经由它自己的面要素读到。
- **读地图画出的**：准星只读当前缩放下地图实际画出的要素，用的就是画它时的属性；[4.4](/developers/chartset/tiles/#4.4) 的显示级别和文字避让都算在内。面只在地图用填色画它的级别读到：准星在面内，或在吸附范围内靠近它的边（这时以最近一条边上的点计位置）。只画了边线或名称的面读不到，下一条的类除外。
- **限制区等区域**：[5.1](/developers/chartset/data/#5.1) E 组写“面”的各类虽然只画边线，地图从 8 级起另给它们一层透明填色（`TSEZNE` 用它自己的填色，见 [4.4](/developers/chartset/tiles/#4.4)），所以准星在面内或靠近它的边时同样读得到。
- **禁止事项领先**：这些面的 `RESTRN` 含 1、3、5、7、9、11、13、14、15（禁止锚泊、禁止捕鱼、禁止拖网、禁止进入、禁止疏浚、禁止潜水、禁止兴波、避航区、禁止施工）且准星在面内时：如果没有锁定的点、线或航标，也没有包含准星的危险物（`OBSTRN`、`UWTROC`、`WRECKS`）面或架空物（`BRIDGE`、`CBLOHD`、`PIPOHD` 及带净空属性的物标）面，读数由这个区域领先，显示它禁止的事项和所在处的水深，例如“禁止锚泊　30–50米”，详情打开这个区域；否则它排在“此处还有”的最前面。
- **点亮**：准星在上一条所说的面内、读得到它时，地图把当前画出的、同一物标类且 `RESTRN` 取值集合相同的区域边线叠画为加粗的品红实线，内部不涂，不计列表顺序和重复值，不论读数是否由它领先；准星离开后熄灭。只在吸附范围内靠近它的边、没有进到面内时不点亮。多个命中集合的边线都点亮，裁切口仍是开口；不需要新增派生字段，边线和属性要求见 [4.2](/developers/chartset/tiles/#4.2)。
- **航标的各部分**：坐标完全相同、并且都画出来了的航标本体、`LIGHTS`、`TOPMAR`、`DAYMAR`、`RTPBCN`、`RADRFL`、`RDOSTA`、`RADSTA` 点是同一座航标，准星把它们作为一个目标锁定和读出，各部分列在这座航标的详情里。
- **属性**：除 `DEPARE` 面外，详情列出物标携带的、S-57 物标目录认识的全部属性，包括 `INFORM`、`NINFOM`、`TXTDSC`、`SORDAT`、`SORIND`、`SCAMIN`；目录外的键不列出，`dh_surface_cell`、`dh_surface_cscl`（来源）除外。`SOUNDG` 的 `DEPTH` 用于水深读数。

## 5.3 地表类（Group 1 面）

S-57 App. B.1 §3.10.1 的 Group 1 是 `DEPARE DRGARE FLODOC HULKES LNDARE PONTON UNSARE` **且源几何为面**：读为脚下地表；其余有效地理物标为物标。
