# 调色板推荐指南 / Palette Recommendation Guide

> 本文档提供基于使用场景的调色板推荐决策矩阵，帮助选择最适合的 paletteer 调色板。

---

## 快速决策树 / Quick Decision Tree

```
你的数据是什么类型？
│
├─ 连续数值（温度、密度、高度等）
│   ├─ 需要色盲友好？
│   │   ├─ 是 → viridis::viridis / scico::batlow / scico::davos
│   │   └─ 否 → rcartocolor::Sunset / viridis::magma / viridis::plasma
│   │
│   └─ 需要灰度/印刷友好？
│       ├─ 是 → scico::oslo / RColorBrewer::Greys
│       └─ 否 → viridis::inferno / scico::hawaii
│
├─ 发散数值（偏差、正负值、温度异常等）
│   ├─ 需要色盲友好？
│   │   ├─ 是 → scico::vik / scico::berlin / scico::broc
│   │   └─ 否 → RColorBrewer::RdBu / RColorBrewer::PuOr
│   │
│   └─ 需要经典学术风格？
│       └─ RColorBrewer::RdBu / RColorBrewer::BrBG / scico::roma
│
└─ 离散类别（物种、分组、类型等）
    ├─ 需要色盲友好？
    │   ├─ 是 → RColorBrewer::Dark2 / rcartocolor::Safe
    │   └─ 否 → nord::aurora / wesanderson::FantasticFox1
    │
    ├─ 学术论文/期刊？
    │   ├─ 是 → ggsci::npg / ggsci::lancet / ggsci::jco / ggsci::nejm
    │   └─ 否 → 继续判断
    │
    ├─ 需要多少种颜色？
    │   ├─ ≤8 → RColorBrewer::Dark2 / RColorBrewer::Set2
    │   ├─ ≤12 → RColorBrewer::Set3 / RColorBrewer::Paired
    │   └─ >12 → ggsci::ucscgb / Polychrome 包
    │
    └─ 美学风格偏好？
        ├─ 电影艺术 → wesanderson::* / ghibli::* / MetBrewer::*
        ├─ 自然风景 → nationalparkcolors::* / MetBrewer::Hiroshige
        ├─ 简约现代 → nord::* / rcartocolor::Bold
        └─ 复古怀旧 → NineteenEightyR::* / vapoRwave::*
```

---

## 按场景推荐 / By Scenario

### 1. 学术论文 / Academic Publication

| 推荐调色板 | 类型 | 颜色数 | 色盲友好 | 说明 |
|-----------|------|--------|---------|------|
| `ggsci::npg` | discrete | 10 | ✗ | Nature 期刊风格，学术论文首选 |
| `ggsci::lancet` | discrete | 9 | ✗ | Lancet 期刊风格，医学论文 |
| `ggsci::aaas` | discrete | 10 | ✗ | Science 期刊风格 |
| `ggsci::jco` | discrete | 10 | ✗ | 临床肿瘤学期刊 |
| `ggsci::nejm` | discrete | 8 | ✗ | NEJM 期刊风格 |
| `RColorBrewer::Dark2` | discrete | 8 | ✓ | 经典色盲安全，论文常客 |
| `scico::batlow` | continuous | ∞ | ✓ | 感知均匀连续型，顶刊推荐 |
| `viridis::viridis` | continuous | ∞ | ✓ | 学术界默认连续型 |

**R 代码示例:**
```r
library(paletteer)
library(ggplot2)

# Nature 风格散点图
ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Species)) +
  geom_point(size = 3) +
  scale_color_paletteer_d("ggsci::npg") +
  theme_minimal()

# viridis 连续型热力图
ggplot(faithfuld, aes(waiting, eruptions, fill = density)) +
  geom_raster() +
  scale_fill_paletteer_c("viridis::viridis")
```

---

### 2. 商务报告 / Business Report

| 推荐调色板 | 类型 | 颜色数 | 色盲友好 | 印刷友好 | 说明 |
|-----------|------|--------|---------|---------|------|
| `RColorBrewer::Blues` | sequential | 9 | ✓ | ✓ | 商务蓝色渐变 |
| `RColorBrewer::Set2` | qualitative | 8 | ✗ | ✗ | 柔和专业分类色 |
| `rcartocolor::Safe` | qualitative | 9 | ✓ | ✗ | 色盲安全分类 |
| `rcartocolor::Bold` | qualitative | 11 | ✗ | ✗ | 高对比度商务分类 |
| `RColorBrewer::RdBu` | diverging | 11 | ✓ | ✓ | 正负值对比 |
| `viridis::cividis` | continuous | ∞ | ✓ | ✓ | 印刷友好连续型 |

---

### 3. 数据可视化 / General Data Visualization

