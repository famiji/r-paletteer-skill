# r-paletteer-skill

> 便捷使用 R 语言 [paletteer](https://github.com/EmilHvitfeldt/paletteer) 配色包的辅助工具

paletteer 聚合了来自 79 个 R 包的 **2893+ 个调色板**，是 R 生态中最全面的调色板集合。本工具提供查询、智能推荐、代码生成和可视化能力，支持中英文双语输入，无需安装 R 即可离线使用。

---

## 功能概览

| 能力 | 说明 |
|------|------|
| **查询调色板** | 按包名、类型（连续/离散/动态）、类别（顺序/发散/定性）或关键词检索 |
| **智能推荐** | 根据颜色数量、风格、使用场景、色盲友好/印刷友好等约束推荐 |
| **生成 R 代码** | 自动生成 `paletteer_c()` / `paletteer_d()` / `paletteer_dynamic()` 函数调用 |
| **ggplot2 集成** | 生成 `scale_color/fill_paletteer_*()` 比例尺代码 |
| **可视化** | 生成 SVG 色块图或交互式 HTML（点击复制 HEX 值） |
| **中英文支持** | 接受 `--色盲友好`、`--场景 论文`、`--风格 暖色` 等中文参数 |

---

## 项目结构

本仓库遵循 [Agent Skills 规范](https://agentskills.io/specification)，Skill 目录即仓库根目录：

```
r-paletteer-skill/                     # Skill 根目录（SKILL.md 位于顶层）
├── SKILL.md                           # 技能定义文件（frontmatter + 指令）
├── scripts/                           # 可执行代码（Python + R）
│   ├── palettes_data.py               # 离线调色板数据库（150+ 个，含 HEX 色值）
│   ├── query_paletteer.py             # Python 查询脚本
│   ├── recommend_palettes.py          # Python 智能推荐引擎
│   ├── generate_palette_viz.py        # Python 可视化生成器（SVG / HTML）
│   └── paletteer_tools.R              # R 原生工具脚本（直接调用 paletteer）
├── references/                        # 按需加载的参考文档
│   ├── function_reference.md          # paletteer 函数签名完整参考
│   ├── palettes_catalog.md            # 调色板目录（按源包组织，含 HEX 值）
│   ├── recommendation_guide.md        # 推荐决策矩阵
│   └── ggplot2_examples.md            # ggplot2 各图表类型集成示例
├── LICENSE
└── README.md
```

---

## 快速开始

### 环境要求

- Python 3.8+
- （可选）R + paletteer 包 — 安装后脚本会自动查询完整的 2893 个调色板

```r
# R 中安装 paletteer
install.packages("paletteer")
```

### 查询调色板

```bash
# 获取指定调色板的颜色
python3 scripts/query_paletteer.py --get "wesanderson::Royal1" --no-r

# 列出某包的所有调色板
python3 scripts/query_paletteer.py --list-by-package nord --no-r

# 按类型列出（continuous / discrete / dynamic）
python3 scripts/query_paletteer.py --list-by-type discrete --no-r

# 按类别列出（sequential / diverging / qualitative）
python3 scripts/query_paletteer.py --list-by-category qualitative --no-r

# 关键词搜索
python3 scripts/query_paletteer.py --search "colorblind" --no-r
```

### 智能推荐

```bash
# 推荐 5 色定性调色板，要求色盲友好
python3 scripts/recommend_palettes.py --n 5 --category qualitative --colorblind

# 推荐学术场景用的 7 色调色板
python3 scripts/recommend_palettes.py --scenario academic --n 7

# 推荐暖色调调色板
python3 scripts/recommend_palettes.py --style warm --n 5

# 中文参数
python3 scripts/recommend_palettes.py --场景 论文 --数量 6 --色盲友好
```

### 生成可视化

```bash
# 生成 HTML（可交互，点击复制 HEX）
python3 scripts/generate_palette_viz.py "nord::aurora" --format html --no-r

# 生成 SVG
python3 scripts/generate_palette_viz.py "scico::berlin" --n 10 --format svg --no-r
```

### R 原生脚本（需要 R + paletteer）

`scripts/paletteer_tools.R` 直接调用 paletteer 包，可访问**全部 2893+ 个调色板**，并支持作为函数库 `source()` 使用：

```bash
# CLI 模式（与 Python 脚本参数形状一致）
Rscript scripts/paletteer_tools.R --get "nord::frost"
Rscript scripts/paletteer_tools.R --get "pals::ocean.haline" --n 6
Rscript scripts/paletteer_tools.R --list-by-package wesanderson
Rscript scripts/paletteer_tools.R --list-by-category qualitative
Rscript scripts/paletteer_tools.R --search blue
Rscript scripts/paletteer_tools.R --recommend --n 5 --category qualitative
Rscript scripts/paletteer_tools.R --r-code "RColorBrewer::Set1"
Rscript scripts/paletteer_tools.R --ggplot2-code "pals::ocean.haline"
Rscript scripts/paletteer_tools.R --plot "RColorBrewer::Set1" --save set1.png
```

作为函数库使用：

```r
source("scripts/paletteer_tools.R")

paletteer_get("nord::frost")                  # 取颜色
paletteer_plot("nord::aurora")                # 当前设备绘制色块
paletteer_plot("nord::aurora", save = "aurora.png")  # 保存 PNG/PDF/SVG
paletteer_recommend(n_colors = 5, category = "qualitative")  # 推荐
cat(paletteer_r_code("RColorBrewer::Set1"))  # 生成 R 调用代码
```

**注意**：`--get` 与 `--plot` 需要对应的源包已安装（如 `wesanderson`、`scico`），否则需先 `install.packages("wesanderson")`。列表、搜索、推荐和代码生成不需要源包。

---

## 涵盖的源包

内置 150+ 个常用调色板的 HEX 色值数据，涵盖以下 10 个热门包：

| 源包 | 调色板数 | 特点 |
|------|---------|------|
| **RColorBrewer** | 35 | 经典 ColorBrewer 配色，学术论文最常用 |
| **viridis** | 8 | 感知均匀 + 色盲友好，连续型首选 |
| **wesanderson** | 22+ | Wes Anderson 电影风格 |
| **nord** | 8 | 北欧极简风格 |
| **rcartocolor** | 22 | CARTO 地图配色方案 |
| **scico** | 14+ | 科学配色，全部感知均匀且色盲友好 |
| **ggsci** | 9 | 学术期刊风格（NPG/Lancet/JCO/NEJM 等） |
| **ghibli** | 8 | 吉卜力工作室动画风格 |
| **MetBrewer** | 26+ | 大都会艺术博物馆名画风格 |
| **nationalparkcolors** | 24 | 美国国家公园风格 |

安装 R + paletteer 后，可查询全部 79 个包的 2893 个调色板。

---

## 输出示例

```json
{
  "palette_id": "nord::aurora",
  "package": "nord",
  "palette": "aurora",
  "type": "discrete",
  "category": "qualitative",
  "colorblind_safe": false,
  "print_friendly": false,
  "max_colors": 5,
  "colors": ["#BF616A", "#D08770", "#EBCB8B", "#A3BE8C", "#B48EAD"],
  "description": "Nord Aurora: warm accent colors",
  "r_code": "paletteer_d(\"nord::aurora\")",
  "source": "embedded_db"
}
```

---

## paletteer 函数速查

| 函数 | 用途 | 示例 |
|------|------|------|
| `paletteer_c()` | 连续型调色板 | `paletteer_c("scico::berlin", n = 10)` |
| `paletteer_d()` | 离散型调色板 | `paletteer_d("nord::frost")` |
| `paletteer_dynamic()` | 动态型调色板 | `paletteer_dynamic("cartography::green.pal", 5)` |
| `scale_color_paletteer_d()` | ggplot2 离散着色 | `+ scale_color_paletteer_d("nord::aurora")` |
| `scale_fill_paletteer_c()` | ggplot2 连续填充 | `+ scale_fill_paletteer_c("viridis::magma")` |

---

## 相关链接

- [paletteer GitHub](https://github.com/EmilHvitfeldt/paletteer)
- [paletteer 文档](https://emilhvitfeldt.github.io/paletteer/)
- [所有调色板可视化](https://github.com/EmilHvitfeldt/r-color-palettes)
- [调色板在线浏览器](https://r-graph-gallery.com/color-palette-finder)

## License

MIT
