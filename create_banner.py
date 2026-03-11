#!/usr/bin/env python3
"""Create a Redbubble shop banner from landmark style-transfer images.

Redbubble banner: 2400x600 pixels.
Layout: 6 landmark images in a panoramic strip with gradient overlays
and shop name text.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

LANDMARK_DIR = Path.home() / "Documents" / "Claude" / "landmark-style-transfer-unified" / "output" / "poster"
OUTPUT = Path(__file__).parent / "redbubble_banner.png"

# Banner dimensions
W, H = 2400, 600

# Curated selection — diverse landmarks x diverse styles for visual variety
PANELS = [
    "eiffel_tower_starry_night_poster.png",      # Van Gogh blues/yellows
    "pyramids_giza_the_scream_poster.png",        # Munch oranges/reds
    "mount_fuji_great_wave_poster.png",           # Hokusai blues/whites
    "taj_mahal_water_lilies_poster.png",          # Monet greens/pastels
    "colosseum_starry_night_poster.png",          # Van Gogh swirls
    "golden_gate_great_wave_poster.png",          # Hokusai dramatic
]

SHOP_NAME = "ModernDesignCo"
TAGLINE = "Famous Landmarks Reimagined in Classic Art Styles"


def create_banner():
    banner = Image.new("RGB", (W, H), (20, 20, 30))
    draw = ImageDraw.Draw(banner)

    panel_w = W // len(PANELS)

    # Place each panel image
    for i, filename in enumerate(PANELS):
        img_path = LANDMARK_DIR / filename
        if not img_path.exists():
            print(f"  Warning: {filename} not found, skipping")
            continue

        with Image.open(img_path) as img:
            img = img.convert("RGB")

            # Crop to a vertical strip from center (portrait crop for banner height)
            src_w, src_h = img.size
            # We want a strip that's panel_w/H aspect ratio from the source
            target_ratio = panel_w / H
            src_ratio = src_w / src_h

            if src_ratio > target_ratio:
                # Source is wider — crop width
                new_w = int(src_h * target_ratio)
                left = (src_w - new_w) // 2
                img = img.crop((left, 0, left + new_w, src_h))
            else:
                # Source is taller — crop height
                new_h = int(src_w / target_ratio)
                top = (src_h - new_h) // 2
                img = img.crop((0, top, src_w, top + new_h))

            img = img.resize((panel_w, H), Image.LANCZOS)

            # Apply subtle edge blend — darken left/right edges of each panel
            overlay = Image.new("RGBA", (panel_w, H), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            blend_w = panel_w // 6
            for x in range(blend_w):
                alpha = int(80 * (1 - x / blend_w))
                overlay_draw.line([(x, 0), (x, H)], fill=(0, 0, 0, alpha))
                overlay_draw.line([(panel_w - 1 - x, 0), (panel_w - 1 - x, H)], fill=(0, 0, 0, alpha))

            img = img.convert("RGBA")
            img = Image.alpha_composite(img, overlay)
            banner.paste(img.convert("RGB"), (i * panel_w, 0))

    # Add a dark gradient overlay at the bottom for text readability
    gradient = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(gradient)
    for y in range(H // 2, H):
        progress = (y - H // 2) / (H // 2)
        alpha = int(180 * progress)
        grad_draw.line([(0, y), (W, y)], fill=(10, 10, 20, alpha))

    # Also add a subtle top gradient
    for y in range(H // 4):
        progress = 1 - y / (H // 4)
        alpha = int(100 * progress)
        grad_draw.line([(0, y), (W, y)], fill=(10, 10, 20, alpha))

    banner = banner.convert("RGBA")
    banner = Image.alpha_composite(banner, gradient)
    banner = banner.convert("RGB")

    # Add text
    draw = ImageDraw.Draw(banner)

    # Try to load a nice font, fall back to default
    title_size = 52
    tagline_size = 22
    try:
        # macOS system fonts
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", title_size)
        tagline_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", tagline_size)
    except Exception:
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/SFNSDisplay.ttf", title_size)
            tagline_font = ImageFont.truetype("/System/Library/Fonts/SFNSDisplay.ttf", tagline_size)
        except Exception:
            title_font = ImageFont.load_default()
            tagline_font = ImageFont.load_default()

    # Draw shop name — centered, near bottom
    title_bbox = draw.textbbox((0, 0), SHOP_NAME, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    title_x = (W - title_w) // 2
    title_y = H - 140

    # Text shadow
    draw.text((title_x + 2, title_y + 2), SHOP_NAME, fill=(0, 0, 0), font=title_font)
    draw.text((title_x, title_y), SHOP_NAME, fill=(255, 255, 255), font=title_font)

    # Draw tagline
    tag_bbox = draw.textbbox((0, 0), TAGLINE, font=tagline_font)
    tag_w = tag_bbox[2] - tag_bbox[0]
    tag_x = (W - tag_w) // 2
    tag_y = title_y + title_size + 15

    draw.text((tag_x + 1, tag_y + 1), TAGLINE, fill=(0, 0, 0), font=tagline_font)
    draw.text((tag_x, tag_y), TAGLINE, fill=(220, 220, 230), font=tagline_font)

    # Add subtle decorative line above text
    line_w = 300
    line_x = (W - line_w) // 2
    line_y = title_y - 20
    draw.line([(line_x, line_y), (line_x + line_w, line_y)], fill=(200, 200, 210, 150), width=1)

    banner.save(OUTPUT, "PNG", quality=95)
    print(f"Banner saved: {OUTPUT}")
    print(f"  Size: {W}x{H}")
    print(f"  Panels: {len(PANELS)} landmark images")


if __name__ == "__main__":
    create_banner()
