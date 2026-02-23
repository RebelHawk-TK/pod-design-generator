"""Centered text layout with auto-sizing."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

from src.effects.shadow import draw_text_with_shadow


def _fit_font_size(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_loader,
    max_width: int,
    max_height: int,
    start_size: int = 400,
    min_size: int = 40,
) -> tuple[ImageFont.FreeTypeFont, int]:
    """Binary search for the largest font size that fits within bounds."""
    lo, hi = min_size, start_size
    best_size = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        font = font_loader(mid)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        if tw <= max_width and th <= max_height:
            best_size = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return font_loader(best_size), best_size


def render_centered(
    img: Image.Image,
    text: str,
    font_loader,
    fg_color: str | tuple,
    safe_zone: tuple[int, int, int, int],
    shadow: bool = True,
    max_font_size: int = 400,
) -> None:
    """Render text centered within the safe zone, auto-sized to fit."""
    draw = ImageDraw.Draw(img)
    sz = safe_zone
    max_w = sz[2] - sz[0]
    max_h = sz[3] - sz[1]

    font, _ = _fit_font_size(draw, text, font_loader, max_w, max_h, start_size=max_font_size)

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = sz[0] + (max_w - tw) // 2 - bbox[0]
    y = sz[1] + (max_h - th) // 2 - bbox[1]

    if shadow:
        draw_text_with_shadow(img, (x, y), text, font, fg_color)
    else:
        draw.text((x, y), text, font=font, fill=fg_color)
