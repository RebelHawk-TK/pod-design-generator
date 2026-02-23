#!/usr/bin/env python3
"""CLI entry point for POD Design Generator."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.generators.text_design import TextDesignGenerator
from src.generators.pattern_design import PatternDesignGenerator
from src.generators.niche_design import NicheDesignGenerator
from src.metadata import generate_metadata, save_metadata
from src.batch import run_batch
from src.config import PRODUCTS


def parse_products(val: str | None) -> list[str]:
    """Parse comma-separated product names."""
    if not val:
        return ["tshirt"]
    names = [p.strip().lower() for p in val.split(",")]
    for n in names:
        if n not in PRODUCTS:
            print(f"Error: Unknown product '{n}'. Available: {list(PRODUCTS.keys())}")
            sys.exit(1)
    return names


def cmd_text(args):
    products = parse_products(args.products)
    gen = TextDesignGenerator(
        text=args.text,
        font_name=args.font or "anton",
        color_shortcut=args.colors,
        palette=args.palette,
        layout=args.layout or "centered",
        shadow=not args.no_shadow,
        products=products,
    )

    # Build filename from text
    filename = args.filename or args.text[:40].replace(" ", "_").replace("\n", "_").lower()
    filename = "".join(c for c in filename if c.isalnum() or c == "_")

    print(f"Generating text design: \"{args.text}\"")
    saved = gen.generate_and_save(filename)

    # Metadata
    meta = generate_metadata(text=args.text, design_type="text")
    for path in saved:
        meta_path = save_metadata(meta, path)
        print(f"  Saved: {path}")
        print(f"  Meta:  {meta_path}")

    print(f"\nDone! {len(saved)} design(s) generated.")


def cmd_pattern(args):
    products = parse_products(args.products)
    gen = PatternDesignGenerator(
        style=args.style or "geometric",
        palette=args.palette or "neon",
        seed=args.seed,
        color_shortcut=args.colors,
        products=products,
    )

    style = args.style or "geometric"
    seed_str = f"_s{args.seed}" if args.seed is not None else ""
    filename = args.filename or f"pattern_{style}{seed_str}"

    print(f"Generating pattern: {style} (palette: {args.palette or 'neon'})")
    saved = gen.generate_and_save(filename)

    meta = generate_metadata(
        text=f"{style} pattern", design_type="pattern", style=style,
    )
    for path in saved:
        meta_path = save_metadata(meta, path)
        print(f"  Saved: {path}")
        print(f"  Meta:  {meta_path}")

    print(f"\nDone! {len(saved)} design(s) generated.")


def cmd_niche(args):
    products = parse_products(args.products)
    gen = NicheDesignGenerator(
        theme=args.theme,
        text=args.text,
        products=products,
    )

    text_for_meta = args.text or args.theme
    filename = args.filename or f"niche_{args.theme}"
    if args.text:
        slug = args.text[:30].replace(" ", "_").replace("\n", "_").lower()
        slug = "".join(c for c in slug if c.isalnum() or c == "_")
        filename = args.filename or f"niche_{args.theme}_{slug}"

    print(f"Generating niche design: theme={args.theme}")
    saved = gen.generate_and_save(filename)

    meta = generate_metadata(
        text=text_for_meta, design_type="niche", theme=args.theme,
        extra_tags=gen.template.get("tags", []),
    )
    for path in saved:
        meta_path = save_metadata(meta, path)
        print(f"  Saved: {path}")
        print(f"  Meta:  {meta_path}")

    print(f"\nDone! {len(saved)} design(s) generated.")


def cmd_batch(args):
    print(f"Running batch from: {args.config}")
    paths = run_batch(args.config)
    images = [p for p in paths if p.suffix == ".png"]
    metas = [p for p in paths if p.suffix == ".json"]
    print(f"\nDone! {len(images)} image(s) and {len(metas)} metadata file(s) generated.")


def main():
    parser = argparse.ArgumentParser(
        description="POD Design Generator — create print-on-demand designs for Redbubble",
    )
    subparsers = parser.add_subparsers(dest="command", help="Design type")

    # ---- text ----
    p_text = subparsers.add_parser("text", help="Text/quote design")
    p_text.add_argument("text", help="Text or quote to render (use \\n for line breaks)")
    p_text.add_argument("--font", "-f", help="Font name (e.g., anton, pacifico, bebas)")
    p_text.add_argument("--colors", "-c", help="Color shortcut (e.g., white-on-black, neon-on-dark)")
    p_text.add_argument("--palette", help="Color palette name")
    p_text.add_argument("--layout", "-l", choices=["centered", "stacked", "arced"], default="centered")
    p_text.add_argument("--products", "-p", help="Comma-separated products (tshirt,sticker,poster)")
    p_text.add_argument("--no-shadow", action="store_true", help="Disable drop shadow")
    p_text.add_argument("--filename", help="Output filename (without extension)")
    p_text.set_defaults(func=cmd_text)

    # ---- pattern ----
    p_pattern = subparsers.add_parser("pattern", help="Geometric/abstract pattern")
    p_pattern.add_argument("--style", "-s", choices=["geometric", "circles", "triangles", "grid", "tessellation"], default="geometric")
    p_pattern.add_argument("--palette", default="neon", help="Color palette (warm/cool/neon/pastel/earth)")
    p_pattern.add_argument("--seed", type=int, help="Random seed for reproducibility")
    p_pattern.add_argument("--colors", "-c", help="Color shortcut for background")
    p_pattern.add_argument("--products", "-p", help="Comma-separated products")
    p_pattern.add_argument("--filename", help="Output filename (without extension)")
    p_pattern.set_defaults(func=cmd_pattern)

    # ---- niche ----
    p_niche = subparsers.add_parser("niche", help="Themed template design")
    p_niche.add_argument("--theme", "-t", required=True, help="Theme name (motivational, funny, profession, hobby)")
    p_niche.add_argument("--text", help="Custom text (otherwise random from theme)")
    p_niche.add_argument("--products", "-p", help="Comma-separated products")
    p_niche.add_argument("--filename", help="Output filename (without extension)")
    p_niche.set_defaults(func=cmd_niche)

    # ---- batch ----
    p_batch = subparsers.add_parser("batch", help="Batch generate from JSON config")
    p_batch.add_argument("--config", "-c", required=True, help="Path to batch config JSON")
    p_batch.set_defaults(func=cmd_batch)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Process escaped newlines in text args
    if hasattr(args, "text") and args.text:
        args.text = args.text.replace("\\n", "\n")

    args.func(args)


if __name__ == "__main__":
    main()
