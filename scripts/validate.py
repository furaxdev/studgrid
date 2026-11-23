#!/usr/bin/env python3
"""Quality gates for the studgrid-ui skill.

Prints a table with the real count of every gate and exits 0 only when all gates pass.
A missing artefact is a failure, never a pass.

Usage: python scripts/validate.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_TEARDOWNS = 12
MIN_STYLES = 54
MIN_TEMPLATES = 12
MIN_ICONS = 80
TEMPLATE_NAMES = [
    "login", "main-menu", "settings", "inventory-grid", "shop", "quest-log",
    "leaderboard", "chat", "dialog", "hud-overlay", "loading", "error-modal",
]


def rel_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    chans = []
    for i in (0, 2, 4):
        c = int(h[i : i + 2], 16) / 255
        chans.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = chans
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = sorted((rel_luminance(a), rel_luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def check_catalog() -> tuple[bool, str]:
    p = ROOT / "docs" / "refs" / "catalog.json"
    if not p.exists():
        return False, "catalog.json absent"
    d = json.loads(p.read_text(encoding="utf-8"))
    n = d.get("count", 0)
    return n > 0, f"{n} captures"


def check_teardowns() -> tuple[bool, str]:
    files = sorted((ROOT / "references" / "teardowns").glob("*.md"))
    ok = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        if re.search(r"https?://\S+\.(png|jpe?g|webp|gif)", text) and re.search(r"palette", text, re.I):
            ok += 1
    return ok >= MIN_TEARDOWNS, f"{ok}/{MIN_TEARDOWNS} teardowns avec capture + palette"


def check_styles() -> tuple[bool, str]:
    p = ROOT / "styles" / "_index.md"
    if not p.exists():
        return False, "styles/_index.md absent"
    rows = [l for l in p.read_text(encoding="utf-8").splitlines() if l.startswith("|") and "---" not in l]
    rows = rows[1:] if rows else rows  # header
    cited = [r for r in rows if re.search(r"https?://|catalog\.json|teardowns/", r)]
    return len(cited) >= MIN_STYLES, f"{len(cited)}/{MIN_STYLES} styles cités"


def check_templates() -> tuple[bool, str]:
    present = [n for n in TEMPLATE_NAMES if (ROOT / "templates" / f"{n}.lua").exists()]
    ok = len(present) >= MIN_TEMPLATES
    bad = []
    for n in present:
        text = (ROOT / "templates" / f"{n}.lua").read_text(encoding="utf-8")
        if "return function(parent: Instance, tokens: {})" not in text:
            bad.append(n)
    return ok and not bad, f"{len(present)}/{MIN_TEMPLATES} Lua, signature invalide: {bad or 'aucune'}"


def check_icons() -> tuple[bool, str]:
    p = ROOT / "icons" / "manifest.json"
    if not p.exists():
        return False, "icons/manifest.json absent"
    items = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(items, dict):
        items = items.get("icons", [])
    missing = [i for i in items if not all(i.get(k) for k in ("path", "license", "source", "category"))]
    return len(items) >= MIN_ICONS and not missing, f"{len(items)}/{MIN_ICONS} icônes, sans licence/source: {len(missing)}"


def check_palettes() -> tuple[bool, str]:
    p = ROOT / "styles" / "palettes.json"
    if not p.exists():
        return False, "styles/palettes.json absent"
    data = json.loads(p.read_text(encoding="utf-8"))
    fails = []
    for name, pal in data.items():
        for pair in pal.get("text_on_bg", []):
            if contrast(pair["text"], pair["bg"]) < 4.5:
                fails.append(f"{name}:{pair['text']}/{pair['bg']}")
    return not fails, f"{len(data)} palettes, contraste < 4.5 : {fails or 'aucun'}"


def check_asset_ids() -> tuple[bool, str]:
    hits = []
    for f in ROOT.rglob("*"):
        if not f.is_file() or ".git" in f.parts or ".cache" in f.parts:
            continue
        if f.suffix.lower() not in {".lua", ".md", ".html", ".json"}:
            continue
        if "rbxassetid://0" in f.read_text(encoding="utf-8", errors="ignore"):
            hits.append(str(f.relative_to(ROOT)))
    return not hits, f"rbxassetid://0 : {hits or 'aucun'}"


GATES = [
    ("catalogue DevForum", check_catalog),
    ("teardowns", check_teardowns),
    ("styles cités", check_styles),
    ("templates Lua", check_templates),
    ("icônes", check_icons),
    ("palettes / contraste", check_palettes),
    ("ids Roblox", check_asset_ids),
]


def main() -> int:
    results = []
    for name, fn in GATES:
        ok, detail = fn()
        results.append((name, ok, detail))
    width = max(len(n) for n, _, _ in results)
    print(f"{'GATE'.ljust(width)}  STATUT  DÉTAIL")
    for name, ok, detail in results:
        print(f"{name.ljust(width)}  {'OK' if ok else 'ÉCHEC'}    {detail}")
    all_ok = all(ok for _, ok, _ in results)
    print("\nRÉSULTAT :", "tous les gates passent" if all_ok else "gates en échec")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
