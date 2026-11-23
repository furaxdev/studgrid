#!/usr/bin/env python3
"""Scrape real UI screenshots from the DevForum thread "Show off your UI designs"
and sample a 6-colour palette per image with PIL median-cut quantisation.

Output: docs/refs/catalog.json (deterministic order, no timestamps).
Images are cached under scripts/.cache/refs/ (git-ignored) so the catalog can be
regenerated offline once the cache exists.

Usage:  python scripts/collect_ui_refs.py [--max-images N] [--offline]
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "scripts" / ".cache" / "refs"
OUT = ROOT / "docs" / "refs" / "catalog.json"

THREAD_ID = 311776
THREAD_SLUG = "show-off-your-ui-designs"
THREAD_URL = f"https://devforum.roblox.com/t/{THREAD_SLUG}/{THREAD_ID}"
THREAD_JSON = f"https://devforum.roblox.com/t/{THREAD_ID}.json"
POSTS_JSON = f"https://devforum.roblox.com/t/{THREAD_ID}/posts.json"
UA = "studgrid-ui-refs/1.0 (research; contact via repository owner)"
MIN_SIDE = 300  # px; skip emoji, avatars and thumbnails
PALETTE_COLORS = 6
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif")


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def fetch_thread_posts() -> list[dict]:
    head = json.loads(fetch(THREAD_JSON))
    stream = head["post_stream"]["stream"]
    posts: dict[int, dict] = {p["id"]: p for p in head["post_stream"]["posts"]}
    missing = [i for i in stream if i not in posts]
    for start in range(0, len(missing), 20):
        chunk = missing[start : start + 20]
        qs = urllib.parse.urlencode([("post_ids[]", i) for i in chunk])
        data = json.loads(fetch(f"{POSTS_JSON}?{qs}"))
        for p in data["post_stream"]["posts"]:
            posts[p["id"]] = p
    return [posts[i] for i in stream if i in posts]


def normalise_url(src: str) -> str:
    src = html.unescape(src)
    if src.startswith("//"):
        src = "https:" + src
    elif src.startswith("/"):
        src = urllib.parse.urljoin("https://devforum.roblox.com", src)
    return src


def candidate_images(post: dict) -> list[str]:
    cooked = post.get("cooked", "")
    urls: list[str] = []
    for m in re.finditer(r'<img[^>]+src="([^"]+)"', cooked):
        src = normalise_url(m.group(1))
        if "/user_avatar/" in src or "/emoji/" in src or "/images/emoji" in src:
            continue
        urls.append(src)
    for m in re.finditer(r'href="([^"]+)"', cooked):
        href = normalise_url(m.group(1))
        if href.lower().split("?")[0].endswith(IMG_EXT):
            urls.append(href)
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def cached_path(url: str) -> Path:
    ext = Path(urllib.parse.urlparse(url).path).suffix.lower() or ".img"
    digest = hashlib.sha256(url.encode()).hexdigest()[:16]
    return CACHE / f"{digest}{ext}"


def ensure_download(url: str, offline: bool) -> Path | None:
    path = cached_path(url)
    if path.exists():
        return path
    if offline:
        return None
    CACHE.mkdir(parents=True, exist_ok=True)
    try:
        path.write_bytes(fetch(url))
    except Exception as exc:  # network or 404: drop the image, never invent it
        print(f"skip {url}: {exc}", file=sys.stderr)
        return None
    return path


def sample_palette(path: Path) -> tuple[int, int, list[dict]] | None:
    with Image.open(path) as im:
        im = im.convert("RGB")
        w, h = im.size
        if min(w, h) < MIN_SIDE:
            return None
        # Quantise on a downscaled copy so sampling is fast and deterministic.
        thumb = im.copy()
        thumb.thumbnail((320, 320), Image.Resampling.NEAREST)
        q = thumb.quantize(colors=PALETTE_COLORS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        pal = q.getpalette()[: PALETTE_COLORS * 3]
        counts = Counter(q.getdata())
        total = sum(counts.values())
        colours = []
        for idx, n in counts.most_common():
            r, g, b = pal[idx * 3 : idx * 3 + 3]
            colours.append({"hex": f"#{r:02X}{g:02X}{b:02X}", "share": round(n / total, 4)})
        return w, h, colours


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-images", type=int, default=0, help="0 = all")
    ap.add_argument("--offline", action="store_true", help="use cache only")
    args = ap.parse_args()

    posts = [] if args.offline else fetch_thread_posts()
    entries: list[dict] = []
    for post in posts:
        for url in candidate_images(post):
            path = ensure_download(url, args.offline)
            if path is None:
                continue
            sampled = sample_palette(path)
            if sampled is None:
                continue
            w, h, colours = sampled
            entries.append(
                {
                    "post_id": post["id"],
                    "post_url": f"{THREAD_URL}/{post['post_number']}",
                    "author": post.get("username"),
                    "image_url": url,
                    "width": w,
                    "height": h,
                    "palette": colours,
                }
            )
            if args.max_images and len(entries) >= args.max_images:
                break
        if args.max_images and len(entries) >= args.max_images:
            break

    if args.offline and not entries:
        print("offline run with empty cache: nothing to write", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "source_thread": THREAD_URL,
        "method": f"PIL MEDIANCUT quantize to {PALETTE_COLORS} colours on <=320px thumbnail",
        "min_side_px": MIN_SIDE,
        "count": len(entries),
        "entries": entries,
    }
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} with {len(entries)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
