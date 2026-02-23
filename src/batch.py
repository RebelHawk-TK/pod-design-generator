"""Batch processing — reads JSON config and generates all designs."""

from __future__ import annotations

import json
from pathlib import Path

from src.generators.text_design import TextDesignGenerator
from src.generators.pattern_design import PatternDesignGenerator
from src.generators.niche_design import NicheDesignGenerator
from src.metadata import generate_metadata, save_metadata
from src.canvas import save_design


def run_batch(config_path: str | Path) -> list[Path]:
    """
    Read a batch config JSON and generate all designs.
    Returns list of all saved file paths (images + metadata).
    """
    config_path = Path(config_path)
    with open(config_path) as f:
        config = json.load(f)

    designs = config.get("designs", [])
    all_paths: list[Path] = []

    for i, entry in enumerate(designs):
        design_type = entry.get("type", "text")
        products = entry.get("products", ["tshirt"])
        filename = entry.get("filename", f"batch_{i:03d}")
        text = entry.get("text", "Design")

        print(f"  [{i+1}/{len(designs)}] Generating {design_type}: {filename}")

        if design_type == "text":
            gen = TextDesignGenerator(
                text=text,
                font_name=entry.get("font", "anton"),
                color_shortcut=entry.get("colors"),
                palette=entry.get("palette"),
                layout=entry.get("layout", "centered"),
                shadow=entry.get("shadow", True),
                products=products,
            )
        elif design_type == "pattern":
            gen = PatternDesignGenerator(
                style=entry.get("style", "geometric"),
                palette=entry.get("palette", "neon"),
                seed=entry.get("seed"),
                color_shortcut=entry.get("colors"),
                products=products,
            )
        elif design_type == "niche":
            gen = NicheDesignGenerator(
                theme=entry.get("theme", "motivational"),
                text=entry.get("text"),
                products=products,
            )
        else:
            print(f"    [skip] Unknown type: {design_type}")
            continue

        saved = gen.generate_and_save(filename)
        all_paths.extend(saved)

        # Generate and save metadata
        meta = generate_metadata(
            text=text,
            design_type=design_type,
            theme=entry.get("theme"),
            style=entry.get("style"),
            extra_tags=entry.get("tags"),
        )
        for path in saved:
            meta_path = save_metadata(meta, path)
            all_paths.append(meta_path)

    return all_paths
