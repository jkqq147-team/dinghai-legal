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

对生产方提供的海图集，地图只画本节列出的类和 `dh_coverage`、`dh_area_symbol`（[4.2](/developers/chartset/tiles/#4.2)）；准星只报告地图上已绘制且符合点选资格的物标，其他目录内未绘制的物标不会报告（[5.2](/developers/chartset/data/#5.2)）。

**A. 水深与水域**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `DEPARE` | 面 | `DRVAL1`、`DRVAL2` | — |
| `DRGARE` | 面、边线 | `DRVAL1` | `DRVAL2`（水深） |
| `DEPCNT` | 线 | `VALDCO` | `dh_prev_valdco`（安全等深线） |
| `SOUNDG` | 点，**每个水深点一个点要素** | `DEPTH` | — |
| `CANALS` `RIVERS` | 面、线 | — | — |
| `DOCARE` `LOKBSN` `LAKARE` | 面 | — | — |
| `TS_FEB` `CURENT` | 点 | — | `ORIENT`（流向箭头）；`TS_FEB` 的 `CAT_TS`（涨潮流的箭头样式，涨、落潮流的读数标题）；`CURVEL`（流速）；`INFORM`（没有 `CURVEL` 时显示的说明） |

- `DEPARE` 缺上下限、`DRGARE` 缺下限，表示水深未知，不是实测安全水深。
- `SOUNDG` 的水深写在派生字段 `DEPTH`（米），不是 S-57 的 3D 坐标；一个多点测深物标须拆成多个点要素，每点带自己的 `DEPTH`，id 规则见 [4.1](/developers/chartset/tiles/#4.1)。
- 负值表示干出高度，不应由生产方改成绝对值。
- `TS_FEB`（潮流）、`CURENT`（海流）：`ORIENT` 是 0–360 的数值时，地图画一支指向 `ORIENT` 的箭头（水流流去的方向，照写 S-57 原值），箭头方向固定在地图上；没有或读不出 `ORIENT` 时不画箭头。`TS_FEB` 的 `CAT_TS` 为 1（涨潮流）时箭尾带单侧短羽，`CURENT` 的箭尾带成对的羽，其余是无羽的箭头。点下方显示 `CURVEL` 加“kn”，没有 `CURVEL` 时显示 `INFORM` 全文。准星读数和详情的标题由类别、流向和流速组成，不用名称，例如“涨潮流 · 45° · 2.0 节”；没有 `CURVEL` 时，流速取 `INFORM` 里形如 `2 KN`、`1-2 KN` 的部分。

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
| `TUNNEL` | 面、边线、线 | — | `CONVIS`（线醒目）；面为透明查询面（[4.4](/developers/chartset/tiles/#4.4)、[5.2](/developers/chartset/data/#5.2)） |
| `LNDRGN` | 点、线、面 | — | 名称（标注；没有名称时不显示） |

**C. 港口与建筑**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `HULKES` `DRYDOC` | 面、边线 | — | — |
| `PONTON` `FLODOC` `DAMCON` `DYKCON` `CAUSWY` `GATCON` | 面、边线、线 | — | — |
| `BRIDGE` | 面、边线、线 | — | `VERCSA`、`VERCLR`、`VERCCL`、`VERCOP`（净空）；`CATBRG`（开启桥）；见表下 |
| `SLCONS` | 面、边线、线、点 | — | `CONDTN`、`CATSLC`、`WATLEV`（线与面画法、状态标题、点显示档位与导航风险，见表下） |
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
| `CGUSTA` `SISTAW` `SISTAT` `CRANES` `FORSTC` `CTRPNT` `SLOGRD` | 点 | — | — |
| `NEWOBJ` | 点 | — | `dh_virtual_aid`（虚拟航标，见 [4.2](/developers/chartset/tiles/#4.2)） |

- **净空**：`BRIDGE`、`CBLOHD`、`PIPOHD` 的 `VERCSA`（安全净空）、`VERCLR`（净空）、`VERCCL`（关闭净空）、`VERCOP`（开启净空）按米读，写成米制浮点（[4.2](/developers/chartset/tiles/#4.2)）。App 不换算单位，也不看源数据的 `HUNI`、`HUNITS`；源数据不是米的，写入前换算成米。负值和读不出数字的值，地图和准星读数不写。
- 地图从 13 级起在物标旁写出净空，按安全净空、净空、关闭净空、开启净空的顺序，例如“净空 38.7米”。线（不含边线）在中点旁沿线写一行，各项用“ · ”隔开；一条线跨多张瓦片时，每张瓦片里的那一段各写一次；线短得放不下这行字时，这一级不写。`BRIDGE` 的面（大桥可以每一跨写一个面，各带自己的净空）把各项分行写在面内。这些文字与其他文字互相避让（[4.4](/developers/chartset/tiles/#4.4)）。
- `BRIDGE` 的 `CATBRG` 含 2、3、4、5、7、8（开启桥、平转桥、升降桥、竖转桥、吊桥、运渡桥）而没有 `VERCOP` 时，净空之后再写“开启桥”；只有这样的 `CATBRG`、没有净空属性时只写“开启桥”。
- 准星读数的标题是名称（没有名称时用物标类名）后接地图写的各项，例如“架空电缆 · 安全净空 36.25米 · 净空 40米”。详情把净空按同样的名字和顺序排在属性最前面，值带“米”。其他物标类带这些属性时，准星读数和详情也这样写，地图不写。
- 数值写到厘米，厘米以下舍去、不进位，例如 12.349 写作“12.34米”（与整厘米相差不到 0.5 微米的按整厘米算，所以 2.3 仍写作“2.3米”）；末尾的 0 不写，例如 40 写作“40米”。地图、准星读数和详情都这样写。
- **岸线建筑物（`SLCONS`）**：线和边线按 S-52 的 SLCONS03 依次分四支画：`CONDTN` 为 1、2（在建、废墟）画细虚线；否则 `CATSLC` 为 6、15、16（码头、实体码头、透空码头）画粗实线；否则 `WATLEV` 为 3、4（常淹没、干出）画粗虚线；其余（含 `WATLEV` 为 5 适淹）画普通实线。面只在画虚线的分支留空不填色（仍保留透明查询面供准星读取），画实线的填建筑色。属于虚线分支的 `SLCONS`，准星读数与详情标题会在名称（无名称时取 `CATSLC` 类别词，缺省用“岸线建筑物”）后附带 `CONDTN`（1、2）和 `WATLEV`（3、4）的状态词，例如“防波堤 · 常淹没”；画实线的不变。点状 `SLCONS` 若 `CATSLC` 为 1、2、3、4、5、7、14 或 `WATLEV` 为 1、3、4、5，会提升至不避让省略的显示档位，并提高准星导航风险优先级（起画级别仍见 [4.4](/developers/chartset/tiles/#4.4)）。

**D. 航标**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `BOYLAT` `BCNLAT` `BOYCAR` `BCNCAR` `BOYISD` `BCNISD` `BOYSAW` `BCNSAW` `BOYSPP` `BCNSPP` `LITFLT` `LITVES` | 单点 Point | — | `BOYSHP`、`BCNSHP`（形状）；`CATLAM`、`CATCAM`（类别）；`COLOUR`、`COLPAT`（颜色）；`MARSYS`（浮标制度）；名称（标注） |
| `TOPMAR` | 单点 Point | — | `TOPSHP`（形状）；`COLOUR`（颜色） |
| `LIGHTS` | 单点 Point | — | `COLOUR`（颜色）；`LITCHR`、`SIGGRP`、`SIGPER`（灯质）；`SECTR1`、`SECTR2`（扇区）；`CATLIT` 含 1 或 16 并带 `ORIENT`（定向灯的方向线）；`LITVIS`（被遮蔽、微弱扇区的画法）；`HEIGHT`、`VALNMR`（灯质后的灯高、射程）；`dh_has_body`（灯光位置）；`dh_sectors`、`dh_light_label`、`dh_light_colour`（同位置扇区合成一站） |
| `DAYMAR` | 点 | — | `TOPSHP`（日标牌形状）；`COLOUR`（颜色） |
| `RTPBCN` `RADRFL` `RDOSTA` `RADSTA` | 单点 Point | — | — |

- 真实颜色已知时写 `COLOUR`。
- 顶标、灯与浮标本体同位置时，分别写在各自的图层（`TOPMAR`、`LIGHTS`），与 S-57 一致。
- 灯与本体同位置（条件见 [4.2](/developers/chartset/tiles/#4.2)）时，App 转换 S-57 会在 `LIGHTS` 点上写入 `dh_has_body = 1`，外部生产方可选择写入以将灯光画在本体灯头处，也可不写；缺少该字段时，灯画成以自身位置为中心的灯色圆点。
- 扇区灯和定向灯：带 `SECTR1`、`SECTR2`（0–360，起止方位不同）的记录画成扇区；没有有效扇区、`CATLIT` 含 1 或 16 并带 `ORIENT`（0–360）的记录画成一条方向线。方位照写 S-57 原值（从海上看向灯的真方位）。`LITVIS` 含 7（遮蔽）的扇区留空不画，遮蔽的定向灯不画方向线；含 3 或 8（微弱、部分遮蔽）的画成虚线。扇区和方向线的颜色来自 `COLOUR`：红、绿各用本色，白、黄、橙、琥珀画成黄色；两种颜色交替的扇区分成内外两层；`COLOUR` 缺失、含其他颜色或超过两种颜色时画品红。其余 `LIGHTS` 记录是全向灯，照常画灯光符号。
- 同一位置的多条扇区、定向记录，App 转换 S-57 时合成一站，在主记录上写 `dh_sectors`、`dh_light_label`、`dh_light_colour`（规则和编码见 [4.2](/developers/chartset/tiles/#4.2)），地图画一组扇区、一条合并的标注。外部生产方可以照此写入，也可以不写；不写时每条记录各画各的扇区、概览圆点和灯质，同一位置的灯质不合并。
- `DAYMAR`、`RTPBCN`、`RADRFL`、`RDOSTA`、`RADSTA` 与航标本体、灯或顶标坐标完全相同时，准星把它们读作这座航标的一部分（[5.2](/developers/chartset/data/#5.2)）。

**E. 航路、限制区、管线**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `FAIRWY` `DWRTPT` `TWRTPT` | 面、边线 | — | `ORIENT`、`TRAFIC`（方向箭头、准星方位读数）；见表下 |
| `RCTLPT` | 面、边线 | — | `ORIENT`（方向箭头、准星方位读数）；`TRAFIC`（为 4 时准星标题不带方位）；见表下 |
| `PRCARE` `ISTZNE` `TSSRON` `TSSCRS` | 面、边线 | — | 见表下 |
| `TSSLPT` | 面 | — | `ORIENT`（方向箭头、准星方位读数）；`TRAFIC`（为 4 时准星标题不带方位）；见表下 |
| `TSEZNE` | 面 | — | — |
| `TSELNE` `TSSBND` | 线 | — | — |
| `DWRTCL` `RCRTCL` | 线 | — | `CATTRK`（实线或虚线）；`TRAFIC`（沿线的箭头或“?”）；`ORIENT`（沿线的方位、准星方位读数）；见表下 |
| `RECTRC` | 线、面、边线 | — | 线：同 `DWRTCL`；面：`ORIENT`、`TRAFIC`（方向箭头、准星方位读数）；见表下 |
| `NAVLNE` | 线 | — | `ORIENT`（准星方位读数；`CATNAV` 为 1、2 时沿线写方位） |
| `FERYRT` | 线、面、边线 | — | — |
| `RESARE` `MIPARE` `SPLARE` `CBLARE` `PIPARE` `FSHFAC` `HRBARE` `SUBTLN` `FSHGRD` `CTSARE` `ICNARE` | 面、边线 | — | 见表下 |
| `OSPARE` | 面、边线 | — | `CATPRA`（风电场符号）；见表下 |
| `MARCUL` | 面、边线、线、点 | — | 点：`WATLEV`（显示档位与导航风险）；见表下 |
| `CTNARE` `DMPGRD` `WEDKLP` | 面、边线、点 | — | 见表下 |
| `SNDWAV` | 面、边线、线、点 | — | 见表下 |
| `ACHBRT` | 面、边线、点 | — | `OBJNAM`（锚位编号）；见表下 |
| `ACHARE` | 面、边线、点 | — | 名称（标注）；见表下 |
| `PILBOP` | 面、边线、点 | — | 见表下 |
| `RDOCAL` | 线、点 | — | `ORIENT`（点的方向符号；`TRAFIC` 为 4 时画成双向）；`COMCHA`（频道） |
| `CBLSUB` | 线 | — | `CATCBL`（为 6 时较早显示，见 [4.4](/developers/chartset/tiles/#4.4)） |
| `PIPSOL` | 线 | — | — |
| `CBLOHD` `PIPOHD` | 线 | — | 净空属性（见 C 组表下） |

- 在生产方提供的海图集中，本组写“面”的类，除 `TSEZNE` 的填色和 `SNDWAV` 的沙波图案外，面本身不画，看得见的是边线（[4.2](/developers/chartset/tiles/#4.2)）；`TSSLPT` 不画边线，看得见的只有它的方向箭头或区域符号；准星靠面读到这个区域（[5.2](/developers/chartset/data/#5.2)），只写边线的读不到。
- `RESARE`、`CTNARE`、`ACHARE`、`MIPARE`、`DMPGRD`、`SPLARE`、`MARCUL`、`CBLARE`、`PIPARE`、`PRCARE`、`ISTZNE`、`OSPARE` 的面：`RESTRN`、`CATREA` 决定区域符号，`OSPARE` 的 `CATPRA` 只含 9 时是风电场符号；`TSSLPT` 的面：有 `ORIENT` 时是指向 `ORIENT` 的方向箭头，没有时是 `caution`；`TSSRON` 的面是 `roundabout`，`TSSCRS` 的面是 `caution`；`RCTLPT`、`DWRTPT`、`TWRTPT`、`FAIRWY`、`RECTRC` 的面：`ORIENT`、`TRAFIC` 决定单向或双向的方向箭头（`FAIRWY`、`RECTRC` 只画单向箭头，双向的不画），缺了时画“?”（`DWRTPT` 画竖直的双向箭头，`FAIRWY` 不画）（规则见 [4.2](/developers/chartset/tiles/#4.2)）。区域符号也决定准星“此处还有”里这个区域那一行的图标。海图集的区域符号要生产方写进 `dh_area_symbol`；无 manifest 的矢量 MBTiles 由 App 生成（[7.2](/developers/chartset/vector-mbtiles/#7.2)）。
- `TSSLPT`、`FAIRWY`、`DWRTPT`、`TWRTPT`、`RCTLPT`、`RECTRC`、`DWRTCL`、`RCRTCL`、`NAVLNE` 的 `ORIENT` 是 0–360 的数值时，准星读数和详情的标题是名称加方位；没有名称时，`TSSLPT` 用“通航分道”，其他类用物标类名，例如“通航分道 · 306°”“推荐航迹 · 270°”。其中面几何受 `TRAFIC` 限制：`FAIRWY`、`RECTRC`、`TWRTPT`、`DWRTPT` 的面仅在单向（`TRAFIC` 为 1、2、3）时带方位，`TSSLPT`、`RCTLPT` 的面在双向（`TRAFIC` 为 4）时不带方位；线几何不受 `TRAFIC` 限制。
- `RECTRC`、`DWRTCL`、`RCRTCL` 的线：`CATTRK` 为 1（依据固定标志）时画实线，否则画虚线。`TRAFIC` 为 1、2、3（单向）时沿线重复画单向箭头，**箭头指向线的数字化方向**（从第一个顶点到最后一个顶点），所以单向航线必须按通航方向数字化；`TRAFIC` 为 4（双向）时，`DWRTCL`、`RCRTCL` 画双向箭头，`RECTRC` 不画箭头；没有 `TRAFIC` 或取其他值时画正立的“?”。App 转换 S-57 时，会把带 `ORIENT` 的单向线调成 `ORIENT` 所指的方向；按 manifest 导入的海图集和无 manifest 的矢量 MBTiles，App 照写入的顺序画，不调整。`ORIENT` 是 0–360 的数值时，沿线写方位，例如“270°”；`NAVLNE` 只在 `CATNAV` 为 1、2（避险线、叠标线）时写。
- `SNDWAV` 的面另画沙波图案；`ACHBRT` 的面另在中央画锚位符号；`PILBOP` 的面另在中央画引航员登船处符号。`ACHBRT` 有名称时，准星读数和详情的标题是“锚位”加名称，例如“锚位 W2”；`RDOCAL` 有 `COMCHA` 时，标题是名称（没有名称时用“无线电报告点”）加频道，例如“无线电报告点 · VHF 12”。显示级别见 [4.4](/developers/chartset/tiles/#4.4)。
- 点状 `MARCUL` 若 `WATLEV` 为 1、3、4、5，会提升至不避让省略的显示档位，并提高准星导航风险优先级（起画级别仍见 [4.4](/developers/chartset/tiles/#4.4)）。
- 准星读得到的面：`RESTRN` 含禁止事项时，准星可由这个面领先（[5.2](/developers/chartset/data/#5.2)）。本组写“面”的类：准星“此处还有”里这个区域那一行带它的关键属性：`ACHARE` 的 `CATACH`、`MARCUL` 的 `CATMFA`、`FSHFAC` 的 `CATFIF`、`MIPARE` 的 `CATMPA`，没有时用 `RESTRN`；其他类先 `RESTRN`，再 `CATREA`。

**F. 危险物**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `WRECKS` | 面、边线、线、点 | — | `WATLEV`（水位）；`CATWRK`（符号）；`VALSOU`（水深）；点上和面上 `dh_drval1`（周围水深） |
| `OBSTRN` | 面、边线、线、点 | — | `WATLEV`（水位）；`CATOBS`（符号）；`VALSOU`（水深）；点上和面上 `dh_drval1`（周围水深）；面的画法见表下 |
| `UWTROC` | 点 | — | `WATLEV`（水位）；`VALSOU`（水深）；点上 `dh_drval1`（周围水深） |
| `SBDARE` | 面、边线、线、点 | — | `NATSUR`（点和面的底质；没有 `NATSUR` 时不写底质）；`WATLEV`（面的画法）；见表下 |

提供 `VALSOU` 时用实际米制深度；周围水深的派生字段 `dh_drval1` 见 [4.2](/developers/chartset/tiles/#4.2)，不能把危险物本身的深度写成周围水域深度。

- `OBSTRN`、`WRECKS` 的面也按孤立危险物规则判定，面状的也要写 `dh_drval1`：面状 `WRECKS` 不写时按在安全水域里处理，可能在面的中央画出孤立危险物符号；面状 `OBSTRN` 必须显式提供 `dh_drval1` 且不浅于安全水深才视为在安全水域内，不写时不会提升为孤立危险物，保留普通障碍物面样式（[4.4](/developers/chartset/tiles/#4.4) 表下）。非孤立危险物面的 `VALSOU` 写在面的中央，哪些写、哪些不写见 4.4 的表。
- `OBSTRN` 的面按 S-52 的 OBSTRN07 画，按下列顺序取第一个成立的：画成孤立危险物的，铺最浅一档水深区蓝色的半透明水洗（非不透明填色），铺碍航图案（“#”），画警示色点线边线；有 `VALSOU` 的不填色，露出下面的水深区，`VALSOU` 不超过用户设置的安全水深时画点线边线，更深时画灰色虚线边线；`CATOBS` 为 6（不良区）的不填色，只铺碍航图案，画点线边线；其余按 `WATLEV`：1、2（干出）填比陆地深一档的赭色，画粗实线边线；4（时没时现）填干出水深区的绿色，画粗虚线边线；其他值或未写的水下面铺最浅一档水深区蓝色的半透明水洗（非不透明填色），画点线边线。
- `CATOBS` 为 7（不良底质）、8（拦冰栅）、10，或 `WATLEV` 为 7 的 `OBSTRN` 无论点、面都不画成孤立危险物。其中面不按上条画：不填色，边线不画危险物的点线，改画虚线，面的中央画符号，也不写水深。
- `WRECKS` 的面按 S-52 的 WRECKS05 画，不铺碍航图案。填色：有 `VALSOU` 的不填色；没有的按 `WATLEV` 不透明填色（1、2 填比陆地深一档的赭色，4 填干出水深区的绿色，其他值或未写填最浅一档水深区的蓝色），画成孤立危险物的也一样。边线：画成孤立危险物的画点线；有 `VALSOU` 的，不超过安全水深时画点线，更深时画虚线；其余按 `WATLEV`，1、2 画粗实线，4 画粗虚线，其他值或未写画点线。
- `OBSTRN`、`WRECKS` 面的填色和碍航图案画在水深区（包括浅水图案）、疏浚区边线，`CANALS`、`DOCARE`、`LOKBSN`、`RIVERS`、`LAKARE` 的面，`CANALS`、`RIVERS` 的线和 `LNDARE` 的面之上，所以落在船坞、船闸、运河、河流、湖泊或陆地面内的危险物面照样看得到填色；其他各类压在它上面，例如 `LNDARE` 的点（小岛），陆上的建筑物等背景面和陆上的线，构筑物，等深线，海缆和管道，航路和限制区的线。危险物面的边线、符号和水深画在这些之上。
- `SBDARE` 的面：`WATLEV` 为 3 或 4 时画细虚线边线；其中 `WATLEV` 为 4、`NATSUR` 为 9、11 或 14（岩、熔岩、珊瑚，单值）的面画礁石图案，其余在面的中央写底质。`SBDARE` 的线画细实线。

**G. 名称**

| 物标类 | 几何 | 必须 | 可选 |
| --- | --- | --- | --- |
| `SEAARE` | 点、线、面 | — | 名称（标注；没有名称时不显示）；`CATSEA`（类别） |

## 5.2 点选会报告的物标

- **资格**：只报告 S-57 目录内的地理物标；元物标（`M_*`）、集合物标（`C_*`）、制图物标不报告。5.3 的七类仅源几何为面时是地表，其余有效地理物标可报告。`dh_boundary = 1` 的边线不读：面只经由它自己的面要素读到。
- **读地图画出的**：准星只读当前缩放下地图实际画出的要素，用的就是画它时的属性；[4.4](/developers/chartset/tiles/#4.4) 的显示级别和文字避让都算在内。面只在地图用填色画它的级别读到：准星在面内，或在吸附范围内靠近它的边（这时以最近一条边上的点计位置）。只画了边线或名称的面读不到，下一条的类除外。
- **限制区等区域与隧道面**：[5.1](/developers/chartset/data/#5.1) E 组写“面”的各类中，`TSEZNE` 从 7.5 级起淡入自身填色（7.5 级起可读），`SNDWAV` 的沙波图案填色无最低级别限制（任意级别可读，边线 7.5 级起淡入），其余各类只画边线（`TSSLPT` 连边线也不画）、由地图从 8 级起另给一层透明查询面；`TUNNEL` 的面同样不绘填色，由地图从 9 级起另给一层透明查询面。所以准星在面内或靠近它们的边时同样读得到（[4.4](/developers/chartset/tiles/#4.4)）。
- **包含面的领先顺序（禁止事项与航路面）**：没有锁定的点、线或航标时，包含准星且准星读得到的面按以下顺序领先于单纯水深：第一档是架空物（`BRIDGE`、`CBLOHD`、`PIPOHD` 及带净空属性的物标）面和在当前安全水深下构成航行危害的危险物（`OBSTRN`、`WRECKS`）面——其中 `OBSTRN` 的 `CATOBS` 为 7（不良底质）不算航行危害，漂浮物（`WATLEV` 为 7）与 `CATOBS` 为 8（拦冰栅）、10 始终算，其余 `OBSTRN`、`WRECKS` 须其水深（`VALSOU`，无 `VALSOU` 时按 S-52 缺省深度）不超过安全水深。第二档是带禁止事项的面（包括带 `RESTRN` 的 `DRGARE` 疏浚区等）：其 `RESTRN` 含 1、3、5、7、9、11、13、14、15、16、18、20、22、23、24、25、26（禁止锚泊、禁止捕鱼、禁止拖网、禁止进入、禁止疏浚、禁止潜水、禁止兴波、避航区、禁止施工、禁止排放、禁止工业或矿产勘探开发、禁止钻探、禁止移走历史文物、禁止货物过驳、禁止海底拖曳、禁止停船、禁止登陆）时，读数由这个区域领先，显示它禁止的事项和所在处的水深，例如“禁止停船　30–50米”，详情打开这个区域；有锁定物标或第一档包含面时，它排在“此处还有”的最前面。17、19、21、27（限制排放、限制工业或矿产勘探开发、限制钻探、限速）是限制类，不按这一档领先；这个面自己属于第一档时，读数按危险物或架空物写（净空照 [5.1](/developers/chartset/data/#5.1) C 组写出），禁止事项在它的详情里。第三档是航路面（`FAIRWY`、`TSSLPT`、`TSSRON`、`TSSCRS`、`TWRTPT`、`DWRTPT`、`RCTLPT`、`ISTZNE`、`PRCARE`）：无锁定物标且无前两档包含面时，由包含准星的航路面领先于单纯水深。
- **航标的各部分**：坐标完全相同、并且都画出来了的航标本体、`LIGHTS`、`TOPMAR`、`DAYMAR`、`RTPBCN`、`RADRFL`、`RDOSTA`、`RADSTA` 点是同一座航标，准星把它们作为一个目标锁定和读出，各部分列在这座航标的详情里。
- **属性**：除 `DEPARE` 面外，详情列出物标携带的、S-57 物标目录认识的全部属性，包括 `INFORM`、`NINFOM`、`TXTDSC`、`SORDAT`、`SORIND`、`SCAMIN`；目录外的键不列出，`dh_surface_cell`、`dh_surface_cscl`（来源）除外。`SOUNDG` 的 `DEPTH` 用于水深读数。

## 5.3 地表类（Group 1 面）

S-57 App. B.1 §3.10.1 的 Group 1 是 `DEPARE DRGARE FLODOC HULKES LNDARE PONTON UNSARE` **且源几何为面**：读为脚下地表；其余有效地理物标为物标。
