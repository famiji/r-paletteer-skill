---
name: r-paletteer
description: "This skill should be used when working with R's paletteer color package (https://github.com/EmilHvitfeldt/paletteer). It provides comprehensive palette querying, smart recommendation, R code generation, and visualization for the 2893+ color palettes from 79 R packages aggregated by paletteer. Use this skill when users ask about R color palettes, paletteer functions (paletteer_c, paletteer_d, paletteer_dynamic), ggplot2 color scales, color palette selection/recommendation, or need HEX color values for R visualization. Supports Chinese and English input. Triggers include: paletteer, R color palette, R 配色, ggplot2 配色, 调色板, color palette R, palette recommendation, 配色推荐."
---

# R Paletteer — paletteer 配色包便捷使用工具

## Overview

This skill enables efficient use of R's **paletteer** package — a comprehensive collection of 2893+ color palettes from 79 R packages accessed through a unified interface. It provides palette querying, smart recommendation, R code generation, and visualization capabilities, supporting both Chinese and English input.

**Key capabilities:**
- Query palettes by package, type (continuous/discrete/dynamic), or category (sequential/diverging/qualitative)
- Smart recommendation based on color count, style, scenario, and constraints (colorblind-safe, print-friendly)
- Generate ready-to-use paletteer R function syntax and ggplot2 integration code
- Visualize selected palettes as SVG or interactive HTML
- Return structured palette info (name, source package, type, HEX color list)
- Works offline with embedded palette data; queries live R/paletteer when available

---

## When to Use This Skill

Use this skill when users:

1. **Ask about paletteer functions** — `paletteer_c()`, `paletteer_d()`, `paletteer_dynamic()`, or ggplot2 scale functions (`scale_color_paletteer_d()`, etc.)
2. **Need R color palettes** — "I need a color palette for my R plot", "R 配色推荐", "ggplot2 配色"
3. **Want palette recommendations** — "Recommend a palette for 5 categories", "推荐一个色盲友好的调色板"
4. **Need HEX color values** — "What are the colors in nord::aurora?", "viridis 的 HEX 值"
5. **Want to visualize palettes** — "Show me what this palette looks like", "可视化这个配色"
6. **Need ggplot2 integration code** — "How to use paletteer with ggplot2?", "ggplot2 中怎么调用"
7. **Search for palettes by keyword** — "Find blue palettes", "找暖色调色板"

---

## Resources Overview

### scripts/

Three Python scripts provide the core functionality:

| Script | Purpose |
|--------|---------|
| `scripts/palettes_data.py` | Embedded offline database of 150+ popular palettes with HEX values, metadata, and bilingual aliases |
| `scripts/query_paletteer.py` | Query palettes by package/type/category/name; prioritizes live R, falls back to embedded data |
| `scripts/recommend_palettes.py` | Smart recommendation engine with color analysis, scenario matching, and R code generation |
| `scripts/generate_palette_viz.py` | Generate SVG or interactive HTML visualizations of palettes |

### references/

Four reference documents provide detailed knowledge:

| File | Content |
|------|---------|
| `references/function_reference.md` | Complete function signatures for all paletteer functions + ggplot2 scales |
| `references/palettes_catalog.md` | Curated catalog of 150+ palettes with HEX values, organized by source package |
| `references/recommendation_guide.md` | Decision tree and recommendation matrix by scenario, style, and constraints |
| `references/ggplot2_examples.md` | Comprehensive ggplot2 integration examples for all chart types |

---

## Workflow

### Step 1: Understand User Intent

Determine what the user needs:

| User says | Action |
|-----------|--------|
| "List all palettes from package X" | Query by package |
| "I need N colors for a qualitative plot" | Recommend with constraints |
| "What colors are in palette X?" | Get specific palette |
| "Show me what palette X looks like" | Generate visualization |
| "How to use palette X in ggplot2?" | Generate R code |
| "推荐一个学术论文用的调色板" | Recommend by scenario (academic) |
| "找一个色盲友好的连续型配色" | Recommend with colorblind + continuous constraints |

### Step 2: Execute Query or Recommendation

#### Option A: Query a Specific Palette

```bash
python3 scripts/query_paletteer.py --get "wesanderson::Royal1" --no-r
```

Returns JSON with: `palette_id`, `package`, `palette`, `type`, `category`, `colorblind_safe`, `print_friendly`, `max_colors`, `colors` (HEX list), `description`, `source`.

#### Option B: List Palettes

```bash
# By package
python3 scripts/query_paletteer.py --list-by-package wesanderson --no-r

# By type (continuous/discrete/dynamic)
python3 scripts/query_paletteer.py --list-by-type discrete --no-r

# By category (sequential/diverging/qualitative)
python3 scripts/query_paletteer.py --list-by-category qualitative --no-r

# Search by keyword (supports Chinese)
python3 scripts/query_paletteer.py --search "colorblind" --no-r
python3 scripts/query_paletteer.py --search "暖色" --no-r
```

