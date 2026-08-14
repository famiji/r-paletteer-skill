#!/usr/bin/env python3
"""
query_paletteer.py
==================

Query paletteer palettes by package, type, category, or specific name.
Prioritizes live R/paletteer queries; falls back to the embedded offline database.

Usage:
    python3 query_paletteer.py --list-packages
    python3 query_paletteer.py --list-by-package wesanderson
    python3 query_paletteer.py --list-by-type discrete
    python3 query_paletteer.py --list-by-category qualitative
    python3 query_paletteer.py --get "wesanderson::Royal1"
    python3 query_paletteer.py --get "scico::berlin" --n 10
    python3 query_paletteer.py --search "blue"

Output: JSON to stdout with structured palette information.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

# Ensure we can import palettes_data regardless of cwd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from palettes_data import (
    PALETTES,
    PACKAGE_INFO,
    SCENARIO_ALIASES,
    TYPE_TO_FUNCTION,
    TYPE_TO_SCALE,
)


# ---------------------------------------------------------------------------
# R / paletteer query functions
# ---------------------------------------------------------------------------

def _find_rscript():
    """Locate Rscript binary on the system."""
    for candidate in ["Rscript", "/usr/local/bin/Rscript", "/opt/homebrew/bin/Rscript"]:
        path = shutil.which(candidate)
        if path:
            return path
    return None


def _r_paletteer_available():
    """Check if paletteer is installed in R."""
    rscript = _find_rscript()
    if not rscript:
        return False
    try:
        result = subprocess.run(
            [rscript, "-e", "suppressMessages(requireNamespace('paletteer', quietly = TRUE))"],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def _r_query_palette(palette_name, n=None):
    """Query a single palette from live R/paletteer. Returns colors list or None."""
    rscript = _find_rscript()
    if not rscript:
        return None

    # Determine type from embedded data if available, otherwise try all
    palette_key = palette_name
    if palette_key in PALETTES:
        ptype = PALETTES[palette_key]["type"]
        func = TYPE_TO_FUNCTION.get(ptype, "paletteer_d")
    else:
        func = "paletteer_d"  # default

    # Build R expression
    if func == "paletteer_c":
        n_val = n if n else 10
        r_expr = (
            f"cat(as.character(paletteer::paletteer_c('{palette_name}', n={n_val})), sep=' ')"
        )
    elif func == "paletteer_dynamic":
        n_val = n if n else 5
        r_expr = (
            f"cat(as.character(paletteer::paletteer_dynamic('{palette_name}', {n_val})), sep=' ')"
        )
    else:
        if n:
            r_expr = (
                f"cat(as.character(paletteer::paletteer_d('{palette_name}', n={n})), sep=' ')"
            )
        else:
            r_expr = (
                f"cat(as.character(paletteer::paletteer_d('{palette_name}')), sep=' ')"
            )

    try:
        result = subprocess.run(
            [rscript, "-e", r_expr],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            colors = result.stdout.strip().split()
            # Normalize hex format: remove alpha if 8-char, keep #
            normalized = []
            for c in colors:
                c = c.strip()
                if c.startswith("#") and len(c) == 9:
                    c = c[:7]  # strip alpha
                normalized.append(c.upper())
            return normalized if normalized else None
    except Exception:
        pass
    return None


def _r_list_palettes_by_type(ptype):
    """List all palettes of a given type from live R. Returns list of "pkg::name" strings."""
    rscript = _find_rscript()
    if not rscript:
        return None

    df_name = {"continuous": "palettes_c_names", "discrete": "palettes_d_names", "dynamic": "palettes_dynamic_names"}.get(ptype)
    if not df_name:
        return None

    r_expr = (
        f"df <- paletteer::{df_name}; "
        f"cat(paste(df$package, df$palette, sep='::'), sep='\\n')"
    )
    try:
        result = subprocess.run(
            [rscript, "-e", r_expr],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
            return lines
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Offline database query functions
# ---------------------------------------------------------------------------

def _normalize_palette_key(name):
    """Try to normalize a palette identifier to 'package::palette' form."""
    if "::" in name:
        return name
    # Try matching case-insensitively against known keys
    lower = name.lower()
    for key in PALETTES:
        if key.lower() == lower:
            return key
    return name


def get_palette(palette_name, n=None, use_r=True):
    """
    Get a specific palette by 'package::palette' name.

    Returns a dict with: package, palette, type, category, colorblind_safe,
    print_friendly, max_colors, colors, description, n_requested, source
    """
    palette_name = _normalize_palette_key(palette_name)

    # Try live R first
    if use_r and _r_paletteer_available():
        r_colors = _r_query_palette(palette_name, n)
        if r_colors:
            # Enrich with metadata from embedded db if available
            meta = PALETTES.get(palette_name, {})
            return {
                "palette_id": palette_name,
                "package": palette_name.split("::")[0] if "::" in palette_name else "",
                "palette": palette_name.split("::")[1] if "::" in palette_name else palette_name,
                "type": meta.get("type", "discrete"),
                "category": meta.get("category", "unknown"),
                "colorblind_safe": meta.get("colorblind_safe", None),
                "print_friendly": meta.get("print_friendly", None),
                "max_colors": meta.get("max_colors", None),
                "n_requested": n,
                "colors": r_colors,
                "description": meta.get("description", ""),
                "source": "R_paletteer",
            }

    # Fall back to embedded data
    if palette_name in PALETTES:
        entry = PALETTES[palette_name]
        colors = list(entry["colors"])

        # If n is specified and different from default, try to sub-sample or pad
        if n and n != len(colors):
            if entry["type"] == "continuous":
                # Interpolate: sample n colors evenly from the available set
                if len(colors) > 1:
                    step = (len(colors) - 1) / (n - 1) if n > 1 else 0
                    sampled = [colors[int(round(i * step))] for i in range(n)]
                    colors = sampled
            elif n < len(colors):
                colors = colors[:n]
            # If n > len(colors) for discrete, we can't generate more — keep original
            # and note the limitation

        return {
            "palette_id": palette_name,
            "package": entry["package"],
            "palette": entry["palette"],
            "type": entry["type"],
            "category": entry["category"],
            "colorblind_safe": entry["colorblind_safe"],
            "print_friendly": entry["print_friendly"],
            "max_colors": entry["max_colors"],
            "n_requested": n,
            "colors": colors,
            "description": entry["description"],
            "source": "embedded_db",
        }

    return {"error": f"Palette '{palette_name}' not found in embedded database or R environment."}


def list_by_package(pkg_name, use_r=True):
    """List all palettes from a specific source package."""
    results = []

    # Embedded data
    for key, entry in PALETTES.items():
        if entry["package"].lower() == pkg_name.lower():
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
                "source": "embedded_db",
            })

    # Try R for complete list
    if use_r and _r_paletteer_available():
        for ptype in ["continuous", "discrete", "dynamic"]:
            r_list = _r_list_palettes_by_type(ptype)
            if r_list:
                existing_keys = {r["palette_id"] for r in results}
                for pname in r_list:
                    if pname.lower().startswith(pkg_name.lower() + "::") and pname not in existing_keys:
                        parts = pname.split("::")
                        results.append({
                            "palette_id": pname,
                            "package": parts[0],
                            "palette": parts[1],
                            "type": ptype,
                            "category": "unknown",
                            "colorblind_safe": None,
                            "print_friendly": None,
                            "max_colors": None,
                            "num_colors": None,
                            "colors": [],
                            "description": "",
                            "source": "R_paletteer",
                        })

    return results


def list_by_type(ptype, use_r=True):
    """List all palettes of a specific paletteer type (continuous/discrete/dynamic)."""
    results = []

    # Embedded data
    for key, entry in PALETTES.items():
        if entry["type"] == ptype:
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
                "source": "embedded_db",
            })

    # Try R for complete list
    if use_r and _r_paletteer_available():
        r_list = _r_list_palettes_by_type(ptype)
        if r_list:
            existing_keys = {r["palette_id"] for r in results}
            for pname in r_list:
                if pname not in existing_keys:
                    parts = pname.split("::")
                    results.append({
                        "palette_id": pname,
                        "package": parts[0],
                        "palette": parts[1],
                        "type": ptype,
                        "category": "unknown",
                        "colorblind_safe": None,
                        "print_friendly": None,
                        "max_colors": None,
                        "num_colors": None,
                        "colors": [],
                        "description": "",
                        "source": "R_paletteer",
                    })

    return results


def list_by_category(category, use_r=True):
    """List all palettes of a specific category (sequential/diverging/qualitative)."""
    results = []
    for key, entry in PALETTES.items():
        if entry["category"] == category:
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
                "source": "embedded_db",
            })
    return results


def list_packages(use_r=True):
    """List all known paletteer source packages."""
    packages = {}

    # From embedded info
    for pkg, info in PACKAGE_INFO.items():
        packages[pkg] = {
            "package": pkg,
            "types": info["types"],
            "cran": info.get("cran", None),
            "description": info["description"],
            "embedded_palettes": 0,
            "source": "embedded_db",
        }

    # Count embedded palettes per package
    for key, entry in PALETTES.items():
        pkg = entry["package"]
        if pkg in packages:
            packages[pkg]["embedded_palettes"] += 1

    # Try R for total count
    if use_r and _r_paletteer_available():
        rscript = _find_rscript()
        r_expr = (
            "df <- paletteer::paletteer_packages; "
            "cat(paste(df$packages, df$github_version, df$cran_version, sep='\t'), sep='\\n')"
        )
        try:
            result = subprocess.run(
                [rscript, "-e", r_expr],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0 and result.stdout.strip():
                for line in result.stdout.strip().split("\n"):
                    parts = line.split("\t")
                    if len(parts) >= 1:
                        pkg = parts[0].strip()
                        if pkg and pkg not in packages:
                            packages[pkg] = {
                                "package": pkg,
                                "types": [],
                                "cran": len(parts) >= 3 and parts[2].strip() != "" and parts[2].strip() != "NA",
                                "description": "",
                                "embedded_palettes": 0,
                                "source": "R_paletteer",
                            }
        except Exception:
            pass

    return list(packages.values())


def search_palettes(query, use_r=True):
    """Search palettes by keyword in name, description, or package."""
    query_lower = query.lower()
    # Check if query is a Chinese alias
    resolved = SCENARIO_ALIASES.get(query_lower, query_lower)

    results = []
    for key, entry in PALETTES.items():
        searchable = " ".join([
            key, entry["package"], entry["palette"],
            entry["category"], entry["description"],
            "colorblind" if entry["colorblind_safe"] else "",
            "print" if entry["print_friendly"] else "",
        ]).lower()

        if query_lower in searchable or resolved in searchable or resolved in entry["category"]:
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
                "source": "embedded_db",
            })

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Query paletteer palettes (R or offline database)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list-packages
  %(prog)s --list-by-package wesanderson
  %(prog)s --list-by-type discrete
  %(prog)s --list-by-category qualitative
  %(prog)s --get "wesanderson::Royal1"
  %(prog)s --get "scico::berlin" --n 10
  %(prog)s --search "colorblind"
  %(prog)s --get "nord::frost" --no-r
        """,
    )
    parser.add_argument("--list-packages", action="store_true", help="List all known source packages")
    parser.add_argument("--list-by-package", type=str, help="List palettes from a specific package")
    parser.add_argument("--list-by-type", type=str, choices=["continuous", "discrete", "dynamic"], help="List palettes by paletteer type")
    parser.add_argument("--list-by-category", type=str, choices=["sequential", "diverging", "qualitative"], help="List palettes by color category")
    parser.add_argument("--get", type=str, help="Get a specific palette by 'package::palette' name")
    parser.add_argument("--search", type=str, help="Search palettes by keyword (supports Chinese)")
    parser.add_argument("--n", type=int, default=None, help="Number of colors to retrieve")
    parser.add_argument("--no-r", action="store_true", help="Skip R/paletteer, use embedded database only")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")

    args = parser.parse_args()
    use_r = not args.no_r

    if args.list_packages:
        result = list_packages(use_r=use_r)
    elif args.list_by_package:
        result = list_by_package(args.list_by_package, use_r=use_r)
    elif args.list_by_type:
        result = list_by_type(args.list_by_type, use_r=use_r)
    elif args.list_by_category:
        result = list_by_category(args.list_by_category, use_r=use_r)
    elif args.get:
        result = get_palette(args.get, n=args.n, use_r=use_r)
    elif args.search:
        result = search_palettes(args.search, use_r=use_r)
    else:
        parser.print_help()
        sys.exit(1)

    indent = 2 if args.pretty else None
    print(json.dumps(result, ensure_ascii=False, indent=indent))


if __name__ == "__main__":
    main()
