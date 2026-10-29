---
title: 5. 数据清单
description: 样式要画的物标类、点选会报告的物标与地表类。
---

定海只用瓦片里的两样东西：**样式画出来的**和**点选报告出来的**。下面按这两条列出每类物标要什么。

术语：

- **必填**：缺了这一项，这一类物标画不出来、画错，或点选读不到它的水深或名称。
- **可选**：有就用（画符号、写标注、详情里列出），没有也能画、能点选。
- **忽略**：App 不读，可以不写。
- “名称”指 `NOBJNM`（非空时，中文界面优先）或 `OBJNAM`。

## 5.1 样式要画的物标类

起始缩放是图层完全显示的级别；点符号与航标在起始缩放前半级淡入。

**A. 水深与水域**

| 物标类 | 几何 | 必填 | 可选 | 起始缩放 |
| --- | --- | --- | --- | --- |
| `DEPARE` | 面 | `DRVAL1`、`DRVAL2` | — | 0 |
| `DRGARE` | 面、边线 | `DRVAL1` | `DRVAL2` | 0 |
| `DEPCNT` | 线 | `VALDCO` | — | 0（数字标注 13） |
| `SOUNDG` | 点，**每个水深点一个点要素** | `DEPTH` | — | 11 |
| `CANALS` `DOCARE` `LOKBSN` `LAKARE` `RIVERS` | 面 | — | — | 0 |

