#!/usr/bin/env Rscript
# =============================================================================
# paletteer_tools.R
# =============================================================================
# R 原生工具脚本：查询、推荐、可视化和代码生成
# 直接调用 paletteer 包，可访问全部 2893+ 个调色板（79 个源包）。
#
# 依赖：R (>= 4.0), paletteer（jsonlite 可选，用于 JSON 输出）
#
# 安装 paletteer:
#   install.packages("paletteer")
#
# 作为库使用（source 后调用函数）：
#   source("paletteer_tools.R")
#   paletteer_get("nord::frost")
#   paletteer_plot("nord::aurora", save = "aurora.png")
#
# 命令行使用：
#   Rscript paletteer_tools.R --list-packages
#   Rscript paletteer_tools.R --list-by-type discrete
#   Rscript paletteer_tools.R --list-by-category qualitative
#   Rscript paletteer_tools.R --list-by-package wesanderson
#   Rscript paletteer_tools.R --get "nord::frost"
#   Rscript paletteer_tools.R --get "scico::berlin" --n 10
#   Rscript paletteer_tools.R --search blue
#   Rscript paletteer_tools.R --recommend --n 5 --category qualitative
#   Rscript paletteer_tools.R --plot "nord::aurora" --save aurora.png
# =============================================================================

suppressMessages(library(paletteer))

# -----------------------------------------------------------------------------
# 内部工具
# -----------------------------------------------------------------------------

.has_jsonlite <- requireNamespace("jsonlite", quietly = TRUE)

# 输出 JSON（jsonlite 可用时）或 R 文本格式
.out <- function(x) {
  if (.has_jsonlite) {
    cat(jsonlite::toJSON(x, auto_unbox = TRUE, pretty = TRUE, force = TRUE))
  } else {
    dput(x)
  }
  cat("\n")
}

# 标准化 HEX 颜色：去掉 alpha 通道（8 位 -> 6 位），统一大写
.norm_hex <- function(colors) {
  hex <- as.character(colors)
  hex <- toupper(hex)
  for (i in seq_along(hex)) {
    h <- hex[i]
    if (grepl("^#", h) && nchar(h) == 9) {
      hex[i] <- substr(h, 1, 7)
    } else if (!grepl("^#", h) && nchar(h) == 8) {
      hex[i] <- paste0("#", substr(h, 1, 6))
    } else if (!grepl("^#", h) && nchar(h) == 6) {
      hex[i] <- paste0("#", h)
    }
  }
  hex
}

# 根据 palette_id 判断类型（连续/离散/动态）
.palette_type <- function(palette_id) {
  c_ids <- paste(palettes_c_names$package, palettes_c_names$palette, sep = "::")
  d_ids <- paste(palettes_d_names$package, palettes_d_names$palette, sep = "::")
  dy_ids <- paste(palettes_dynamic_names$package, palettes_dynamic_names$palette, sep = "::")
  if (palette_id %in% c_ids) return("continuous")
  if (palette_id %in% d_ids) return("discrete")
  if (palette_id %in% dy_ids) return("dynamic")
  NULL
}

# 类别统一：paletteer 内部连续型用 "diverging"、离散型用 "divergent"
.norm_category <- function(x) {
  ifelse(tolower(x) %in% c("diverging", "divergent"), "diverging", tolower(x))
}

# -----------------------------------------------------------------------------
# 1. 查询功能
# -----------------------------------------------------------------------------

#' 列出所有源包
paletteer_list_packages <- function() {
  df <- paletteer_packages
  cols <- c("packages", "github_version", "cran_version")
  cols <- cols[cols %in% names(df)]
  df[, cols, drop = FALSE]
}

#' 列出调色板
#' @param type "all" | "continuous" | "discrete" | "dynamic"
#' @param category "sequential" | "diverging" | "qualitative"（可选过滤）
#' @param package 源包名（可选过滤）
paletteer_list <- function(type = c("all", "continuous", "discrete", "dynamic"),
                           category = NULL, package = NULL) {
  type <- match.arg(type)

  build <- function(df, t) {
    data.frame(
      palette_id = paste(df$package, df$palette, sep = "::"),
      package    = df$package,
      palette    = df$palette,
      type       = t,
      category   = .norm_category(df$type),
      length     = if ("length" %in% names(df)) df$length else NA,
      stringsAsFactors = FALSE
    )
  }

  out <- NULL
  if (type %in% c("all", "continuous"))  out <- rbind(out, build(palettes_c_names, "continuous"))
  if (type %in% c("all", "discrete"))    out <- rbind(out, build(palettes_d_names, "discrete"))
  if (type %in% c("all", "dynamic"))     out <- rbind(out, build(palettes_dynamic_names, "dynamic"))

  if (!is.null(category)) {
    cat_key <- .norm_category(category)
    out <- out[out$category == cat_key, , drop = FALSE]
  }
  if (!is.null(package)) {
    out <- out[out$package == package, , drop = FALSE]
  }
  rownames(out) <- NULL
  out
}

