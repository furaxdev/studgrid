#!/usr/bin/env python3
"""Generate the studgrid icon set: 80 SVG glyphs (24x24, 2 px stroke, currentColor).

Every glyph is written from the primitives below, so the whole set is reproducible
from this file. Output:
  icons/svg/<name>.svg
  icons/manifest.json   (path, size, license, source, category)

License: CC0-like, authored in this repository (source: scripts/build_icons.py).
Roblox-owned asset ids are NOT used here; manifest lists none.

Usage: python scripts/build_icons.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "icons"
SVG_DIR = OUT / "svg"
SIZE = 24


def c(cx, cy, r):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'


def r(x, y, w, h, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'


def l(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'


def p(d, fill=False):
    return f'<path d="{d}"{" fill=\"currentColor\"" if fill else ""}/>'


def poly(points, closed=True):
    pts = " ".join(f"{x},{y}" for x, y in points)
    tag = "polygon" if closed else "polyline"
    return f'<{tag} points="{pts}"/>'


# name -> (category, primitives)
ICONS: dict[str, tuple[str, list[str]]] = {
    # Navigation
    "arrow-left": ("nav", [p("M19 12H5"), p("M11 6l-6 6 6 6")]),
    "arrow-right": ("nav", [p("M5 12h14"), p("M13 6l6 6-6 6")]),
    "arrow-up": ("nav", [p("M12 19V5"), p("M6 11l6-6 6 6")]),
    "arrow-down": ("nav", [p("M12 5v14"), p("M6 13l6 6 6-6")]),
    "chevron-left": ("nav", [poly([(15, 6), (9, 12), (15, 18)], False)]),
    "chevron-right": ("nav", [poly([(9, 6), (15, 12), (9, 18)], False)]),
    "menu": ("nav", [l(4, 6, 20, 6), l(4, 12, 20, 12), l(4, 18, 20, 18)]),
    "close": ("nav", [l(6, 6, 18, 18), l(18, 6, 6, 18)]),
    "home": ("nav", [p("M4 11l8-7 8 7"), p("M6 10v10h12V10")]),
    "map": ("nav", [poly([(3, 6), (9, 4), (15, 6), (21, 4), (21, 18), (15, 20), (9, 18), (3, 20)]), l(9, 4, 9, 18), l(15, 6, 15, 20)]),
    "compass": ("nav", [c(12, 12, 9), p("M15 9l-2 5-4 1 2-5z")]),
    "target": ("nav", [c(12, 12, 9), c(12, 12, 5), c(12, 12, 1)]),
    "flag": ("nav", [l(5, 21, 5, 3), p("M5 4h12l-2 4 2 4H5")]),
    # Actions
    "plus": ("action", [l(12, 5, 12, 19), l(5, 12, 19, 12)]),
    "minus": ("action", [l(5, 12, 19, 12)]),
    "check": ("action", [p("M5 12l4 4 10-10")]),
    "edit": ("action", [p("M4 20h4L19 9l-4-4L4 16z"), l(13, 7, 17, 11)]),
    "trash": ("action", [l(4, 7, 20, 7), p("M9 7V4h6v3"), p("M6 7l1 13h10l1-13")]),
    "save": ("action", [p("M5 3h11l3 3v15H5z"), r(8, 3, 6, 5), r(8, 13, 8, 8)]),
    "download": ("action", [l(12, 4, 12, 15), p("M7 11l5 5 5-5"), l(4, 20, 20, 20)]),
    "upload": ("action", [l(12, 15, 12, 4), p("M7 9l5-5 5 5"), l(4, 20, 20, 20)]),
    "refresh": ("action", [p("M20 11a8 8 0 1 0-2 5.3"), p("M20 4v7h-7")]),
    "share": ("action", [c(18, 5, 2), c(6, 12, 2), c(18, 19, 2), l(8, 11, 16, 6), l(8, 13, 16, 18)]),
    "link": ("action", [p("M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"), p("M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1")]),
    "search": ("action", [c(11, 11, 7), l(16, 16, 21, 21)]),
    "filter": ("action", [poly([(3, 5), (21, 5), (14, 13), (14, 20), (10, 18), (10, 13)], True)]),
    "sort": ("action", [l(7, 4, 7, 20), p("M3 16l4 4 4-4"), l(17, 20, 17, 4), p("M13 8l4-4 4 4")]),
    "undo": ("action", [p("M9 14L4 9l5-5"), p("M4 9h10a6 6 0 0 1 0 12h-3")]),
    "redo": ("action", [p("M15 14l5-5-5-5"), p("M20 9H10a6 6 0 0 0 0 12h3")]),
    "copy": ("action", [r(8, 8, 12, 12, 2), p("M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3")]),
    "lock": ("action", [r(5, 11, 14, 10, 2), p("M8 11V7a4 4 0 0 1 8 0v4")]),
    "unlock": ("action", [r(5, 11, 14, 10, 2), p("M8 11V7a4 4 0 0 1 7.7-1.5")]),
    "key": ("action", [c(8, 15, 4), l(11, 12, 20, 3), l(17, 6, 20, 9)]),
    "power": ("action", [p("M12 3v8"), p("M6.3 6.3a8 8 0 1 0 11.4 0")]),
    "settings": ("action", [c(12, 12, 3), c(12, 12, 8)]),
    "gear": ("action", [c(12, 12, 4), c(12, 12, 9), l(12, 1, 12, 4), l(12, 20, 12, 23), l(1, 12, 4, 12), l(20, 12, 23, 12)]),
    "list": ("action", [l(9, 6, 21, 6), l(9, 12, 21, 12), l(9, 18, 21, 18), c(4, 6, 1), c(4, 12, 1), c(4, 18, 1)]),
    "grid": ("action", [r(3, 3, 7, 7, 1), r(14, 3, 7, 7, 1), r(3, 14, 7, 7, 1), r(14, 14, 7, 7, 1)]),
    # Status
    "info": ("status", [c(12, 12, 9), l(12, 11, 12, 17), c(12, 8, 0.5)]),
    "warning": ("status", [poly([(12, 3), (22, 20), (2, 20)]), l(12, 10, 12, 14), c(12, 17, 0.5)]),
    "error": ("status", [c(12, 12, 9), l(9, 9, 15, 15), l(15, 9, 9, 15)]),
    "success": ("status", [c(12, 12, 9), p("M8 12l3 3 5-6")]),
    "bell": ("status", [p("M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"), p("M10 21h4")]),
    "clock": ("status", [c(12, 12, 9), p("M12 7v5l3 2")]),
    "calendar": ("status", [r(3, 5, 18, 16, 2), l(3, 10, 21, 10), l(8, 3, 8, 7), l(16, 3, 16, 7)]),
    "hourglass": ("status", [p("M6 3h12"), p("M6 21h12"), p("M7 3c0 5 10 5 10 9s-10 4-10 9"), p("M17 3c0 5-10 5-10 9s10 4 10 9")]),
    "eye": ("status", [p("M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"), c(12, 12, 3)]),
    "eye-off": ("status", [p("M3 3l18 18"), p("M10.6 5.1A10 10 0 0 1 12 5c6 0 10 7 10 7a17 17 0 0 1-3 3.7"), p("M6.6 6.6A17 17 0 0 0 2 12s4 7 10 7a10 10 0 0 0 5.4-1.6")]),
    "shield": ("status", [p("M12 3l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V6z")]),
    "zap": ("status", [p("M13 2L4 14h7l-1 8 9-12h-7z")]),
    # Social & comms
    "chat": ("social", [p("M4 5h16v11H9l-5 4z")]),
    "mail": ("social", [r(3, 5, 18, 14, 2), p("M3 7l9 6 9-6")]),
    "user": ("social", [c(12, 8, 4), p("M4 21c0-4 4-7 8-7s8 3 8 7")]),
    "users": ("social", [c(9, 8, 3), p("M3 20c0-3 3-6 6-6s6 3 6 6"), c(17, 9, 2.5), p("M15 14c3 0 6 2 6 5")]),
    "heart": ("social", [p("M12 21s-8-5-8-11a4 4 0 0 1 8-2 4 4 0 0 1 8 2c0 6-8 11-8 11z")]),
    "star": ("social", [poly([(12, 3), (14.6, 9), (21, 9.3), (16, 13.5), (17.6, 20), (12, 16.5), (6.4, 20), (8, 13.5), (3, 9.3), (9.4, 9)])]),
    "thumbs-up": ("social", [p("M7 11v9H4v-9z"), p("M7 11l4-8a2 2 0 0 1 2 2v4h6a2 2 0 0 1 2 2l-2 8a2 2 0 0 1-2 2H7")]),
    "flag-alt": ("social", [l(5, 21, 5, 3), p("M5 4c4-2 6 2 10 0v9c-4 2-6-2-10 0")]),
    # Economy & rewards
    "coin": ("economy", [c(12, 12, 9), c(12, 12, 4)]),
    "cart": ("economy", [p("M3 4h3l2 11h11l2-8H7"), c(9, 19, 1.5), c(17, 19, 1.5)]),
    "bag": ("economy", [r(4, 8, 16, 13, 2), p("M8 8V6a4 4 0 0 1 8 0v2")]),
    "gift": ("economy", [r(3, 8, 18, 4, 1), r(5, 12, 14, 9, 1), l(12, 8, 12, 21), p("M12 8c-2-4-6-4-6-1s6 1 6 1 6 2 6-1-4-3-6 1")]),
    "gem": ("economy", [poly([(6, 4), (18, 4), (22, 9), (12, 21), (2, 9)]), l(2, 9, 22, 9)]),
    "trophy": ("economy", [p("M7 4h10v5a5 5 0 0 1-10 0z"), p("M7 6H4a3 3 0 0 0 3 4"), p("M17 6h3a3 3 0 0 1-3 4"), l(12, 14, 12, 18), r(8, 18, 8, 3, 1)]),
    "medal": ("economy", [c(12, 15, 6), p("M9 3l3 6 3-6"), l(8, 3, 16, 3)]),
    "crown": ("economy", [p("M3 18L5 7l4 5 3-7 3 7 4-5 2 11z"), l(3, 21, 21, 21)]),
    "ticket": ("economy", [p("M3 7h18v3a2 2 0 0 0 0 4v3H3v-3a2 2 0 0 0 0-4z"), l(14, 7, 14, 17)]),
    "dice": ("economy", [r(3, 3, 18, 18, 3), c(8, 8, 1), c(16, 16, 1), c(12, 12, 1)]),
    "chart": ("economy", [l(3, 21, 21, 21), r(5, 12, 3, 8), r(10.5, 8, 3, 12), r(16, 4, 3, 16)]),
    # Gameplay
    "sword": ("game", [l(14, 4, 20, 10), l(4, 20, 14, 10), l(6, 17, 9, 14), l(4, 14, 10, 20)]),
    "shield-game": ("game", [p("M12 2l9 4v6c0 5-4 9-9 10-5-1-9-5-9-10V6z"), l(12, 6, 12, 18)]),
    "potion": ("game", [p("M9 3h6"), p("M10 3v4l-5 9a4 4 0 0 0 4 6h6a4 4 0 0 0 4-6l-5-9V3")]),
    "bow": ("game", [p("M5 3c8 3 8 15 0 18"), l(5, 3, 5, 21), l(5, 12, 20, 12)]),
    "wand": ("game", [l(3, 21, 14, 10), p("M14 4l1 2 2 1-2 1-1 2-1-2-2-1 2-1z"), p("M18 10l1 1")]),
    "pickaxe": ("game", [p("M4 20L14 10"), p("M3 9c3-5 9-7 14-4-3 1-6 3-8 6z")]),
    "shovel": ("game", [l(10, 14, 4, 20), p("M14 3l-4 4 3 3 4-4a2 2 0 0 0-3-3z")]),
    "paw": ("game", [c(6, 10, 2), c(10, 5, 2), c(14, 5, 2), c(18, 10, 2), p("M8 17c0-3 2-6 4-6s4 3 4 6c0 2-2 3-4 3s-4-1-4-3z")]),
    "bone": ("game", [c(5, 8, 2), c(5, 16, 2), c(19, 8, 2), c(19, 16, 2), l(6.5, 9.5, 17.5, 14.5), l(6.5, 14.5, 17.5, 9.5)]),
    "fire": ("game", [p("M12 21c-4 0-6-3-6-6 0-4 4-6 4-11 3 2 6 5 6 9 0 3-2 5-4 8z")]),
    "leaf": ("game", [p("M5 19c0-9 6-14 15-14 0 9-5 15-14 15z"), l(5, 19, 13, 11)]),
    "snowflake": ("game", [l(12, 2, 12, 22), l(3.5, 7, 20.5, 17), l(3.5, 17, 20.5, 7)]),
    "moon": ("game", [p("M20 14a8 8 0 1 1-10-10 6 6 0 0 0 10 10z")]),
    "sun": ("game", [c(12, 12, 4), l(12, 2, 12, 5), l(12, 19, 12, 22), l(2, 12, 5, 12), l(19, 12, 22, 12)]),
    "cloud": ("game", [p("M7 18h11a4 4 0 0 0 0-8 6 6 0 0 0-11 2 3 3 0 0 0 0 6z")]),
    "portal": ("game", [p("M8 4c-3 3-3 13 0 16"), p("M16 4c3 3 3 13 0 16"), c(12, 12, 3)]),
    "door": ("game", [r(6, 3, 12, 18, 1), c(15, 12, 1)]),
    # Media & device
    "play": ("media", [poly([(7, 5), (19, 12), (7, 19)])]),
    "pause": ("media", [l(8, 5, 8, 19), l(16, 5, 16, 19)]),
    "stop": ("media", [r(6, 6, 12, 12, 1)]),
    "skip-next": ("media", [poly([(5, 5), (15, 12), (5, 19)], False), l(19, 5, 19, 19)]),
    "skip-prev": ("media", [poly([(19, 5), (9, 12), (19, 19)], False), l(5, 5, 5, 19)]),
    "volume": ("media", [poly([(3, 9), (7, 9), (12, 5), (12, 19), (7, 15), (3, 15)]), p("M16 9a4 4 0 0 1 0 6")]),
    "mute": ("media", [poly([(3, 9), (7, 9), (12, 5), (12, 19), (7, 15), (3, 15)]), l(16, 9, 22, 15), l(22, 9, 16, 15)]),
    "mic": ("media", [r(9, 3, 6, 11, 3), p("M5 11a7 7 0 0 0 14 0"), l(12, 18, 12, 22)]),
    "camera": ("media", [r(3, 7, 18, 13, 2), c(12, 13, 3.5), p("M8 7l2-3h4l2 3")]),
    "image": ("media", [r(3, 4, 18, 16, 2), c(9, 9, 2), p("M4 18l5-5 4 4 2-2 5 5")]),
    "wifi": ("media", [p("M2 9a15 15 0 0 1 20 0"), p("M5 12.5a10 10 0 0 1 14 0"), p("M8.5 16a5 5 0 0 1 7 0"), c(12, 19.5, 0.5)]),
    "battery": ("media", [r(2, 7, 17, 10, 2), l(22, 10, 22, 14)]),
    "phone": ("media", [r(7, 2, 10, 20, 2), l(11, 18, 13, 18)]),
    "keyboard": ("media", [r(2, 6, 20, 12, 2), l(6, 10, 6, 10), l(10, 10, 10, 10), l(14, 10, 14, 10), l(7, 14, 17, 14)]),
    "gamepad": ("media", [p("M6 9h12a4 4 0 0 1 4 6l-1 2a2 2 0 0 1-4-1l-1-2H8l-1 2a2 2 0 0 1-4 1l-1-2a4 4 0 0 1 4-6z"), l(7, 11, 7, 13), l(6, 12, 8, 12)]),
    "headset": ("media", [p("M4 14v-2a8 8 0 0 1 16 0v2"), r(3, 14, 4, 6, 2), r(17, 14, 4, 6, 2)]),
    "cog-alt": ("media", [c(12, 12, 3), c(12, 12, 8), c(12, 12, 10.5)]),
    "wrench": ("media", [p("M14 6a4 4 0 0 0-5 5L3 18l3 3 7-6a4 4 0 0 0 5-5l-3 3-3-3z")]),
}


def svg_for(body: list[str]) -> str:
    inner = "".join(body)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        f"{inner}</svg>\n"
    )


def main() -> int:
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name in sorted(ICONS):
        category, body = ICONS[name]
        path = SVG_DIR / f"{name}.svg"
        path.write_text(svg_for(body), encoding="utf-8")
        manifest.append(
            {
                "name": name,
                "path": str(path.relative_to(ROOT)),
                "size": SIZE,
                "category": category,
                "license": "repo-authored (CC0)",
                "source": "scripts/build_icons.py",
            }
        )
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(manifest)} icons to {SVG_DIR.relative_to(ROOT)} and manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