| 推荐调色板 | 类型 | 颜色数 | 说明 |
|-----------|------|--------|------|
| `viridis::magma` | continuous | ∞ | 热力图首选 |
| `scico::berlin` | continuous | ∞ | 发散数据首选 |
| `RColorBrewer::Set1` | qualitative | 9 | 高对比度分类 |
| `nord::frost` | qualitative | 4 | 冷色系分类 |
| `nord::aurora` | qualitative | 5 | 暖色系分类 |
| `rcartocolor::Vivid` | qualitative | 11 | 鲜艳分类 |

---

### 4. 艺术创意 / Artistic & Creative

| 推荐调色板 | 类型 | 颜色数 | 说明 |
|-----------|------|--------|------|
| `wesanderson::GrandBudapest1` | qualitative | 5 | 粉紫柔美 |
| `wesanderson::Zissou1` | qualitative | 5 | 红黄蓝活力 |
| `wesanderson::Moonrise1` | qualitative | 5 | 黄粉绿梦幻 |
| `ghibli::MarnieLight1` | qualitative | 10 | 暖色渐变 |
| `ghibli::PonyoLight` | qualitative | 10 | 蓝色海洋 |
| `MetBrewer::Monet` | qualitative | 11 | 印象派柔色 |
| `MetBrewer::Klimt` | qualitative | 8 | 金色华丽 |
| `MetBrewer::Hiroshige` | qualitative | 7 | 浮世绘暖色 |
| `nationalparkcolors::CraterLake` | qualitative | 7 | 深蓝湖泊 |
| `nationalparkcolors::Glacier` | qualitative | 7 | 冰川色彩 |

---

### 5. 自然主题 / Nature & Landscape

| 推荐调色板 | 类型 | 颜色数 | 说明 |
|-----------|------|--------|------|
| `nationalparkcolors::Arches` | qualitative | 7 | 沙漠红岩 |
| `nationalparkcolors::Saguaro` | qualitative | 6 | 仙人掌绿橙 |
| `nationalparkcolors::Redwoods` | qualitative | 7 | 红木森林 |
| `nationalparkcolors::Everglades` | qualitative | 7 | 湿地绿色 |
| `MetBrewer::Hiroshige` | qualitative | 7 | 日本风景画 |
| `MetBrewer::Pissarro` | qualitative | 12 | 绿色田园 |
| `calecopal::*` | qualitative | varies | 加州植物 |
| `soilpalettes::*` | qualitative | varies | 土壤剖面 |

---

### 6. 色盲友好 / Colorblind-Safe

**重要:** 约 8% 的男性有某种形式的色盲。发布可视化时应优先选择色盲友好调色板。

| 推荐调色板 | 类型 | 类别 | 说明 |
|-----------|------|------|------|
| `viridis::viridis` | continuous | sequential | 最知名的色盲安全连续型 |
| `viridis::cividis` | continuous | sequential | 专为色盲优化 |
| `scico::batlow` | continuous | sequential | 感知均匀 |
| `scico::vik` | continuous | diverging | 蓝橙发散，色盲安全 |
| `scico::berlin` | continuous | diverging | 蓝红发散 |
| `RColorBrewer::Dark2` | discrete | qualitative | 经典色盲安全分类 |
| `RColorBrewer::Set2` | discrete | qualitative | 柔和分类 |
| `rcartocolor::Safe` | discrete | qualitative | 专为色盲设计 |
| `RColorBrewer::Blues` | discrete | sequential | 单色渐变 |
| `RColorBrewer::RdBu` | discrete | diverging | 红蓝发散 |

---

### 7. 印刷友好 / Print-Friendly

**注意:** 印刷时颜色可能在 CMYK 转换中失真。以下调色板在印刷中表现较好。

| 推荐调色板 | 类型 | 说明 |
|-----------|------|------|
| `RColorBrewer::Dark2` | discrete | 深色高对比，印刷清晰 |
| `RColorBrewer::Greys` | discrete | 纯灰度 |
| `scico::oslo` | continuous | 黑白灰度连续型 |
| `viridis::cividis` | continuous | 蓝黄连续，印刷友好 |
| `RColorBrewer::Blues` | discrete | 单色蓝渐变 |
| `RColorBrewer::BrBG` | discrete | 棕绿发散 |
| `nord::polarnight` | discrete | 深色系 |

---

## 按颜色数量推荐 / By Color Count

| 需要颜色数 | 推荐定性型调色板 | 推荐连续型调色板 |
|-----------|----------------|----------------|
| 2-3 | `RColorBrewer::Dark2`, `nord::frost` | `viridis::viridis`, `scico::batlow` |
| 4-5 | `wesanderson::Royal1`, `nord::aurora`, `RColorBrewer::Set2` | `viridis::magma`, `scico::berlin` |
| 6-8 | `RColorBrewer::Dark2`, `RColorBrewer::Set1`, `ggsci::npg` | `viridis::plasma`, `scico::hawaii` |
| 9-12 | `RColorBrewer::Set3`, `RColorBrewer::Paired`, `rcartocolor::Bold` | `viridis::turbo`, `scico::roma` |
| 13-20 | `ggsci::d3`, `MetBrewer::Cassatt1`, `nationalparkcolors::*` | `viridis::turbo` |
| 20+ | `ggsci::ucscgb`, `ggsci::igv`, `Polychrome::*` | `viridis::turbo` |

