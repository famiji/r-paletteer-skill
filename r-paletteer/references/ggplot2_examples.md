# ggplot2 集成示例 / ggplot2 Integration Examples

> 本文档包含 paletteer 在 ggplot2 各种图表类型中的集成调用示例。

---

## 基本设置 / Setup

```r
library(ggplot2)
library(paletteer)
```

## 比例尺函数总览 / Scale Functions Overview

| 函数 | 用途 | 数据类型 |
|------|------|---------|
| `scale_color_paletteer_d()` | 离散着色 | 分类变量 |
| `scale_fill_paletteer_d()` | 离散填充 | 分类变量 |
| `scale_color_paletteer_c()` | 连续着色 | 连续变量 |
| `scale_fill_paletteer_c()` | 连续填充 | 连续变量 |
| `scale_color_paletteer_binned()` | 分箱着色 | 连续变量 |
| `scale_fill_paletteer_binned()` | 分箱填充 | 连续变量 |

> `scale_colour_*` 是 `scale_color_*` 的别名，功能完全相同。

---

## 1. 散点图 / Scatter Plot

### 离散着色 / Discrete Color

```r
ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Species)) +
  geom_point(size = 3, alpha = 0.8) +
  scale_color_paletteer_d("nord::aurora") +
  theme_minimal() +
  labs(title = "Iris Sepal Dimensions", x = "Sepal Length", y = "Sepal Width")
```

### 连续着色 / Continuous Color

```r
ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Petal.Length)) +
  geom_point(size = 3, alpha = 0.8) +
  scale_color_paletteer_c("viridis::viridis") +
  theme_minimal()
```

### 反转方向 / Reverse Direction

```r
ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Petal.Length)) +
  geom_point(size = 3) +
  scale_color_paletteer_c("scico::batlow", direction = -1)
```

---

## 2. 柱状图 / Bar Chart

### 离散填充 / Discrete Fill

```r
ggplot(mpg, aes(class, fill = drv)) +
  geom_bar(position = "dodge") +
  scale_fill_paletteer_d("wesanderson::FantasticFox1") +
  theme_minimal() +
  labs(title = "Car Class by Drive Type", x = "Class", y = "Count")
```

### 堆叠柱状图 / Stacked Bar

```r
ggplot(mpg, aes(manufacturer, fill = class)) +
  geom_bar(position = "fill") +
  scale_fill_paletteer_d("RColorBrewer::Set3") +
  theme_minimal() +
  coord_flip() +
  labs(title = "Car Class Proportion by Manufacturer", y = "Proportion")
```

---

## 3. 热力图 / Heatmap

### 连续填充 / Continuous Fill

```r
# 使用 faithfuld 数据集
ggplot(faithfuld, aes(waiting, eruptions, fill = density)) +
  geom_raster() +
  scale_fill_paletteer_c("viridis::magma") +
  theme_minimal() +
  labs(title = "Old Faithful Eruption Density")
```

### 发散填充 / Diverging Fill

```r
# 模拟相关矩阵
cor_matrix <- cor(mtcars)
cor_df <- as.data.frame(as.table(cor_matrix))
colnames(cor_df) <- c("Var1", "Var2", "Correlation")

ggplot(cor_df, aes(Var1, Var2, fill = Correlation)) +
  geom_tile() +
  scale_fill_paletteer_c("scico::berlin") +
  theme_minimal() +
  labs(title = "mtcars Correlation Matrix") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

---

## 4. 箱线图 / Box Plot

```r
ggplot(mpg, aes(class, hwy, fill = class)) +
  geom_boxplot() +
  scale_fill_paletteer_d("ggsci::npg") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(title = "Highway MPG by Car Class", x = "Class", y = "Highway MPG") +
  guides(fill = "none")  # 隐藏图例（已用 x 轴标签）
```

---

## 5. 小提琴图 / Violin Plot

```r
ggplot(diamonds, aes(cut, price, fill = cut)) +
  geom_violin(scale = "width") +
  scale_fill_paletteer_d("MetBrewer::Klimt") +
  theme_minimal() +
  labs(title = "Diamond Price Distribution by Cut") +
  guides(fill = "none")
```

---

## 6. 面积图 / Area Chart

```r
ggplot(economics, aes(date, psavert, fill = psavert)) +
  geom_area() +
  scale_fill_paletteer_c("rcartocolor::Sunset") +
  theme_minimal() +
  labs(title = "Personal Savings Rate Over Time",
       x = "Date", y = "Personal Savings Rate (%)")