- `DEPARE` 需要上下限，`DRGARE` 需要下限；缺值表示未知，不是实测安全水深。着色遵循 S-52 DEPARE01 缺省值，点选只报告提供的范围，不把着色缺省值当实测值。
- `DEPCNT` 的安全等深线派生属性见 [4.2](/developers/chartset/tiles/#4.2)；未提供 `dh_prev_valdco` 时不会被选为安全等深线。
- `SOUNDG` 的水深写在派生字段 `DEPTH`（米，浮点），不是 S-57 的 3D 坐标；一个多点测深物标须拆成多个点要素，每点带自己的 `DEPTH`。拆开的点不能共用 feature id，各用不同的 id 或都不写（[4.1](/developers/chartset/tiles/#4.1)）。
- 深度数值当前可为整数、浮点或数字字符串，推荐浮点；负值表示干出高度，不应由生产方改成绝对值。

**B. 陆地与岸线**

| 物标类 | 几何 | 必填 | 可选 | 起始缩放 |
| --- | --- | --- | --- | --- |
| `LNDARE` | 面、点 | — | 名称（准星读数） | 0 |
| `COALNE` | 线 | — | — | 0 |
| `BUAARE` `BUISGL` `RUNWAY` | 面、边线 | — | `CONVIS`（`1` 为显著，保留醒目色）；`BUAARE` 名称（起始 11） | 0 |
| `ROADWY` `RAILWY` `LNDELV` | 线 | — | `CONVIS` | 12 |
| `LNDRGN` | 点、线、面（名称） | — | 名称 | 11 |

**C. 港口与建筑**

| 物标类 | 几何 | 必填 | 可选 | 起始缩放 |
| --- | --- | --- | --- | --- |
| `PONTON` `FLODOC` `HULKES` `DRYDOC` | 面、边线 | — | — | 0 |
| `DAMCON` `DYKCON` `CAUSWY` `SLCONS` `BRIDGE` | 面、边线、线 | — | — | 0 |
| `HRBFAC` | 点符号；名称在点、线、面上 | — | `CATHAF`（符号）；名称（起始 13） | 13 |
| `SMCFAC` | 点；名称在点、线、面上 | — | 名称（起始 13） | 13 |
| `BERTHS` | 点、线、面（名称） | — | 名称 | 15 |
| `MORFAC` | 点 | — | `CATMOR`、`COLOUR`、`COLPAT`（选符号；系泊浮多色按横带） | 13 |
| `PILPNT` `BUISGL` | 点 | — | `BUISGL` 的 `CONVIS` | 14 |
| `PYLONS` | 点 | — | `CATPYL` | 13 |
| `LNDMRK` `SILTNK` | 点 | — | `CATLMK` / `CATSIL`，`CONVIS` | 12 |
| `OFSPLF` | 点 | — | — | 12 |
| `WEDKLP` `WATTUR` `FOGSIG` `ACHBRT` | 点 | — | — | 13 |
| `CGUSTA` `PRDARE` `NEWOBJ` `SNDWAV` `PILBOP` `DMPGRD` `SISTAW` `SISTAT` | 点 | — | — | 13 |

**D. 航标**

| 物标类 | 几何 | 必填 | 可选 | 起始缩放 |
| --- | --- | --- | --- | --- |
| `BOYLAT` `BCNLAT` `BOYCAR` `BCNCAR` `BOYISD` `BCNISD` `BOYSAW` `BCNSAW` `BOYSPP` `BCNSPP` `LITFLT` `LITVES` | 单点 Point | — | `BOYSHP`、`BCNSHP`、`CATLAM`、`CATCAM`、`COLOUR`、`COLPAT`、`MARSYS`（选形状与颜色）；名称（起始 15） | 11.5 起淡入，12 完全显示 |
| `TOPMAR` | 单点 Point | — | `TOPSHP`、`COLOUR` | 同上 |
| `LIGHTS` | 单点 Point | — | `COLOUR`（光晕与概览圆点颜色）；`LITCHR`、`SIGGRP`、`SIGPER`（灯质标注，起始 12；无 `LITCHR` 不标） | z8–12 为概览圆点；光晕 11.5 起淡入 |

航标的形状和颜色由这些属性决定，缺了画成通用符号，不会不画：浮标、立标完全不写 `COLOUR`（且类别定不出颜色）的，本体画成单色橙（浮标）或单色褐（立标），表示颜色未写；写了但乱码或画不出的颜色画中性灰。真实颜色已知时请写 `COLOUR`。浮标顶标、灯与浮标本体同位置时分别写在各自的图层（`TOPMAR`、`LIGHTS`），与 S-57 一致。

**E. 航路、限制区、管线**

| 物标类 | 几何 | 必填 | 可选 | 起始缩放 |
| --- | --- | --- | --- | --- |
| `FAIRWY` `PRCARE` `TSSLPT` `DWRTPT` | 边线 | — | — | 0 |
| `TSEZNE` | 面 | — | — | 0 |
| `TSELNE` `TSSBND` `DWRTCL` `RECTRC` `RCRTCL` `NAVLNE` `FERYRT` | 线 | — | — | 0 |
| `RESARE` `CTNARE` `MIPARE` `DMPGRD` `SPLARE` `MARCUL` `CBLARE` `PIPARE` | 边线 | — | — | 0 |
| `ACHARE` | 边线；点 | — | 名称（起始 13） | 0（点符号 13） |
| `CBLSUB` `PIPSOL` `CBLOHD` `PIPOHD` | 线 | — | — | 0 |

**F. 危险物**

| 物标类 | 几何 | 必填 | 可选 | 起始缩放 |
| --- | --- | --- | --- | --- |
| `WRECKS` | 面、边线、线、点 | — | `WATLEV`（面的颜色）；`CATWRK`（点符号）；`VALSOU`（点旁水深） | 0（点符号 12，孤立危险 8，仅靠保守缺省的孤立危险 12；点旁水深 12） |
| `OBSTRN` | 面、边线、线、点 | — | `WATLEV`；`CATOBS`（点符号）；`VALSOU`（点旁水深） | 0（点符号 12，孤立危险 8，仅靠保守缺省的孤立危险 12；点旁水深 12） |
| `UWTROC` | 面、边线、线、点 | — | `WATLEV`；`VALSOU`（点旁水深） | 0（点符号 12，孤立危险 8，仅靠保守缺省的孤立危险 12；点旁水深 12） |
| `SBDARE` | 点 | — | `NATSUR`（底质缩写；无 `NATSUR` 不画） | 15 |

提供 `VALSOU` 时用实际米制深度；周围水深的派生字段 `dh_drval1` 见 [4.2](/developers/chartset/tiles/#4.2)，不能把危险物本身的深度写成周围水域深度。缺深度或周围水深的危险物不保证按非危险物显示。

点符号的起始缩放指完全显示，前半级淡入。按安全水深判为孤立危险的点（洋红圆底内画本物形状）提前到 z7.5 淡入、z8 完全显示，z12 以下保持 z12 的大小，不因相互碰撞省略，密集时可能互相遮挡。例外是仅靠保守缺省才成为孤立危险的点，即同时满足：不写 `VALSOU`；不写 `dh_drval1`；`WATLEV` 不写或为 3；`WRECKS` 另需 `CATWRK` 不是 1、2、4、5（不写也算），`OBSTRN` 另需 `CATOBS` 不是 6（不写也算），`UWTROC` 无附加条件。这些点自身和周围的水深都不明，按其余危险物的时机 z11.5 淡入、z12 完全显示；它们仍是孤立危险，显示后仍画洋红圆底，点选读数仍是孤立危险图标。`VALSOU`、`dh_drval1`、`WATLEV` 看的是有没有写：写成 0、空串或未知代码都算写了，`dh_drval1` 为 −1 也算写了，`WATLEV` 写了且不是 3 就不满足；任一条不满足的孤立危险照常 z8 显示。其余危险物点符号仍 z11.5 淡入、z12 完全显示，点旁水深仍 z12 起。低缩放只能画出瓦片里已有的点：外部海图集在 z8–11 级没有写入的危险物不会显示。

**G. 名称**

| 物标类 | 几何 | 可选 | 起始缩放 |
| --- | --- | --- | --- |
| `SEAARE` | 点、线、面（名称） | 名称；`CATSEA` | z10–12 只标有 `CATSEA` 的，12 起全部 |

名称层（本组 `SEAARE` 及前面各组的 `LNDRGN`、`BUAARE`、`ACHARE`、`HRBFAC`、`SMCFAC`、`BERTHS`）只要求有名称且不是 `dh_boundary` 派生边线，不过滤点、线、面几何；例如带名称的 `BERTHS` 线也进入名称层。

本节列出的类以外，样式不画任何东西。

## 5.2 点选会报告的物标

点选报告的输入范围：

- **资格**：只报告 S-57 目录内的地理物标；元物标（`M_*`）、集合物标（`C_*`）、制图物标不报告。5.3 的七类仅源几何为面时是地表，其余有效地理物标可报告；点可进读数，线／面可进详情。`dh_boundary = 1` 是源面的派生边线，按面判定，不作为线物标。
- **排序**：资格通过之后才排序：危险物（`WRECKS`、`OBSTRN`、`UWTROC`）> 航标（目录内的 `BOY*`、`BCN*`、`LIGHTS`、`TOPMAR`、`FOGSIG` 等）> 航行相关（锚地、航道、航线等）> 其余目录地理物标。前缀不授予资格，`BOYFAKE` 等目录外名字不会被读成航标。
- **属性**：按规范命名的 S-57 物标，详情列出它携带的、S-57 物标目录认识的**全部**属性，包括 `INFORM`、`NINFOM`、`TXTDSC`、`SORDAT`、`SORIND`、`SCAMIN`；枚举值按目录翻译成文字，列表逐项翻译。**例外是 external 海图集的 `DEPARE` 面：详情被合成为区间水深，其他目录属性（即使写了 `INFORM` 等）不显示，原 `DEPARE` 面也不另列一项。**除这个例外外，其余 S-57 属性都是“可选”：写了才显示，点、线、面一样。
- **忽略与派生字段例外**：按规范命名的 S-57 物标，目录以外的属性键通常不显示；`DEPTH` 用于水深读数，`dh_surface_cell`、`dh_surface_cscl` 按 4.2 显示为“来源单元”“编辑比例尺”，`DEPARE` 的合成水深详情也可带这两个来源字段。目录以外的图层名不报告；违反大写命名要求的小写层名可能走通用详情（[4.2](/developers/chartset/tiles/#4.2)），不适用这里的目录属性解释。

## 5.3 地表类（Group 1 面）

S-57 App. B.1 §3.10.1 的 Group 1 是 `DEPARE DRGARE FLODOC HULKES LNDARE PONTON UNSARE` **且源几何为面**（“…if they are of type area”）：读为脚下地表；其余有效地理物标为物标，不以样式是否画它决定资格。地表重叠或落在查询容差内时，先取实际包含准星的面，再按浮体 > 陆地 > 水的顺序仲裁；`PONTON` 等面仍有详情。