---

## 按颜色风格推荐 / By Color Style

### 暖色调 / Warm Tones

| 调色板 | 说明 |
|--------|------|
| `wesanderson::FantasticFox1` | 橙黄蓝组合 |
| `MetBrewer::Hiroshige` | 日落暖色 |
| `MetBrewer::Tura` | 文艺复兴暖色 |
| `nationalparkcolors::Arches` | 沙漠红岩 |
| `viridis::inferno` | 黑到火红 |
| `RColorBrewer::Oranges` | 橙色渐变 |
| `RColorBrewer::Reds` | 红色渐变 |

### 冷色调 / Cool Tones

| 调色板 | 说明 |
|--------|------|
| `nord::frost` | 冰蓝青色 |
| `nord::polarnight` | 深蓝灰 |
| `MetBrewer::Hokusai2` | 深蓝主导 |
| `nationalparkcolors::CraterLake` | 湖泊蓝 |
| `viridis::viridis` | 紫到青绿 |
| `RColorBrewer::Blues` | 蓝色渐变 |

### 柔和/粉彩 / Pastel & Soft

| 调色板 | 说明 |
|--------|------|
| `RColorBrewer::Pastel1` | 粉彩系列 1 |
| `RColorBrewer::Pastel2` | 粉彩系列 2 |
| `RColorBrewer::Set2` | 柔和专业 |
| `wesanderson::GrandBudapest1` | 粉紫柔美 |
| `MetBrewer::Monet` | 印象派柔色 |
| `rcartocolor::Pastel` | CARTO 粉彩 |

### 鲜艳/高饱和 / Vivid & High Saturation

| 调色板 | 说明 |
|--------|------|
| `RColorBrewer::Set1` | 高对比红蓝绿 |
| `rcartocolor::Vivid` | 鲜艳明亮 |
| `rcartocolor::Bold` | 大胆高对比 |
| `MetBrewer::Signac` | 点彩派鲜艳 |
| `MetBrewer::Laffique` | 活力色彩 |
| `viridis::plasma` | 鲜艳连续型 |

### 灰度/单色 / Greyscale & Monochrome

| 调色板 | 说明 |
|--------|------|
| `RColorBrewer::Greys` | 白到黑灰度 |
| `scico::oslo` | 感知均匀灰度 |
| `nord::polarnight` | 深色灰度 |
| `nord::snowstorm` | 浅色灰度 |

### 大地色 / Earth Tones

| 调色板 | 说明 |
|--------|------|
| `MetBrewer::Pissarro` | 绿色田园 |
| `MetBrewer::Robert` | 绿色风景 |
| `nationalparkcolors::Denali` | 苔原色 |
| `nationalparkcolors::GrandTeton` | 山岳大地 |
| `soilpalettes::*` | 土壤色系 |
| `RColorBrewer::YlOrBr` | 黄到棕 |

---

## 中英文关键词对照 / Bilingual Keyword Reference

推荐引擎支持以下中英文关键词（通过 `--style`、`--scenario`、`--category` 参数传入）：

| 中文 | English | 含义 |
|------|---------|------|
| 顺序 / 顺序型 / 渐变 | sequential | 单色调由浅到深 |
| 发散 / 发散型 / 双向 | diverging | 两个极端+中间色 |
| 定性 / 定性型 / 离散 / 分类 | qualitative | 互不相似的类别色 |
| 连续 / 连续型 | continuous | 可生成任意数量颜色 |
| 色盲 / 色盲友好 / 无障碍 | colorblind | 色盲安全调色板 |
| 印刷 / 打印 / 印刷友好 | print | 印刷友好 |
| 学术 / 论文 / 期刊 / 科学 | academic | 学术出版物 |
| 商业 / 商务 / 报表 | business | 商务报告 |
| 艺术 / 创意 / 电影 | artistic | 艺术创意 |
| 自然 / 风景 / 公园 | nature | 自然主题 |
| 温暖 / 暖色 | warm | 暖色调 |
| 冷色 / 冷调 | cool | 冷色调 |
| 明亮 | bright | 明亮色调 |
| 鲜艳 | vivid | 高饱和 |
| 柔和 / 淡雅 | pastel | 粉彩柔和 |
| 暗色 / 深色 | dark | 深色调 |
| 浅色 | light | 浅色调 |
| 柔和低饱和 | muted | 低饱和 |
| 大地色 | earth | 大地色系 |
| 彩虹 | rainbow | 彩虹光谱 |
| 灰度 / 灰色 | greyscale / gray | 灰度单色 |
