#!/usr/bin/env python3
"""Generate all designs from all templates for all products."""

from __future__ import annotations

import json
import time
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.generators.niche_design import NicheDesignGenerator
from src.metadata import generate_metadata, save_metadata
from src.canvas import save_design
from src.config import TEMPLATES_DIR, PRODUCTS

PRODUCTS_LIST = ["tshirt", "sticker", "poster"]


def slugify(text: str, max_len: int = 50) -> str:
    slug = text[:max_len].replace("\n", "_").replace(" ", "_").lower()
    return "".join(c for c in slug if c.isalnum() or c == "_").strip("_")


def main():
    templates = sorted(TEMPLATES_DIR.glob("*.json"))
    total_phrases = 0
    for t in templates:
        with open(t) as f:
            data = json.load(f)
        total_phrases += len(data.get("phrases", []))

    total_images = total_phrases * len(PRODUCTS_LIST)
    print(f"Found {len(templates)} templates, {total_phrases} phrases")
    print(f"Generating {total_images} images ({total_phrases} designs x {len(PRODUCTS_LIST)} products)\n")

    start = time.time()
    image_count = 0
    design_count = 0

    for tmpl_path in templates:
        theme = tmpl_path.stem
        with open(tmpl_path) as f:
            data = json.load(f)

        phrases = data.get("phrases", [])
        print(f"--- {theme} ({len(phrases)} phrases) ---")

        for i, phrase in enumerate(phrases):
            slug = slugify(phrase)
            filename = f"{theme}_{i:03d}_{slug}"

            gen = NicheDesignGenerator(
                theme=theme,
                text=phrase,
                products=PRODUCTS_LIST,
            )

            saved = gen.generate_and_save(filename)
            image_count += len(saved)
            design_count += 1

            # Save metadata alongside each image
            meta = generate_metadata(
                text=phrase,
                design_type="niche",
                theme=theme,
                extra_tags=data.get("tags", []),
            )
            for path in saved:
                save_metadata(meta, path)

            elapsed = time.time() - start
            rate = design_count / elapsed if elapsed > 0 else 0
            eta = (total_phrases - design_count) / rate if rate > 0 else 0
            print(f"  [{design_count}/{total_phrases}] {filename} ({len(saved)} images) "
                  f"[{elapsed:.0f}s elapsed, ~{eta:.0f}s remaining]")

    elapsed = time.time() - start
    print(f"\nDone! {image_count} images + {image_count} metadata files generated in {elapsed:.0f}s")


if __name__ == "__main__":
    main()
