#!/usr/bin/env python3
"""
generate_palette_viz.py
=======================

Generate SVG or HTML visualizations of paletteer color palettes.
Produces self-contained files that can be opened in any browser.

Usage:
    python3 generate_palette_viz.py "wesanderson::Royal1" --format svg
    python3 generate_palette_viz.py "scico::berlin" --n 10 --format html
    python3 generate_palette_viz.py --from-json palette_data.json --format html
    python3 generate_palette_viz.py "nord::aurora" --format svg --output /tmp/aurora.svg
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from palettes_data import PALETTES, TYPE_TO_FUNCTION
from query_paletteer import get_palette


# ---------------------------------------------------------------------------
# SVG generation
# ---------------------------------------------------------------------------

def generate_svg(palette_info, output_path=None):
    """
    Generate an SVG file showing the palette as color swatches with labels.

    palette_info: dict with 'palette_id', 'colors', 'package', 'palette',
                  'type', 'category', 'description', 'colorblind_safe', 'print_friendly'
    """
    colors = palette_info.get("colors", [])
    n = len(colors)
    palette_id = palette_info.get("palette_id", "unknown")
    package = palette_info.get("package", "")
    palette_name = palette_info.get("palette", "")
    ptype = palette_info.get("type", "")
    category = palette_info.get("category", "")
    description = palette_info.get("description", "")
    cb_safe = palette_info.get("colorblind_safe")
    print_ok = palette_info.get("print_friendly")

    # Layout
    swatch_w = 120
    swatch_h = 80
    gap = 4
    label_h = 20
    hex_h = 16
    margin = 20
    header_h = 80

    if n == 0:
        total_w = 400
        total_h = header_h + 40
    else:
        total_w = max(n * (swatch_w + gap) - gap + margin * 2, 400)
        total_h = header_h + swatch_h + label_h + hex_h + margin

    svg_parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" '
        f'viewBox="0 0 {total_w} {total_h}" font-family="system-ui, -apple-system, sans-serif">',
        # Background
        f'<rect width="{total_w}" height="{total_h}" fill="#fafafa" rx="8"/>',
        # Header
        f'<text x="{margin}" y="28" font-size="16" font-weight="bold" fill="#1a1a1a">'
        f'{package}::{palette_name}</text>',
        f'<text x="{margin}" y="48" font-size="12" fill="#666">'
        f'type: {ptype} | category: {category} | colors: {n}</text>',
    ]

    if description:
        # Truncate long descriptions
        desc = description if len(description) <= 80 else description[:77] + "..."
        svg_parts.append(
            f'<text x="{margin}" y="66" font-size="11" fill="#999">{desc}</text>'
        )

    # Tags
    tag_x = total_w - margin
    if cb_safe is not None:
        tag_color = "#4caf50" if cb_safe else "#f44336"
        tag_text = "CB-safe" if cb_safe else "not CB-safe"
        svg_parts.append(
            f'<rect x="{tag_x - 70}" y="14" width="70" height="18" fill="{tag_color}" rx="4" opacity="0.15"/>'
            f'<text x="{tag_x - 35}" y="27" font-size="10" fill="{tag_color}" text-anchor="middle" font-weight="600">{tag_text}</text>'
        )
        tag_x -= 78
    if print_ok is not None:
        tag_color = "#2196f3" if print_ok else "#ff9800"
        tag_text = "print OK" if print_ok else "screen only"
        svg_parts.append(
            f'<rect x="{tag_x - 70}" y="14" width="70" height="18" fill="{tag_color}" rx="4" opacity="0.15"/>'
            f'<text x="{tag_x - 35}" y="27" font-size="10" fill="{tag_color}" text-anchor="middle" font-weight="600">{tag_text}</text>'
        )

    # Color swatches
    y_start = header_h
    for i, color in enumerate(colors):
        x = margin + i * (swatch_w + gap)
        # Normalize color to #RRGGBB
        hex_val = color.upper().lstrip("#")
        if len(hex_val) == 8:
            hex_val = hex_val[:6]
        hex_val = "#" + hex_val

        # Determine text color (dark on light, light on dark)
        r, g, b = int(hex_val[1:3], 16), int(hex_val[3:5], 16), int(hex_val[5:7], 16)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        text_color = "#333" if luminance > 0.5 else "#fff"

        # Swatch
        svg_parts.append(
            f'<rect x="{x}" y="{y_start}" width="{swatch_w}" height="{swatch_h}" '
            f'fill="{hex_val}" rx="4" stroke="#e0e0e0" stroke-width="1"/>'
        )
        # Index label
        svg_parts.append(
            f'<text x="{x + swatch_w / 2}" y="{y_start + 16}" font-size="11" '
            f'fill="{text_color}" text-anchor="middle" opacity="0.7">#{i + 1}</text>'
        )
        # HEX value
        svg_parts.append(
            f'<text x="{x + swatch_w / 2}" y="{y_start + swatch_h - 8}" font-size="11" '
            f'fill="{text_color}" text-anchor="middle" font-weight="600" '
            f'font-family="monospace">{hex_val}</text>'
        )

    # R code at bottom
    func = TYPE_TO_FUNCTION.get(ptype, "paletteer_d")
    if ptype == "continuous":
        r_code = f'{func}("{palette_id}", n = {n})'
    elif ptype == "dynamic":
        r_code = f'{func}("{palette_id}", {n})'
    else:
        r_code = f'{func}("{palette_id}")'

    svg_parts.append(
        f'<text x="{margin}" y="{total_h - 8}" font-size="11" fill="#888" '
        f'font-family="monospace">R: {r_code}</text>'
    )

    svg_parts.append("</svg>")

    svg_content = "\n".join(svg_parts)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        return output_path
    return svg_content


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

def generate_html(palette_info, output_path=None):
    """
    Generate a self-contained HTML file showing the palette with
    interactive swatches, R code, and ggplot2 examples.
    """
    colors = palette_info.get("colors", [])
    n = len(colors)
    palette_id = palette_info.get("palette_id", "unknown")
    package = palette_info.get("package", "")
    palette_name = palette_info.get("palette", "")
    ptype = palette_info.get("type", "")
    category = palette_info.get("category", "")
    description = palette_info.get("description", "")
    cb_safe = palette_info.get("colorblind_safe")
    print_ok = palette_info.get("print_friendly")

    # Generate R code
    func = TYPE_TO_FUNCTION.get(ptype, "paletteer_d")
    if ptype == "continuous":
        r_code = f'paletteer_c("{palette_id}", n = {n})'
    elif ptype == "dynamic":
        r_code = f'paletteer_dynamic("{palette_id}", {n})'
    else:
        r_code = f'paletteer_d("{palette_id}")'

    # Generate ggplot2 code
    if ptype == "continuous":
        ggplot_code = (
            f'ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Sepal.Length)) +\n'
            f'  geom_point(size = 3) +\n'
            f'  scale_color_paletteer_c("{palette_id}")'
        )
    else:
        ggplot_code = (
            f'ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Species)) +\n'
            f'  geom_point(size = 3) +\n'
            f'  scale_color_paletteer_d("{palette_id}")'
        )

    # Build swatches HTML
    swatches_html = ""
    for i, color in enumerate(colors):
        hex_val = color.upper().lstrip("#")
        if len(hex_val) == 8:
            hex_val = hex_val[:6]
        hex_display = "#" + hex_val
        r, g, b = int(hex_val[0:2], 16), int(hex_val[2:4], 16), int(hex_val[4:6], 16)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        text_color = "#333" if luminance > 0.5 else "#fff"

        swatches_html += f"""
        <div class="swatch" style="background: {hex_display};" onclick="copyToClipboard('{hex_display}')">
            <span class="swatch-index" style="color: {text_color};">#{i + 1}</span>
            <span class="swatch-hex" style="color: {text_color};">{hex_display}</span>
        </div>"""

    # Tags
    tags_html = ""
    if cb_safe is not None:
        tag_class = "tag tag-ok" if cb_safe else "tag tag-no"
        tag_text = "色盲友好 Colorblind-safe" if cb_safe else "非色盲友好 Not colorblind-safe"
        tags_html += f'<span class="{tag_class}">{tag_text}</span>'
    if print_ok is not None:
        tag_class = "tag tag-ok" if print_ok else "tag tag-warn"
        tag_text = "印刷友好 Print-friendly" if print_ok else "仅屏幕 Screen only"
        tags_html += f'<span class="{tag_class}">{tag_text}</span>'
    tags_html += f'<span class="tag tag-info">{ptype}</span>'
    tags_html += f'<span class="tag tag-info">{category}</span>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{palette_id} - paletteer</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
            background: #f5f5f5;
            color: #1a1a1a;
            padding: 24px;
            min-height: 100vh;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: #fff;
            border-radius: 12px;
            padding: 24px 28px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }}
        .header h1 {{
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 4px;
            font-family: "SF Mono", Monaco, monospace;
        }}
        .header .meta {{
            font-size: 13px;
            color: #888;
            margin-bottom: 12px;
        }}
        .header .desc {{
            font-size: 14px;
            color: #555;
            margin-bottom: 12px;
        }}
        .tags {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .tag {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }}
        .tag-ok {{ background: #e8f5e9; color: #2e7d32; }}
        .tag-no {{ background: #ffebee; color: #c62828; }}
        .tag-warn {{ background: #fff3e0; color: #e65100; }}
        .tag-info {{ background: #e3f2fd; color: #1565c0; }}
        .swatches {{
            display: flex;
            gap: 4px;
            margin-bottom: 16px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }}
        .swatch {{
            flex: 1;
            min-width: 80px;
            height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            padding: 12px 8px;
            cursor: pointer;
            transition: transform 0.15s, flex 0.15s;
        }}
        .swatch:hover {{
            flex: 1.5;
            transform: translateY(-2px);
        }}
        .swatch-index {{
            font-size: 12px;
            opacity: 0.7;
        }}
        .swatch-hex {{
            font-size: 12px;
            font-weight: 700;
            font-family: "SF Mono", Monaco, monospace;
        }}
        .code-section {{
            background: #fff;
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }}
        .code-section h2 {{
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #555;
        }}
        pre {{
            background: #1e1e2e;
            color: #cdd6f4;
            padding: 16px;
            border-radius: 8px;
            font-size: 13px;
            font-family: "SF Mono", Monaco, "Cascadia Code", monospace;
            overflow-x: auto;
            line-height: 1.6;
        }}
        .copy-hint {{
            font-size: 11px;
            color: #999;
            margin-top: 8px;
            text-align: center;
        }}
        .toast {{
            position: fixed;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            background: #333;
            color: #fff;
            padding: 10px 24px;
            border-radius: 8px;
            font-size: 13px;
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
            z-index: 1000;
        }}
        .toast.show {{ opacity: 1; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{palette_id}</h1>
            <div class="meta">package: {package} | palette: {palette_name} | colors: {n}</div>
            <div class="desc">{description}</div>
            <div class="tags">{tags_html}</div>
        </div>

        <div class="swatches">{swatches_html}
        </div>
        <div class="copy-hint">Click any color swatch to copy its HEX value</div>

        <div class="code-section">
            <h2>R Code</h2>
            <pre><code>library(paletteer)

{r_code}</code></pre>
        </div>

        <div class="code-section">
            <h2>ggplot2 Integration</h2>
            <pre><code>library(ggplot2)
library(paletteer)

{ggplot_code}</code></pre>
        </div>
    </div>

    <div class="toast" id="toast">Copied!</div>

    <script>
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(function() {{
                const toast = document.getElementById('toast');
                toast.textContent = 'Copied: ' + text;
                toast.classList.add('show');
                setTimeout(function() {{ toast.classList.remove('show'); }}, 1500);
            }});
        }}
    </script>
</body>
</html>"""

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path
    return html


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate palette visualizations (SVG or HTML)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "wesanderson::Royal1" --format svg
  %(prog)s "scico::berlin" --n 10 --format html
  %(prog)s "nord::aurora" --format svg --output ./aurora.svg
  %(prog)s --from-json palette.json --format html
        """,
    )

    parser.add_argument("palette", nargs="?", help="Palette name in 'package::palette' format")
    parser.add_argument("--n", type=int, default=None, help="Number of colors")
    parser.add_argument("--format", choices=["svg", "html"], default="html", help="Output format")
    parser.add_argument("--output", type=str, default=None, help="Output file path")
    parser.add_argument("--from-json", type=str, default=None, help="Read palette data from JSON file")
    parser.add_argument("--no-r", action="store_true", help="Use embedded database only")

    args = parser.parse_args()

    if args.from_json:
        with open(args.from_json, "r", encoding="utf-8") as f:
            palette_info = json.load(f)
    elif args.palette:
        palette_info = get_palette(args.palette, n=args.n, use_r=not args.no_r)
        if "error" in palette_info:
            print(json.dumps(palette_info, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        safe_name = palette_info.get("palette_id", "palette").replace("::", "_")
        ext = "svg" if args.format == "svg" else "html"
        output_path = os.path.join(os.getcwd(), f"palette_{safe_name}.{ext}")

    if args.format == "svg":
        generate_svg(palette_info, output_path)
    else:
        generate_html(palette_info, output_path)

    print(json.dumps({"output": output_path, "format": args.format}, ensure_ascii=False))


if __name__ == "__main__":
    main()
