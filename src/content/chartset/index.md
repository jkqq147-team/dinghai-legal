---
title: 定海海图集接入手册 v1
description: 外部生产方生成定海海图集的输入契约：目录、manifest、瓦片剖面与自检方法。
---

本文是外部生产方生成**定海海图集**的输入契约，包含目录、manifest、瓦片剖面与自检方法；样式、图标和字体不由生产方提供。[第 7 节](/developers/chartset/vector-mbtiles/)另列本地导入无 manifest 矢量 MBTiles 的首批规则；不改变已有 manifest 包的合同。

本文是正式版 v1，对应 manifest 格式 `1.x`（当前 `1.1`）和瓦片剖面 `1`。版本规则见[第 2.4 节](/developers/chartset/manifest/#2.4)：大版本一变，App 拒绝旧版本的海图集，生产方要按新版本重新生成。

文中“App 校验”指违反即在导入时拒绝的条件；“要求”指生产方须遵守的约定。当前可消费但不属于规范的写法单独注明，不保证后续支持；导入成功不等于全部瓦片可绘制、可点选。

## 0. 速览

- 海图集的内容根是一个文件夹：`manifest.json` + `chart.mbtiles`，可选再加一个只有一级的概览瓦片集 `overview.mbtiles`（[3.3](/developers/chartset/mbtiles/#3.3)）。可直接导入目录，也可将相同内容打成 ZIP；内容根可以在所选目录／ZIP 根部，或在单层纯包装目录内（[第 1 节](/developers/chartset/structure/)）。
- `chart.mbtiles` 是 MBTiles 1.3 矢量瓦片集（MVT，gzip 压缩，TMS 行号，Web Mercator 瓦片网格），metadata 里写 `dh_profile = 1`。
- 每个 source-layer 是一个 S-57 物标类缩写（`DEPARE`、`BOYLAT`、`WRECKS` …），属性用 S-57 属性缩写，值按 S-57 属性类型编码。
- 面状物标要画边线时，另写一条带 `dh_boundary = 1` 的线放在同一 source-layer。
- 最小样例：[`minimal-chartset.zip`](/developers/chartset/downloads/minimal-chartset.zip)，由参考生成脚本 [`generate-chartset-sample.py`](/developers/chartset/downloads/generate-chartset-sample.py) 生成（只用 Python 标准库，可当参考实现）。
- 自检：在真机 App 里导入海图集，走与用户相同的导入路径（[第 6 节](/developers/chartset/self-check/)）；测试 ZIP 时直接导入 ZIP，不以解压目录替代。

## 下载

| 文件 | 内容 |
| --- | --- |
| [`minimal-chartset.zip`](/developers/chartset/downloads/minimal-chartset.zip) | 最小样例海图集：包装目录 `minimal-chartset/` 内的 `manifest.json` 与 `chart.mbtiles`（[6.1](/developers/chartset/self-check/#6.1)）。 |
| [`generate-chartset-sample.py`](/developers/chartset/downloads/generate-chartset-sample.py) | 生成上述样例的参考脚本，只用 Python 标准库；输出是确定的，重跑得到相同的 `manifest.json` 与解码后的瓦片内容（[6.1](/developers/chartset/self-check/#6.1)）。 |

## 章节

1. [目录结构](/developers/chartset/structure/)：内容根、包装与内容识别
2. [manifest.json](/developers/chartset/manifest/)：示例、字段、id 与替换、版本规则
3. [chart.mbtiles：文件](/developers/chartset/mbtiles/)：metadata、tiles、overview.mbtiles
4. [chart.mbtiles：瓦片内容](/developers/chartset/tiles/)：坐标系与编码、图层与属性、几何、缩放级别
5. [数据清单](/developers/chartset/data/)：样式要画的物标类、点选会报告的物标、地表类
6. [自检](/developers/chartset/self-check/)：最小样例、在 App 里导入、报错对照、导入成功后应看到的结果
7. [本地导入无 manifest 的矢量 MBTiles](/developers/chartset/vector-mbtiles/)
