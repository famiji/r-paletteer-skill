#!/usr/bin/env python3
"""
recommend_palettes.py
=====================

Smart palette recommendation engine for paletteer.
Recommends palettes based on color count, style, scenario, and constraints.
Supports both Chinese and English input.

Usage:
    python3 recommend_palettes.py --n 5 --category qualitative --colorblind
    python3 recommend_palettes.py --n 8 --scenario academic
    python3 recommend_palettes.py --n 7 --style warm --colorblind --print
    python3 recommend_palettes.py --n 12 --category qualitative
    python3 recommend_palettes.py --scenario 论文 --n 6 --色盲友好

Output: JSON to stdout with ranked recommendations + R code snippets.
"""

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from palettes_data import (
    PALETTES,
    PACKAGE_INFO,
    SCENARIO_ALIASES,
    TYPE_TO_FUNCTION,
    TYPE_TO_SCALE,
)


# ---------------------------------------------------------------------------
# Color analysis helpers
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_color):
    """Convert #RRGGBB to (r, g, b) tuple (0-255)."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 8:
        hex_color = hex_color[:6]
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def _rgb_to_hsl(r, g, b):
    """Convert RGB (0-255) to HSL (0-1 for H,S,L)."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c
    l = (max_c + min_c) / 2

    if diff == 0:
        h = s = 0
    else:
        s = diff / (2 - max_c - min_c) if l > 0.5 else diff / (max_c + min_c)
        if max_c == r:
            h = ((g - b) / diff) % 6
        elif max_c == g:
            h = (b - r) / diff + 2
        else:
            h = (r - g) / diff + 4
        h /= 6

    return h, s, l


def _analyze_palette(colors):
    """Analyze a palette's color properties."""
    if not colors:
        return None

    hsls = []
    brightnesses = []
    saturations = []

    for c in colors:
        rgb = _hex_to_rgb(c)
        if rgb:
            h, s, l = _rgb_to_hsl(*rgb)
            hsls.append((h, s, l))
            brightnesses.append(l)
            saturations.append(s)

    if not hsls:
        return None

    avg_brightness = sum(brightnesses) / len(brightnesses)
    avg_saturation = sum(saturations) / len(saturations)
    brightness_range = max(brightnesses) - min(brightnesses) if brightnesses else 0

    # Determine warmth: red/orange/yellow hues are warm, blue/cyan/green are cool
    warm_count = 0
    for h, s, l in hsls:
        if s > 0.1:  # not grey
            if h < 0.15 or h > 0.85:  # red-orange
                warm_count += 1
            elif 0.05 < h < 0.2:  # orange-yellow
                warm_count += 1

    warmth = warm_count / len(hsls) if hsls else 0.5

    return {
        "avg_brightness": round(avg_brightness, 3),
        "avg_saturation": round(avg_saturation, 3),
        "brightness_range": round(brightness_range, 3),
        "warmth": round(warmth, 3),  # 0=cool, 1=warm
        "is_dark": avg_brightness < 0.4,
        "is_light": avg_brightness > 0.65,
        "is_vivid": avg_saturation > 0.6,
        "is_pastel": avg_saturation < 0.35 and avg_brightness > 0.6,
        "is_muted": avg_saturation < 0.35 and avg_brightness < 0.6,
        "is_greyscale": avg_saturation < 0.1,
        "is_rainbow": brightness_range > 0.5 and avg_saturation > 0.4,
    }


# ---------------------------------------------------------------------------
# Recommendation engine
# ---------------------------------------------------------------------------

