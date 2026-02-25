#!/usr/bin/env python3
"""Generate product mockup images for Pinterest pins.

Composites existing POD designs onto t-shirt and poster mockup templates.
Output at Pinterest-optimal 1000x1500 (2:3) resolution.

Usage:
    python3 generate_mockups.py --folder tshirt --limit 5     # Test a few
    python3 generate_mockups.py --folder tshirt --dry-run      # Preview count
    python3 generate_mockups.py --folder tshirt                # All t-shirts
    python3 generate_mockups.py --folder poster                # All posters
    python3 generate_mockups.py --folder tshirt --shirt-color black
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).parent / "output"
MOCKUP_DIR = Path(__file__).parent / "output" / "mockups"
FONTS_DIR = Path(__file__).parent / "fonts"

# Pinterest optimal pin size
PIN_WIDTH = 1000
PIN_HEIGHT = 1500

# T-shirt mockup layout
SHIRT_COLORS = {
    "black": (30, 30, 30),
    "white": (245, 245, 245),
    "navy": (25, 35, 65),
    "gray": (130, 130, 130),
    "heather": (180, 180, 175),
}
DEFAULT_SHIRT_COLOR = "black"

# Background colors (clean, Pinterest-friendly)
BG_COLORS = {
    "black": (245, 243, 240),      # warm off-white for dark shirts
    "white": (55, 55, 60),          # dark charcoal for white shirts
    "navy": (235, 235, 230),        # light warm gray
    "gray": (245, 243, 240),        # warm off-white
    "heather": (250, 248, 245),     # near-white
}

# Poster mockup layout
WALL_COLOR = (235, 228, 218)        # warm beige wall
FRAME_COLOR = (45, 40, 35)          # dark wood frame
FRAME_WIDTH = 8
SHADOW_OFFSET = 6
SHADOW_BLUR = 12


# ---------------------------------------------------------------------------
# T-shirt shape (polygon coordinates for 1000x1500 canvas)
# ---------------------------------------------------------------------------

def _tshirt_polygon() -> list[tuple[int, int]]:
    """Return polygon points for a front-view t-shirt silhouette."""
    # Designed for a 1000x1500 canvas, natural proportions
    return [
        # Collar left
        (420, 130),
        # Left shoulder
        (360, 125), (240, 148),
        # Left sleeve top
        (90, 245),
        # Left sleeve bottom
        (130, 400),
        # Left armpit
        (260, 320),
        # Left side (natural taper)
        (255, 850), (265, 860),
        # Bottom hem (slight curve)
        (350, 870), (500, 875), (650, 870),
        # Right side
        (735, 860), (745, 850),
        (740, 320),
        # Right armpit
        (870, 400),
        # Right sleeve top
        (910, 245),
        # Right shoulder
        (760, 148), (640, 125),
        # Collar right
        (580, 130),
    ]


def _draw_collar(draw: ImageDraw.Draw, color: tuple) -> None:
    """Draw a simple crew neck collar."""
    r, g, b = color
    collar_color = (max(0, r - 25), max(0, g - 25), max(0, b - 25))
    draw.arc([410, 115, 590, 170], start=0, end=180, fill=collar_color, width=6)


def _draw_shirt_details(draw: ImageDraw.Draw, color: tuple) -> None:
    """Add subtle seam lines for realism."""
    r, g, b = color
    seam_color = (max(0, r - 15), max(0, g - 15), max(0, b - 15), 60)

    # Shoulder seams
    draw.line([(240, 148), (420, 130)], fill=seam_color, width=1)
    draw.line([(580, 130), (760, 148)], fill=seam_color, width=1)


# ---------------------------------------------------------------------------
# Mockup generators
# ---------------------------------------------------------------------------

def generate_tshirt_mockup(
    design_path: Path,
    title: str,
    shirt_color_name: str = DEFAULT_SHIRT_COLOR,
) -> Image.Image:
    """Generate a t-shirt mockup with the design on it."""
    shirt_rgb = SHIRT_COLORS.get(shirt_color_name, SHIRT_COLORS[DEFAULT_SHIRT_COLOR])
    bg_rgb = BG_COLORS.get(shirt_color_name, BG_COLORS[DEFAULT_SHIRT_COLOR])

    # Create canvas
    canvas = Image.new("RGB", (PIN_WIDTH, PIN_HEIGHT), bg_rgb)
    draw = ImageDraw.Draw(canvas)

    # Draw t-shirt shape
    shirt_layer = Image.new("RGBA", (PIN_WIDTH, PIN_HEIGHT), (0, 0, 0, 0))
    shirt_draw = ImageDraw.Draw(shirt_layer)
    shirt_draw.polygon(_tshirt_polygon(), fill=(*shirt_rgb, 255))
    _draw_collar(shirt_draw, shirt_rgb)
    _draw_shirt_details(shirt_draw, shirt_rgb)

    # Add shirt shadow
    shadow = Image.new("RGBA", (PIN_WIDTH, PIN_HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.polygon(_tshirt_polygon(), fill=(0, 0, 0, 50))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
    # Offset shadow slightly down
    shadow_shifted = Image.new("RGBA", (PIN_WIDTH, PIN_HEIGHT), (0, 0, 0, 0))
    shadow_shifted.paste(shadow, (4, 8))

    canvas.paste(Image.alpha_composite(
        Image.new("RGBA", (PIN_WIDTH, PIN_HEIGHT), (*bg_rgb, 255)),
        shadow_shifted,
    ).convert("RGB"))

    # Paste shirt on canvas
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shirt_layer).convert("RGB")

    # Load design and crop to content (remove transparent padding)
    design = Image.open(design_path).convert("RGBA")
    bbox = design.getbbox()
    if bbox:
        design = design.crop(bbox)

    # Print area: chest region of the shirt
    print_w, print_h = 400, 420
    print_x, print_y = 500 - print_w // 2, 280

    # Scale design to fit print area while maintaining aspect ratio
    dw, dh = design.size
    scale = min(print_w / dw, print_h / dh)
    new_w = int(dw * scale)
    new_h = int(dh * scale)
    design_resized = design.resize((new_w, new_h), Image.LANCZOS)

    # Center design in print area
    paste_x = print_x + (print_w - new_w) // 2
    paste_y = print_y + (print_h - new_h) // 2

    # Paste design onto shirt (using alpha mask)
    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.paste(design_resized, (paste_x, paste_y), design_resized)
    canvas = canvas_rgba.convert("RGB")

    # Add title text at bottom
    canvas = _add_title_bar(canvas, title, bg_rgb, shirt_color_name)

    return canvas


def generate_poster_mockup(design_path: Path, title: str) -> Image.Image:
    """Generate a framed poster mockup on a wall."""
    canvas = Image.new("RGB", (PIN_WIDTH, PIN_HEIGHT), WALL_COLOR)

    # Load design
    design = Image.open(design_path).convert("RGB")

    # Poster area: centered, with margins for frame and wall
    poster_max_w = 700
    poster_max_h = 900

    dw, dh = design.size
    scale = min(poster_max_w / dw, poster_max_h / dh)
    poster_w = int(dw * scale)
    poster_h = int(dh * scale)
    design_resized = design.resize((poster_w, poster_h), Image.LANCZOS)

    # Frame dimensions
    frame_w = poster_w + FRAME_WIDTH * 2
    frame_h = poster_h + FRAME_WIDTH * 2

    # Center position (slightly above center for visual balance)
    frame_x = (PIN_WIDTH - frame_w) // 2
    frame_y = (PIN_HEIGHT - frame_h) // 2 - 80

    # Draw frame shadow
    shadow = Image.new("RGBA", (PIN_WIDTH, PIN_HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle(
        [frame_x + SHADOW_OFFSET, frame_y + SHADOW_OFFSET,
         frame_x + frame_w + SHADOW_OFFSET, frame_y + frame_h + SHADOW_OFFSET],
        fill=(0, 0, 0, 40),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=SHADOW_BLUR))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow).convert("RGB")

    # Draw frame
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(
        [frame_x, frame_y, frame_x + frame_w, frame_y + frame_h],
        fill=FRAME_COLOR,
    )

    # Paste design inside frame
    canvas.paste(design_resized, (frame_x + FRAME_WIDTH, frame_y + FRAME_WIDTH))

    # Add title text at bottom
    canvas = _add_title_bar(canvas, title, WALL_COLOR, "poster")

    return canvas


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _add_title_bar(
    canvas: Image.Image,
    title: str,
    bg_rgb: tuple,
    style: str,
) -> Image.Image:
    """Add a title bar at the bottom of the mockup."""
    draw = ImageDraw.Draw(canvas)

    # Title area
    bar_y = PIN_HEIGHT - 180
    bar_height = 180

    # Semi-transparent overlay
    overlay = Image.new("RGBA", (PIN_WIDTH, bar_height), (255, 255, 255, 220))
    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.paste(overlay, (0, bar_y), overlay)
    canvas = canvas_rgba.convert("RGB")
    draw = ImageDraw.Draw(canvas)

    # Load font
    font_path = FONTS_DIR / "BebasNeue-Regular.ttf"
    if not font_path.exists():
        font_path = FONTS_DIR / "Anton-Regular.ttf"

    # Title text
    try:
        title_font = ImageFont.truetype(str(font_path), 36)
    except Exception:
        title_font = ImageFont.load_default()

    # Truncate title if too long
    display_title = title if len(title) <= 45 else title[:42] + "..."

    # Center title
    bbox = draw.textbbox((0, 0), display_title, font=title_font)
    text_w = bbox[2] - bbox[0]
    text_x = (PIN_WIDTH - text_w) // 2
    text_y = bar_y + 30

    draw.text((text_x, text_y), display_title, fill=(40, 40, 40), font=title_font)

    # Subtitle
    subtitle = "Available on T-Shirts, Hoodies, Mugs & More"
    try:
        sub_font = ImageFont.truetype(str(FONTS_DIR / "PatrickHand-Regular.ttf"), 24)
    except Exception:
        sub_font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
    sub_w = bbox[2] - bbox[0]
    sub_x = (PIN_WIDTH - sub_w) // 2
    sub_y = text_y + 55

    draw.text((sub_x, sub_y), subtitle, fill=(100, 100, 100), font=sub_font)

    # Shop name
    shop = "Modern Design Concept"
    try:
        shop_font = ImageFont.truetype(str(font_path), 20)
    except Exception:
        shop_font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), shop, font=shop_font)
    shop_w = bbox[2] - bbox[0]
    shop_x = (PIN_WIDTH - shop_w) // 2
    shop_y = sub_y + 42

    draw.text((shop_x, shop_y), shop, fill=(140, 140, 140), font=shop_font)

    return canvas


# ---------------------------------------------------------------------------
# Batch processing
# ---------------------------------------------------------------------------

def process_designs(
    folder: str,
    limit: int | None,
    dry_run: bool,
    shirt_color: str,
) -> None:
    """Process all designs in a folder and generate mockups."""
    folder_path = OUTPUT_DIR / folder
    if not folder_path.is_dir():
        print(f"Error: folder not found: {folder_path}")
        return

    # Collect designs with metadata
    designs = []
    for png in sorted(folder_path.glob("*.png")):
        meta_path = png.with_suffix(".json")
        if not meta_path.exists():
            continue
        with open(meta_path) as f:
            metadata = json.load(f)
        designs.append((png, metadata))

    if not designs:
        print(f"No designs found in {folder_path}")
        return

    if limit:
        designs = designs[:limit]

    # Create output directory
    mockup_subdir = MOCKUP_DIR / folder
    if not dry_run:
        mockup_subdir.mkdir(parents=True, exist_ok=True)

    print(f"{'[DRY RUN] ' if dry_run else ''}Generating {len(designs)} mockups for {folder}/")
    print(f"  Output: {mockup_subdir}")
    if folder == "tshirt":
        print(f"  Shirt color: {shirt_color}")
    print()

    if dry_run:
        for i, (png, meta) in enumerate(designs[:5], 1):
            print(f"  [{i}] {png.stem} — {meta['title']}")
        if len(designs) > 5:
            print(f"  ... and {len(designs) - 5} more")
        print(f"\nRun without --dry-run to generate mockups.")
        return

    generated = 0
    skipped = 0
    for i, (png, meta) in enumerate(designs, 1):
        title = meta["title"]
        out_path = mockup_subdir / f"{png.stem}_mockup.png"

        if out_path.exists():
            generated += 1
            if i % 50 == 0 or i == len(designs):
                print(f"  [{i}/{len(designs)}] generated")
            continue

        try:
            if folder in ("tshirt", "sticker"):
                mockup = generate_tshirt_mockup(png, title, shirt_color)
            else:
                mockup = generate_poster_mockup(png, title)

            mockup.save(str(out_path), "PNG", optimize=True)
            generated += 1
        except Exception as exc:
            skipped += 1
            print(f"  SKIP {png.name}: {exc}")

        if i % 50 == 0 or i == len(designs):
            print(f"  [{i}/{len(designs)}] generated")

    print(f"\nDone! {generated} mockups saved to {mockup_subdir}/")
    if skipped:
        print(f"  ({skipped} skipped due to errors)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate product mockup images for Pinterest pins",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python3 generate_mockups.py --folder tshirt --limit 5
  python3 generate_mockups.py --folder tshirt --shirt-color navy
  python3 generate_mockups.py --folder poster
  python3 generate_mockups.py --folder tshirt --dry-run
""",
    )
    parser.add_argument("--folder", required=True, help="Design folder (tshirt, sticker, poster)")
    parser.add_argument("--limit", type=int, help="Max mockups to generate")
    parser.add_argument("--dry-run", action="store_true", help="Preview without generating")
    parser.add_argument(
        "--shirt-color",
        choices=list(SHIRT_COLORS.keys()),
        default=DEFAULT_SHIRT_COLOR,
        help=f"T-shirt color (default: {DEFAULT_SHIRT_COLOR})",
    )
    args = parser.parse_args()

    process_designs(args.folder, args.limit, args.dry_run, args.shirt_color)


if __name__ == "__main__":
    main()