#' 获取调色板颜色
#' @param palette_id 格式 "package::palette"
#' @param n 颜色数量（连续型必填或默认 10；离散型省略则返回全部）
#' @param direction 1 或 -1（反转）
paletteer_get <- function(palette_id, n = NULL, direction = 1) {
  parts <- strsplit(palette_id, "::")[[1]]
  if (length(parts) != 2) {
    stop("Palette must be in 'package::palette' format, e.g. \"nord::frost\"")
  }
  ptype <- .palette_type(palette_id)

  colors <- NULL
  if (is.null(ptype) || ptype == "discrete") {
    colors <- if (is.null(n)) {
      paletteer_d(palette_id, direction = direction)
    } else {
      paletteer_d(palette_id, n = n, direction = direction)
    }
    if (is.null(ptype)) ptype <- "discrete"
  } else if (ptype == "continuous") {
    if (is.null(n)) n <- 10
    colors <- paletteer_c(palette_id, n = n, direction = direction)
  } else if (ptype == "dynamic") {
    if (is.null(n)) n <- 5
    colors <- paletteer_dynamic(palette_id, n = n, direction = direction)
  }

  list(
    palette_id = palette_id,
    package    = parts[1],
    palette    = parts[2],
    type       = ptype,
    n_colors   = length(colors),
    colors     = .norm_hex(colors)
  )
}

#' 关键词搜索调色板（名称/包名/类别）
paletteer_search <- function(keyword) {
  kw <- tolower(keyword)
  df <- paletteer_list("all")
  hits <- grepl(kw, tolower(df$palette_id)) |
          grepl(kw, tolower(df$category))   |
          grepl(kw, tolower(df$package))
  df[hits, , drop = FALSE]
}

# -----------------------------------------------------------------------------
# 2. 推荐功能
# -----------------------------------------------------------------------------

#' 智能推荐调色板
#' @param n_colors 需要的颜色数量
#' @param category "sequential" | "diverging" | "qualitative"
#' @param type "continuous" | "discrete" | "dynamic"
#' @param package 限定源包
#' @param max_results 返回条数
paletteer_recommend <- function(n_colors = NULL, category = NULL, type = NULL,
                                package = NULL, max_results = 10) {
  df <- paletteer_list("all")

  if (!is.null(category)) {
    cat_key <- .norm_category(category)
    df <- df[df$category == cat_key, , drop = FALSE]
  }
  if (!is.null(type)) df <- df[df$type == type, , drop = FALSE]
  if (!is.null(package)) df <- df[df$package == package, , drop = FALSE]

  # 打分：连续型可生成任意数量；离散/动态型需满足颜色数量
  if (!is.null(n_colors)) {
    score <- ifelse(df$type == "continuous", 20,
             ifelse(is.na(df$length), 10,
             ifelse(df$length >= n_colors, 25 + pmax(0, 5 - (df$length - n_colors)),
             ifelse(df$length >= n_colors - 2, 10, -30))))
  } else {
    score <- rep(10, nrow(df))
  }
  df$match_score <- as.integer(score)
  df <- df[order(df$match_score, decreasing = TRUE), , drop = FALSE]
  head(df, max_results)
}

# -----------------------------------------------------------------------------
# 3. 可视化功能
# -----------------------------------------------------------------------------

#' 绘制调色板色块图（base R，无额外依赖）
#' @param palette_id 格式 "package::palette"
#' @param n 颜色数量
#' @param save 输出文件路径（PNG/PDF/SVG，按扩展名）；NULL 则输出到当前设备
#' @param width 图片宽度（英寸）
#' @param height 图片高度（英寸）
paletteer_plot <- function(palette_id, n = NULL, save = NULL,
                           width = 8, height = 2.2, res = 150) {
  p <- paletteer_get(palette_id, n = n)
  colors <- p$colors
  k <- length(colors)

  if (!is.null(save)) {
    ext <- tolower(tools::file_ext(save))
    dev_fn <- switch(ext,
      png  = grDevices::png,
      pdf  = grDevices::pdf,
      svg  = grDevices::svg,
      jpeg = grDevices::jpeg,
      grDevices::png
    )
    dev_fn(save, width = width, height = height, units = "in", res = res)
    on.exit(grDevices::dev.off(), add = TRUE)
  }

  op <- par(mar = c(4, 1, 3, 1))
  graphics::plot.new()
  graphics::plot.window(xlim = c(0, k), ylim = c(0, 1))
  for (i in seq_len(k)) {
    graphics::rect(i - 1, 0, i, 1, col = colors[i], border = NA)
  }
  # 色块下方标注 HEX
  graphics::text(
    x = seq_len(k) - 0.5, y = 0.03,
    labels = colors, cex = 0.6, font = 2
  )
  graphics::title(main = palette_id, cex.main = 1)
  par(op)

  invisible(p)
}

# -----------------------------------------------------------------------------
# 4. 代码生成
# -----------------------------------------------------------------------------