def recommend(
    n_colors=None,
    category=None,
    palette_type=None,
    colorblind_safe=False,
    print_friendly=False,
    style=None,
    scenario=None,
    package=None,
    max_results=10,
):
    """
    Recommend palettes based on constraints. Returns a ranked list of dicts.

    Each result includes:
        - palette metadata (name, package, type, colors, etc.)
        - match_score (0-100)
        - match_reasons (list of strings explaining the match)
        - r_code (R code snippet for this palette)
        - ggplot2_code (ggplot2 integration code)
    """
    # Resolve scenario/style aliases
    resolved_tags = set()
    for tag in [category, style, scenario]:
        if tag:
            tag_lower = tag.lower().strip()
            resolved = SCENARIO_ALIASES.get(tag_lower, tag_lower)
            resolved_tags.add(resolved)

    # Map resolved tags to filter criteria
    want_category = None
    if "sequential" in resolved_tags:
        want_category = "sequential"
    elif "diverging" in resolved_tags:
        want_category = "diverging"
    elif "qualitative" in resolved_tags:
        want_category = "qualitative"

    want_colorblind = colorblind_safe or "colorblind" in resolved_tags
    want_print = print_friendly or "print" in resolved_tags
    want_academic = "academic" in resolved_tags
    want_business = "business" in resolved_tags
    want_artistic = "artistic" in resolved_tags
    want_nature = "nature" in resolved_tags
    want_warm = "warm" in resolved_tags
    want_cool = "cool" in resolved_tags
    want_bright = "bright" in resolved_tags
    want_vivid = "vivid" in resolved_tags
    want_pastel = "pastel" in resolved_tags
    want_dark = "dark" in resolved_tags
    want_light = "light" in resolved_tags
    want_muted = "muted" in resolved_tags
    want_earth = "earth" in resolved_tags
    want_rainbow = "rainbow" in resolved_tags
    want_greyscale = "greyscale" in resolved_tags

    # Override category for specific style requests
    if want_greyscale and not want_category:
        want_category = "sequential"
    if want_rainbow and not want_category:
        want_category = "diverging"

    # Academic scenario: prefer ggsci, scico, RColorBrewer
    academic_packages = {"ggsci", "scico", "RColorBrewer", "khroma", "ggthemes"}
    business_packages = {"RColorBrewer", "rcartocolor", "ggsci", "viridis"}
    nature_packages = {"nationalparkcolors", "MetBrewer", "ghibli", "calecopal", "soilpalettes", "feathers", "fishualize"}
    artistic_packages = {"wesanderson", "MetBrewer", "ghibli", "dutchmasters", "vangogh", "nationalparkcolors"}

    results = []

    for key, entry in PALETTES.items():
        score = 0
        reasons = []

        # --- Hard filters ---
        if want_category and entry["category"] != want_category:
            continue

        if palette_type and entry["type"] != palette_type:
            continue

        if package and entry["package"].lower() != package.lower():
            continue

        if want_colorblind and not entry["colorblind_safe"]:
            continue

        if want_print and not entry["print_friendly"]:
            continue

        # --- Color count matching ---
        if n_colors:
            max_c = entry["max_colors"]
            if entry["type"] == "continuous":
                # Continuous palettes can generate any number of colors
                score += 20
                reasons.append(f"continuous: can generate {n_colors} colors")
            elif max_c is None:
                score += 10
            elif max_c >= n_colors:
                score += 25
                reasons.append(f"supports {n_colors} colors (max {max_c})")
            elif max_c >= n_colors - 2:
                score += 10
                reasons.append(f"close fit: {n_colors} requested, max {max_c}")
            else:
                # Too few colors available
                score -= 30
                reasons.append(f"limited: only {max_c} colors available (need {n_colors})")

        # --- Style matching via color analysis ---
        analysis = _analyze_palette(entry["colors"])
        if analysis:
            if want_warm and analysis["warmth"] > 0.4:
                score += 20
                reasons.append("warm color tones")
            if want_cool and analysis["warmth"] < 0.3:
                score += 20
                reasons.append("cool color tones")
            if want_bright and analysis["avg_brightness"] > 0.6:
                score += 15
                reasons.append("bright/light palette")
            if want_vivid and analysis["is_vivid"]:
                score += 20
                reasons.append("vivid, high saturation")
            if want_pastel and analysis["is_pastel"]:
                score += 25
                reasons.append("pastel, soft tones")
            if want_dark and analysis["is_dark"]:
                score += 20
                reasons.append("dark palette")
            if want_light and analysis["is_light"]:
                score += 15
                reasons.append("light palette")
            if want_muted and analysis["is_muted"]:
                score += 20
                reasons.append("muted, low saturation")
            if want_earth and analysis["avg_saturation"] < 0.5 and not analysis["is_greyscale"]:
                score += 15
                reasons.append("earth tones")
            if want_greyscale and analysis["is_greyscale"]:
                score += 30
                reasons.append("greyscale/monochrome")
            if want_rainbow and analysis["is_rainbow"]:
                score += 25
                reasons.append("rainbow-like spectrum")

        # --- Scenario matching ---
        if want_academic:
            if entry["package"] in academic_packages:
                score += 25
                reasons.append(f"academic-friendly source: {entry['package']}")
            if entry["colorblind_safe"]:
                score += 10
                reasons.append("colorblind-safe (important for publications)")
            if entry["print_friendly"]:
                score += 5
                reasons.append("print-friendly")

        if want_business:
            if entry["package"] in business_packages:
                score += 20
                reasons.append(f"business-friendly source: {entry['package']}")
            if entry["print_friendly"]:
                score += 10
                reasons.append("print-friendly for reports")

        if want_nature:
            if entry["package"] in nature_packages:
                score += 30
                reasons.append(f"nature-inspired source: {entry['package']}")

        if want_artistic:
            if entry["package"] in artistic_packages:
                score += 25
                reasons.append(f"artistic/creative source: {entry['package']}")

        # --- Base score for having metadata ---
        score += 5
        if entry["colorblind_safe"]:
            score += 3
        if entry["print_friendly"]:
            score += 2

        # Cap at 100
        score = min(score, 100)

        if score > 0:
            # Generate R code
            r_code = _generate_r_code(key, entry, n_colors)
            ggplot2_code = _generate_ggplot2_code(key, entry, n_colors)

            results.append({
                "palette_id": key,
                "package": entry["package"],
                "palette": entry["palette"],
                "type": entry["type"],
                "category": entry["category"],
                "colorblind_safe": entry["colorblind_safe"],
                "print_friendly": entry["print_friendly"],
                "max_colors": entry["max_colors"],
                "num_colors": len(entry["colors"]),
                "colors": entry["colors"],
                "description": entry["description"],
                "match_score": score,
                "match_reasons": reasons,
                "r_code": r_code,
                "ggplot2_code": ggplot2_code,
            })

    # Sort by score descending, then by package/palette name
    results.sort(key=lambda x: (-x["match_score"], x["package"], x["palette"]))

    return results[:max_results]


