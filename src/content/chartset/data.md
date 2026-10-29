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

地图只画本节列出的类和 `dh_coverage`；其他目录内物标不画，但点选仍可能报告（[5.2](/developers/chartset/data/#5.2)）。

**A. 水深与水域**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `DEPARE` | 面 | `DRVAL1`、`DRVAL2` | — |
| `DRGARE` | 面、边线 | `DRVAL1` | `DRVAL2`（水深） |
| `DEPCNT` | 线 | `VALDCO` | `dh_prev_valdco`（安全等深线） |
| `SOUNDG` | 点，**每个水深点一个点要素** | `DEPTH` | — |
| `CANALS` `DOCARE` `LOKBSN` `LAKARE` `RIVERS` | 面 | — | — |

- `DEPARE` 缺上下限、`DRGARE` 缺下限，表示水深未知，不是实测安全水深。
- `SOUNDG` 的水深写在派生字段 `DEPTH`（米），不是 S-57 的 3D 坐标；一个多点测深物标须拆成多个点要素，每点带自己的 `DEPTH`，id 规则见 [4.1](/developers/chartset/tiles/#4.1)。
- 负值表示干出高度，不应由生产方改成绝对值。

**B. 陆地与岸线**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `LNDARE` | 面、点 | — | 名称（读数） |
| `COALNE` | 线 | — | — |
| `BUAARE` `RUNWAY` | 面、边线 | — | `CONVIS`（醒目）；`BUAARE` 名称（标注） |
| `BUISGL` | 面、边线、点 | — | `CONVIS`（醒目） |
| `ROADWY` `RAILWY` `LNDELV` | 线 | — | `CONVIS`（醒目） |
| `LNDRGN` | 点、线、面 | — | 名称（标注；没有名称时不显示） |

**C. 港口与建筑**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `PONTON` `FLODOC` `HULKES` `DRYDOC` | 面、边线 | — | — |
| `DAMCON` `DYKCON` `CAUSWY` `SLCONS` `BRIDGE` | 面、边线、线 | — | — |
| `HRBFAC` | 点、线、面 | — | `CATHAF`（符号）；名称（标注；线、面没有名称时不显示） |
| `SMCFAC` | 点、线、面 | — | 名称（标注；线、面没有名称时不显示） |
| `BERTHS` | 点、线、面 | — | 名称（标注；没有名称时不显示） |
| `MORFAC` | 点 | — | `CATMOR`（符号）；`COLOUR`、`COLPAT`（颜色） |
| `PILPNT` | 点 | — | — |
| `PYLONS` | 点 | — | `CATPYL`（符号） |
| `LNDMRK` | 点 | — | `CATLMK`（符号）；`CONVIS`（醒目） |
| `SILTNK` | 点 | — | `CATSIL`（符号）；`CONVIS`（醒目） |
| `OFSPLF` `WEDKLP` `WATTUR` `FOGSIG` `ACHBRT` | 点 | — | — |
| `CGUSTA` `PRDARE` `NEWOBJ` `SNDWAV` `PILBOP` `DMPGRD` `SISTAW` `SISTAT` | 点 | — | — |

**D. 航标**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `BOYLAT` `BCNLAT` `BOYCAR` `BCNCAR` `BOYISD` `BCNISD` `BOYSAW` `BCNSAW` `BOYSPP` `BCNSPP` `LITFLT` `LITVES` | 单点 Point | — | `BOYSHP`、`BCNSHP`（形状）；`CATLAM`、`CATCAM`（类别）；`COLOUR`、`COLPAT`（颜色）；`MARSYS`（浮标制度）；名称（标注） |
| `TOPMAR` | 单点 Point | — | `TOPSHP`（形状）；`COLOUR`（颜色） |
| `LIGHTS` | 单点 Point | — | `COLOUR`（颜色）；`LITCHR`、`SIGGRP`、`SIGPER`（灯质） |

- 真实颜色已知时写 `COLOUR`。
- 顶标、灯与浮标本体同位置时，分别写在各自的图层（`TOPMAR`、`LIGHTS`），与 S-57 一致。

**E. 航路、限制区、管线**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `FAIRWY` `PRCARE` `TSSLPT` `DWRTPT` | 边线 | — | — |
| `TSEZNE` | 面 | — | — |
| `TSELNE` `TSSBND` `DWRTCL` `RECTRC` `RCRTCL` `NAVLNE` `FERYRT` | 线 | — | — |
| `RESARE` `CTNARE` `MIPARE` `DMPGRD` `SPLARE` `MARCUL` `CBLARE` `PIPARE` | 边线 | — | — |
| `ACHARE` | 边线、点 | — | 名称（标注） |
| `CBLSUB` `PIPSOL` `CBLOHD` `PIPOHD` | 线 | — | — |

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

- **资格**：只报告 S-57 目录内的地理物标；元物标（`M_*`）、集合物标（`C_*`）、制图物标不报告。5.3 的七类仅源几何为面时是地表，其余有效地理物标可报告。`dh_boundary = 1` 的边线按它的源面判定，不作为线物标。
- **属性**：除 `DEPARE` 面外，详情列出物标携带的、S-57 物标目录认识的全部属性，包括 `INFORM`、`NINFOM`、`TXTDSC`、`SORDAT`、`SORIND`、`SCAMIN`；目录外的键不列出，`dh_surface_cell`、`dh_surface_cscl`（来源）除外。`SOUNDG` 的 `DEPTH` 用于水深读数。

## 5.3 地表类（Group 1 面）

S-57 App. B.1 §3.10.1 的 Group 1 是 `DEPARE DRGARE FLODOC HULKES LNDARE PONTON UNSARE` **且源几何为面**：读为脚下地表；其余有效地理物标为物标。
