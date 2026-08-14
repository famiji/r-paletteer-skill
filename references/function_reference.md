# paletteer 函数参考 / Function Reference

> 本文档包含 paletteer 包所有导出函数的完整签名、参数说明和用法示例。
>
> This document contains complete signatures, parameter descriptions, and usage examples for all exported paletteer functions.

---

## 核心调色板函数 / Core Palette Functions

### `paletteer_c()` — 连续型调色板 / Continuous Palettes

获取连续型调色板的颜色值。连续型调色板可以生成任意数量的颜色，实现平滑过渡。

```r
paletteer_c(palette, n, direction = 1)
```

**参数 / Arguments:**

| 参数 | 类型 | 说明 |
|------|------|------|
| `palette` | string | 调色板标识，格式为 `"packagename::palettename"` |
| `n` | integer | 需要的颜色数量（必须指定） |
| `direction` | integer | `1`（正序）或 `-1`（反转）。默认 `1` |

**返回值 / Return:** 颜色向量（HEX 格式，含 alpha 通道 `FF`）

**示例 / Examples:**

```r
library(paletteer)

# 获取 10 个颜色的 scico::berlin 连续型调色板
paletteer_c("scico::berlin", n = 10)
#> <colors>
#> #9EB0FFFF #5AA3DAFF #2D7597FF #194155FF #11181DFF #270C01FF #501802FF #8A3F2AFF #C37469FF #FFACACFF

# 反转方向
paletteer_c("viridis::viridis", n = 5, direction = -1)
#> <colors>
#> #FDE725FF #6ECE58FF #35B779FF #1F9E89FF #440154FF
```

**可用调色板列表:** 查询 `palettes_c_names` 数据框

```r
# 查看所有连续型调色板
head(paletteer::palettes_c_names)
#>   package  palette length
#> 1  scico   acton    256
#> 2  scico   bamako   256
#> 3  scico   batlow   256
#> ...
```

---

### `paletteer_d()` — 离散型调色板 / Discrete Palettes

获取固定宽度离散型调色板。颜色集合固定，不会随请求的数量变化（但可通过 `type = "continuous"` 进行插值）。

```r
paletteer_d(palette, n, direction = 1, type = c("discrete", "continuous"))
```

**参数 / Arguments:**

| 参数 | 类型 | 说明 |
|------|------|------|
| `palette` | string | 调色板标识，格式为 `"packagename::palettename"` |
| `n` | integer | 需要的颜色数量。省略时返回完整调色板 |
| `direction` | integer | `1`（正序）或 `-1`（反转）。默认 `1` |
| `type` | string | `"discrete"`（默认）或 `"continuous"`。选 `"continuous"` 时颜色会被插值 |

**返回值 / Return:** 颜色向量（HEX 格式，含 alpha 通道 `FF`）

**示例 / Examples:**

```r
# 获取完整调色板
paletteer_d("nord::frost")
#> <colors>
#> #8FBCBBFF #88C0D0FF #81A1C1FF #5E81ACFF

# 获取指定数量的颜色
paletteer_d("wesanderson::Royal1", 3)
#> <colors>
#> #899DA4FF #C93312FF #FAEFD1FF

# 使用连续插值模式获取 14 个颜色
paletteer_d("Redmonder::dPBIPuOr", 14, type = "continuous")
#> <colors>
#> #53354DFF #73496AFF #9C6D92FF #BD90B3FF ...
```

**可用调色板列表:** 查询 `palettes_d_names` 数据框

---

### `paletteer_dynamic()` — 动态型调色板 / Dynamic Palettes

获取动态型调色板。颜色会根据请求的数量而变化。

```r
paletteer_dynamic(palette, n, direction = 1)
```

**参数 / Arguments:**

| 参数 | 类型 | 说明 |
|------|------|------|
| `palette` | string | 调色板标识，格式为 `"packagename::palettename"` |
| `n` | integer | 需要的颜色数量。省略时返回完整调色板 |
| `direction` | integer | `1`（正序）或 `-1`（反转）。默认 `1` |

**返回值 / Return:** 颜色向量（HEX 格式，含 alpha 通道 `FF`）

**示例 / Examples:**

```r
# 获取 5 个颜色
paletteer_dynamic("cartography::green.pal", 5)
#> <colors>
#> #B8D9A9FF #8DBC80FF #5D9D52FF #287A22FF #17692CFF

# 获取 8 个颜色
paletteer_dynamic("ggthemes_solarized::green", 8)
#> <colors>
#> #859900FF #B58900FF #CB4B16FF #DC322FFF #D33682FF #6C71C4FF #268BD2FF #2AA198FF
```