def _generate_r_code(palette_id, entry, n=None):
    """Generate R code snippet for retrieving this palette."""
    func = TYPE_TO_FUNCTION.get(entry["type"], "paletteer_d")

    if entry["type"] == "continuous":
        n_val = n if n else 10
        return f'paletteer_c("{palette_id}", n = {n_val})'
    elif entry["type"] == "dynamic":
        n_val = n if n else 5
        return f'paletteer_dynamic("{palette_id}", {n_val})'
    else:  # discrete
        if n and n < len(entry["colors"]):
            return f'paletteer_d("{palette_id}", {n})'
        else:
            return f'paletteer_d("{palette_id}")'


def _generate_ggplot2_code(palette_id, entry, n=None):
    """Generate ggplot2 integration code snippet."""
    scales = TYPE_TO_SCALE.get(entry["type"], {})
    color_scale = scales.get("color", "scale_color_paletteer_d")
    fill_scale = scales.get("fill", "scale_fill_paletteer_d")

    if entry["type"] == "continuous":
        return (
            f'library(ggplot2)\n'
            f'library(paletteer)\n\n'
            f'# Continuous color scale\n'
            f'ggplot(data, aes(x, y, color = value)) +\n'
            f'  geom_point() +\n'
            f'  {color_scale}("{palette_id}")\n\n'
            f'# Continuous fill scale (e.g. for raster/heatmap)\n'
            f'ggplot(data, aes(x, y, fill = value)) +\n'
            f'  geom_raster() +\n'
            f'  {fill_scale}("{palette_id}")'
        )
    else:
        return (
            f'library(ggplot2)\n'
            f'library(paletteer)\n\n'
            f'# Discrete color scale\n'
            f'ggplot(data, aes(x, y, color = group)) +\n'
            f'  geom_point() +\n'
            f'  {color_scale}("{palette_id}")\n\n'
            f'# Discrete fill scale\n'
            f'ggplot(data, aes(x, fill = group)) +\n'
            f'  geom_bar() +\n'
            f'  {fill_scale}("{palette_id}")'
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Smart palette recommendation engine for paletteer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Recommend 5-color qualitative palettes that are colorblind-safe
  %(prog)s --n 5 --category qualitative --colorblind

  # Recommend palettes for academic publication
  %(prog)s --scenario academic --n 7

  # Recommend warm-toned palettes for 8 categories
  %(prog)s --n 8 --style warm

  # Recommend colorblind-safe continuous palettes (Chinese input)
  %(prog)s --n 10 --色盲友好 --连续型

  # Recommend nature-inspired palettes
  %(prog)s --scenario nature --n 6
        """,
    )

    parser.add_argument("--n", type=int, default=None, help="Number of colors needed")
    parser.add_argument("--category", type=str, default=None,
                        choices=["sequential", "diverging", "qualitative"],
                        help="Color category (or use Chinese: 顺序型/发散型/定性型)")
    parser.add_argument("--type", type=str, default=None,
                        choices=["continuous", "discrete", "dynamic"],
                        help="paletteer function type (or use Chinese: 连续型/离散型/动态型)")
    parser.add_argument("--style", type=str, default=None,
                        help="Color style: warm/cool/bright/vivid/pastel/dark/light/muted/earth/rainbow/greyscale")
    parser.add_argument("--scenario", type=str, default=None,
                        help="Use case: academic/business/artistic/nature")
    parser.add_argument("--package", type=str, default=None,
                        help="Filter to a specific source package")
    parser.add_argument("--colorblind", action="store_true", help="Only colorblind-safe palettes")
    parser.add_argument("--print", action="store_true", help="Only print-friendly palettes")
    parser.add_argument("--max-results", type=int, default=10, help="Max recommendations to return")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")

    # Chinese aliases
    parser.add_argument("--色盲友好", action="store_true", help="Alias for --colorblind")
    parser.add_argument("--印刷友好", action="store_true", help="Alias for --print")
    parser.add_argument("--连续型", action="store_true", help="Alias for --type continuous")
    parser.add_argument("--离散型", action="store_true", help="Alias for --type discrete")
    parser.add_argument("--动态型", action="store_true", help="Alias for --type dynamic")
    parser.add_argument("--顺序型", action="store_true", help="Alias for --category sequential")
    parser.add_argument("--发散型", action="store_true", help="Alias for --category diverging")
    parser.add_argument("--定性型", action="store_true", help="Alias for --category qualitative")
    parser.add_argument("--风格", type=str, default=None, help="Alias for --style")
    parser.add_argument("--场景", type=str, default=None, help="Alias for --scenario")
    parser.add_argument("--数量", type=int, default=None, help="Alias for --n")

    args = parser.parse_args()

    # Merge Chinese aliases
    n = args.n or args.数量
    category = args.category
    if args.顺序型:
        category = "sequential"
    elif args.发散型:
        category = "diverging"
    elif args.定性型:
        category = "qualitative"

    palette_type = args.type
    if args.连续型:
        palette_type = "continuous"
    elif args.离散型:
        palette_type = "discrete"
    elif args.动态型:
        palette_type = "dynamic"

    colorblind = args.colorblind or args.色盲友好
    print_friendly = args.print or args.印刷友好
    style = args.style or args.风格
    scenario = args.scenario or args.场景

    result = recommend(
        n_colors=n,
        category=category,
        palette_type=palette_type,
        colorblind_safe=colorblind,
        print_friendly=print_friendly,
        style=style,
        scenario=scenario,
        package=args.package,
        max_results=args.max_results,
    )

    indent = 2 if args.pretty else None
    print(json.dumps(result, ensure_ascii=False, indent=indent))


if __name__ == "__main__":
    main()