#### Option C: Smart Recommendation

```bash
# Recommend 5-color qualitative, colorblind-safe
python3 scripts/recommend_palettes.py --n 5 --category qualitative --colorblind

# Recommend for academic publication, 7 colors
python3 scripts/recommend_palettes.py --scenario academic --n 7

# Recommend warm-toned palettes
python3 scripts/recommend_palettes.py --style warm --n 5

# Chinese input
python3 scripts/recommend_palettes.py --场景 论文 --数量 6 --色盲友好
python3 scripts/recommend_palettes.py --风格 自然 --数量 7
```

Returns ranked JSON with: `match_score`, `match_reasons`, `r_code`, `ggplot2_code`, and full palette metadata.

#### Option D: List All Packages

```bash
python3 scripts/query_paletteer.py --list-packages --no-r
```

### Step 3: Generate Visualization (Optional)

When the user wants to see the palette:

```bash
# HTML (interactive, clickable swatches)
python3 scripts/generate_palette_viz.py "wesanderson::Royal1" --format html --no-r

# SVG (static, embeddable)
python3 scripts/generate_palette_viz.py "nord::aurora" --format svg --no-r

# With specific number of colors
python3 scripts/generate_palette_viz.py "scico::berlin" --n 10 --format html --no-r
```

For inline visualization without generating a file, use the `show_widget` tool to render an SVG directly in the conversation.

### Step 4: Present Results

Return structured information to the user:

1. **Palette metadata** — name (`package::palette`), source package, type, category
2. **HEX color list** — the actual color values
3. **Properties** — colorblind-safe, print-friendly, max colors
4. **R code** — ready-to-paste paletteer function call
5. **ggplot2 code** — integration example (if applicable)
6. **Visualization** — color swatches (SVG or HTML)

---

## R Code Generation

### Core Functions

Based on palette type, generate the correct function call:

| Type | Function | Example |
|------|----------|---------|
| continuous | `paletteer_c()` | `paletteer_c("scico::berlin", n = 10)` |
| discrete | `paletteer_d()` | `paletteer_d("nord::frost")` or `paletteer_d("wesanderson::Royal1", 3)` |
| dynamic | `paletteer_dynamic()` | `paletteer_dynamic("cartography::green.pal", 5)` |

### ggplot2 Scales

| Type | Color scale | Fill scale |
|------|-------------|------------|
| discrete | `scale_color_paletteer_d("pkg::pal")` | `scale_fill_paletteer_d("pkg::pal")` |
| continuous | `scale_color_paletteer_c("pkg::pal")` | `scale_fill_paletteer_c("pkg::pal")` |
| binned | `scale_color_paletteer_binned("pkg::pal")` | `scale_fill_paletteer_binned("pkg::pal")` |

All scale functions accept `direction = -1` to reverse the palette.

---

## Bilingual Support

The skill accepts both Chinese and English parameters:

| Chinese | English | Parameter |
|---------|---------|-----------|
| 顺序型 | sequential | --category |
| 发散型 | diverging | --category |
| 定性型 | qualitative | --category |
| 连续型 | continuous | --type |
| 离散型 | discrete | --type |
| 动态型 | dynamic | --type |
| 色盲友好 | colorblind | --colorblind |
| 印刷友好 | print | --print |
| 风格 | style | --style |
| 场景 | scenario | --scenario |
| 数量 | n | --n |

Scenario keywords: 学术/academic, 商务/business, 艺术/artistic, 自然/nature

Style keywords: 暖色/warm, 冷色/cool, 鲜艳/vivid, 柔和/pastel, 暗色/dark, 浅色/light, 灰度/greyscale, 大地色/earth, 彩虹/rainbow

---

## Important Notes

1. **Offline-first design**: The embedded database contains 150+ popular palettes. When R + paletteer are installed, scripts automatically query the full 2893-palette collection. Always pass `--no-r` when running scripts in environments without R.

2. **HEX format**: paletteer returns colors with alpha channel (e.g., `#8FBCBBFF`). The embedded database stores colors without alpha (e.g., `#8FBCBB`) for readability. Both formats work in R.

3. **Palette identifier format**: Always use `"packagename::palettename"` format (e.g., `"nord::frost"`, `"wesanderson::Royal1"`). This is the paletteer v1.7.0+ syntax.

4. **Color count limitations**: Discrete palettes have a fixed maximum number of colors. If the user requests more colors than available, note the limitation and suggest alternatives (e.g., continuous palettes, or palettes with higher max_colors).

5. **Reference consultation**: For detailed function signatures, consult `references/function_reference.md`. For palette HEX values, consult `references/palettes_catalog.md`. For recommendation logic, consult `references/recommendation_guide.md`. For ggplot2 examples, consult `references/ggplot2_examples.md`.