**可用调色板列表:** 查询 `palettes_dynamic_names` 数据框

---

## ggplot2 比例尺函数 / ggplot2 Scale Functions

paletteer 为 ggplot2 提供了原生比例尺函数，使用与核心函数相同的 `"packagename::palettename"` 接口。

### 离散型比例尺 / Discrete Scales

```r
scale_color_paletteer_d(palette, direction = 1, ...)
scale_colour_paletteer_d(palette, direction = 1, ...)  # 别名
scale_fill_paletteer_d(palette, direction = 1, ...)
```

**示例:**

```r
library(ggplot2)
library(paletteer)

# 散点图离散着色
ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Species)) +
  geom_point(size = 3) +
  scale_color_paletteer_d("nord::aurora")

# 柱状图离散填充
ggplot(mpg, aes(class, fill = drv)) +
  geom_bar() +
  scale_fill_paletteer_d("wesanderson::FantasticFox1")
```

### 连续型比例尺 / Continuous Scales

```r
scale_color_paletteer_c(palette, direction = 1, ...)
scale_colour_paletteer_c(palette, direction = 1, ...)  # 别名
scale_fill_paletteer_c(palette, direction = 1, ...)
```

**示例:**

```r
# 连续型着色
ggplot(faithfuld, aes(waiting, eruptions, fill = density)) +
  geom_raster() +
  scale_fill_paletteer_c("viridis::magma")

# 反转方向
ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Petal.Length)) +
  geom_point(size = 3) +
  scale_color_paletteer_c("scico::batlow", direction = -1)
```

### 分箱型比例尺 / Binned Scales

```r
scale_color_paletteer_binned(palette, direction = 1, ...)
scale_colour_paletteer_binned(palette, direction = 1, ...)  # 别名
scale_fill_paletteer_binned(palette, direction = 1, ...)
```

**示例:**

```r
# 分箱着色
ggplot(diamonds, aes(carat, price, color = depth)) +
  geom_point(alpha = 0.5) +
  scale_color_paletteer_binned("rcartocolor::Sunset")
```

---

## 数据框 / Data Frames

paletteer 内置三个数据框，存储所有调色板的元数据信息：

| 数据框 | 说明 | 列 |
|--------|------|-----|
| `palettes_c_names` | 所有连续型调色板 | `package`, `palette`, `length` |
| `palettes_d_names` | 所有固定宽度离散型调色板 | `package`, `palette`, `length` |
| `palettes_dynamic_names` | 所有动态型调色板 | `package`, `palette`, `length` |

### `paletteer_packages` — 包信息数据框

```r
# 查看所有源包信息
head(paletteer::paletteer_packages)
#>      packages github_version cran_version
#> 1  ButterflyColors    0.0.0.9000           NA
#> 2     DresdenColor    0.0.0.9000           NA
#> 3       IslamicArt          0.1.0           NA
#> ...
```

---

## 调色板标识格式 / Palette Identifier Format

所有函数使用统一的 `"packagename::palettename"` 字符串格式：

```
"源包名::调色板名"
```

**示例:**

| 标识 | 源包 | 调色板 |
|------|------|--------|
| `"nord::frost"` | nord | frost |
| `"wesanderson::Royal1"` | wesanderson | Royal1 |
| `"scico::berlin"` | scico | berlin |
| `"viridis::magma"` | viridis | magma |
| `"RColorBrewer::Set1"` | RColorBrewer | Set1 |

> **注意:** paletteer <= 0.2.1 使用 `package` 和 `palette` 两个参数的旧语法已废弃。当前版本仅支持 `"packagename::palettename"` 字符串语法。

---

## 函数选择指南 / Function Selection Guide

| 需求 | 函数 | 数据类型示例 |
|------|------|-------------|
| 连续数值映射（如热力图、密度图） | `paletteer_c()` | 温度、海拔、密度 |
| 离散类别区分（如分组散点图） | `paletteer_d()` | 物种、类别、分组 |
| 动态数量类别（颜色随数量变化） | `paletteer_dynamic()` | 层级分类 |
| ggplot2 离散着色 | `scale_color/fill_paletteer_d()` | — |
| ggplot2 连续着色 | `scale_color/fill_paletteer_c()` | — |
| ggplot2 分箱着色 | `scale_color/fill_paletteer_binned()` | — |

---

## 安装 / Installation

```r
# CRAN 稳定版
install.packages("paletteer")

# GitHub 开发版
# install.packages("devtools")
devtools::install_github("EmilHvitfeldt/paletteer")
```