```

---

## 7. 等高线图 / Contour Plot

```r
ggplot(faithfuld, aes(waiting, eruptions, z = density)) +
  geom_contour_filled() +
  scale_fill_paletteer_d("scico::batlow", direction = -1) +
  theme_minimal() +
  labs(title = "Old Faithful Eruption Density Contours")
```

---

## 8. 分面图 / Faceted Plot

```r
ggplot(mpg, aes(displ, hwy, color = class)) +
  geom_point(size = 2, alpha = 0.7) +
  scale_color_paletteer_d("nationalparkcolors::Arches") +
  facet_wrap(~ drv) +
  theme_minimal() +
  labs(title = "Engine Displacement vs Highway MPG", x = "Displacement (L)", y = "Highway MPG")
```

---

## 9. 地理可视化 / Spatial Visualization

```r
# 使用 sf 包进行地图着色
library(sf)

ggplot(nc_sf, aes(fill = AREA)) +
  geom_sf() +
  scale_fill_paletteer_c("scico::davos") +
  theme_minimal() +
  labs(title = "North Carolina Counties by Area", fill = "Area")
```

---

## 10. 分箱着色 / Binned Scale

```r
ggplot(diamonds, aes(carat, price, color = depth)) +
  geom_point(alpha = 0.5) +
  scale_color_paletteer_binned("rcartocolor::BurgYl") +
  theme_minimal() +
  labs(title = "Diamond Price vs Carat (Binned Depth Color)")
```

---

## 直接获取颜色值 / Get Colors Directly

在 ggplot2 之外，也可以直接获取颜色值用于 base R 绘图或其他用途：

```r
# 获取离散型调色板颜色
colors <- paletteer_d("nord::aurora")
print(colors)
#> <colors>
#> #BF616AFF #D08770FF #EBCB8BFF #A3BE8CFF #B48EADFF

# 获取指定数量的颜色
colors <- paletteer_d("wesanderson::Royal1", 3)

# 获取连续型调色板颜色
colors <- paletteer_c("viridis::viridis", n = 20)

# 获取动态型调色板颜色
colors <- paletteer_dynamic("cartography::green.pal", 5)

# 转换为普通字符向量
color_vector <- as.character(paletteer_d("nord::frost"))
#> [1] "#8FBCBBFF" "#88C0D0FF" "#81A1C1FF" "#5E81ACFF"
```

---

## 与 base R 绘图集成 / Base R Integration

```r
# 获取颜色并用于 base R
colors <- as.character(paletteer_d("wesanderson::Zissou1"))

# 用于 barplot
barplot(1:5, col = colors, names.arg = LETTERS[1:5])

# 用于 pie chart
pie(1:5, col = colors, labels = LETTERS[1:5])

# 用于散点图
plot(iris$Sepal.Length, iris$Sepal.Width,
     col = as.character(paletteer_d("nord::aurora")[as.numeric(iris$Species)]),
     pch = 19, cex = 1.5)
```

---

## 高级技巧 / Advanced Tips

### 自定义调色板方向

```r
# direction = -1 反转调色板
ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Species)) +
  geom_point(size = 3) +
  scale_color_paletteer_d("nord::aurora", direction = -1)
```

### 使用离散型调色板的连续插值

```r
# type = "continuous" 对离散调色板进行插值
ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Sepal.Length)) +
  geom_point(size = 3) +
  scale_color_paletteer_c("wesanderson::Zissou1")  # 自动插值
```

### 组合多个调色板

```r
# 主色和填充使用不同调色板
ggplot(mpg, aes(displ, hwy)) +
  geom_point(aes(color = class), size = 3) +
  geom_smooth(aes(fill = drv), method = "lm") +
  scale_color_paletteer_d("nord::aurora") +
  scale_fill_paletteer_d("wesanderson::Royal1", direction = -1) +
  theme_minimal()
```

### 在 ggplot2 主题中使用 paletteer 颜色

```r
# 获取调色板颜色用于自定义主题
bg_color <- as.character(paletteer_d("nord::polarnight")[1])
text_color <- as.character(paletteer_d("nord::snowstorm")[3])

ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Species)) +
  geom_point(size = 3) +
  scale_color_paletteer_d("nord::frost") +
  theme(
    plot.background = element_rect(fill = bg_color),
    panel.background = element_rect(fill = bg_color),
    text = element_text(color = text_color),
    axis.text = element_text(color = text_color)
  )
```
