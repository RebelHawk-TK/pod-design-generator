#!/usr/bin/env python3
"""Download free Google Fonts for POD design generation."""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

FONTS_DIR = Path(__file__).resolve().parent / "fonts"

# Google Fonts GitHub raw URLs (ofl-licensed, free for commercial use)
BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl"

FONT_URLS: dict[str, str] = {
    "RussoOne-Regular.ttf": f"{BASE}/russoone/RussoOne-Regular.ttf",
    "Anton-Regular.ttf": f"{BASE}/anton/Anton-Regular.ttf",
    "BebasNeue-Regular.ttf": f"{BASE}/bebasneue/BebasNeue-Regular.ttf",
    "Pacifico-Regular.ttf": f"{BASE}/pacifico/Pacifico-Regular.ttf",
    "Caveat-VariableFont_wght.ttf": f"{BASE}/caveat/Caveat%5Bwght%5D.ttf",
    "ShadowsIntoLight-Regular.ttf": f"{BASE}/shadowsintolight/ShadowsIntoLight.ttf",
    "PatrickHand-Regular.ttf": f"{BASE}/patrickhand/PatrickHand-Regular.ttf",
}


def download_fonts() -> None:
    FONTS_DIR.mkdir(exist_ok=True)
    success = 0
    for filename, url in FONT_URLS.items():
        dest = FONTS_DIR / filename
        if dest.exists():
            print(f"  [skip] {filename} (already exists)")
            success += 1
            continue
        print(f"  [download] {filename} ... ", end="", flush=True)
        try:
            urllib.request.urlretrieve(url, dest)
            print("OK")
            success += 1
        except Exception as e:
            print(f"FAILED: {e}")

    print(f"\n{success}/{len(FONT_URLS)} fonts ready in {FONTS_DIR}")
    if success < len(FONT_URLS):
        print("Some fonts failed. Re-run this script to retry.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    print("Setting up fonts for POD Design Generator...\n")
    download_fonts()
    print("\nDone!")