#' 生成 paletteer 函数调用代码
paletteer_r_code <- function(palette_id, n = NULL) {
  ptype <- .palette_type(palette_id)
  if (is.null(ptype) || ptype == "discrete") {
    if (is.null(n)) sprintf('paletteer_d("%s")', palette_id)
    else sprintf('paletteer_d("%s", %d)', palette_id, n)
  } else if (ptype == "continuous") {
    n_val <- if (is.null(n)) 10 else n
    sprintf('paletteer_c("%s", n = %d)', palette_id, n_val)
  } else {
    n_val <- if (is.null(n)) 5 else n
    sprintf('paletteer_dynamic("%s", %d)', palette_id, n_val)
  }
}

#' 生成 ggplot2 集成代码
paletteer_ggplot2_code <- function(palette_id) {
  ptype <- .palette_type(palette_id)
  if (!is.null(ptype) && ptype == "continuous") {
    sprintf(
      'library(ggplot2)\nlibrary(paletteer)\n\nggplot(data, aes(x, y, color = value)) +\n  geom_point() +\n  scale_color_paletteer_c("%s")',
      palette_id
    )
  } else {
    sprintf(
      'library(ggplot2)\nlibrary(paletteer)\n\nggplot(data, aes(x, y, color = group)) +\n  geom_point() +\n  scale_color_paletteer_d("%s")',
      palette_id
    )
  }
}

# -----------------------------------------------------------------------------
# 5. 命令行接口
# -----------------------------------------------------------------------------

.main <- function(argv = commandArgs(trailingOnly = TRUE)) {
  parse_flag <- function(name, has_value = TRUE, default = NULL) {
    idx <- match(name, argv)
    if (is.na(idx)) return(default)
    if (has_value) argv[idx + 1] else TRUE
  }
  # 整数参数（--n）：字符串转整数，NULL 保持不变
  parse_int <- function(name) {
    v <- parse_flag(name)
    if (is.null(v)) NULL else as.integer(v)
  }

  if (length(argv) == 0) {
    cat("paletteer_tools.R - R paletteer 便捷工具\n\n")
    cat("用法:\n")
    cat("  --list-packages                       列出所有源包\n")
    cat("  --list-by-type <type>                 列出调色板 (continuous/discrete/dynamic)\n")
    cat("  --list-by-category <cat>              列出调色板 (sequential/diverging/qualitative)\n")
    cat("  --list-by-package <pkg>               列出某包的调色板\n")
    cat("  --get <package::palette> [--n N]      获取调色板颜色\n")
    cat("  --search <keyword>                    关键词搜索\n")
    cat("  --recommend [--n N] [--category C]\n")
    cat("             [--type T] [--package P]   智能推荐\n")
    cat("  --plot <package::palette> [--n N]\n")
    cat("             [--save FILE]              绘制色块图\n")
    cat("  --r-code <package::palette> [--n N]   生成 paletteer R 代码\n")
    cat("  --ggplot2-code <package::palette>     生成 ggplot2 代码\n")
    return(invisible(NULL))
  }

  if (isTRUE(parse_flag("--list-packages", has_value = FALSE))) {
    .out(paletteer_list_packages())
  } else if (!is.null(parse_flag("--list-by-type"))) {
    .out(paletteer_list(type = parse_flag("--list-by-type")))
  } else if (!is.null(parse_flag("--list-by-category"))) {
    .out(paletteer_list(category = parse_flag("--list-by-category")))
  } else if (!is.null(parse_flag("--list-by-package"))) {
    .out(paletteer_list(package = parse_flag("--list-by-package")))
  } else if (!is.null(parse_flag("--get"))) {
    .out(paletteer_get(parse_flag("--get"), n = parse_int("--n")))
  } else if (!is.null(parse_flag("--search"))) {
    .out(paletteer_search(parse_flag("--search")))
  } else if (isTRUE(parse_flag("--recommend", has_value = FALSE))) {
    .out(paletteer_recommend(
      n_colors  = parse_int("--n"),
      category  = parse_flag("--category"),
      type      = parse_flag("--type"),
      package   = parse_flag("--package")
    ))
  } else if (!is.null(parse_flag("--plot"))) {
    p <- paletteer_plot(
      parse_flag("--plot"),
      n    = parse_int("--n"),
      save = parse_flag("--save")
    )
    cat("Plotted:", p$palette_id, "| colors:", length(p$colors), "\n")
  } else if (!is.null(parse_flag("--r-code"))) {
    cat(paletteer_r_code(parse_flag("--r-code"), n = parse_int("--n")), "\n")
  } else if (!is.null(parse_flag("--ggplot2-code"))) {
    cat(paletteer_ggplot2_code(parse_flag("--ggplot2-code")), "\n")
  } else {
    cat("Unknown arguments. Run with no arguments for usage.\n")
  }
}

# 仅在使用 Rscript 直接执行时运行 CLI
if (sys.nframe() == 0 && !interactive()) {
  .main()
}
