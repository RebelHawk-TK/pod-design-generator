"""Stacked multi-line text layout."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

from src.effects.shadow import draw_text_with_shadow


def _fit_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    font_loader,
    max_width: int,
    max_height: int,
    line_spacing: float = 1.3,
    start_size: int = 400,
    min_size: int = 40,
) -> tuple[ImageFont.FreeTypeFont, int, list[tuple[str, int, int, int, int]]]:
    """
    Find the largest font size where all lines fit.
    Returns (font, size, line_metrics) where line_metrics is
    [(text, x_offset, y_offset, text_width, text_height), ...].
    """
    lo, hi = min_size, start_size
    best_size = lo
    best_metrics: list[tuple[str, int, int, int, int]] = []

    while lo <= hi:
        mid = (lo + hi) // 2
        font = font_loader(mid)
        metrics = []
        total_height = 0
        fits = True

        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            if tw > max_width:
                fits = False
                break
            line_h = int(th * line_spacing) if i < len(lines) - 1 else th
            metrics.append((line, 0, total_height, tw, th))
            total_height += line_h

        if fits and total_height <= max_height:
            best_size = mid
            best_metrics = metrics
            lo = mid + 1
        else:
            hi = mid - 1

    # Recalculate metrics at best size
    font = font_loader(best_size)
    final_metrics = []
    total_height = 0
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        line_h = int(th * line_spacing) if i < len(lines) - 1 else th
        final_metrics.append((line, 0, total_height, tw, th))
        total_height += line_h

    return font, best_size, final_metrics


def render_stacked(
    img: Image.Image,
    text: str,
    font_loader,
    fg_color: str | tuple,
    safe_zone: tuple[int, int, int, int],
    shadow: bool = True,
    line_spacing: float = 1.3,
    max_font_size: int = 400,
) -> None:
    """
    Render multi-line text stacked and centered.
    Lines are split on newlines or auto-wrapped on spaces.
    """
    draw = ImageDraw.Draw(img)
    sz = safe_zone
    max_w = sz[2] - sz[0]
    max_h = sz[3] - sz[1]

    # Split into lines
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        lines = [text]

    font, _, metrics = _fit_lines(
        draw, lines, font_loader, max_w, max_h,
        line_spacing=line_spacing, start_size=max_font_size,
    )

    if not metrics:
        return

    # Calculate total block height
    total_h = metrics[-1][2] + metrics[-1][4]
    block_y = sz[1] + (max_h - total_h) // 2

    for line_text, _, y_off, tw, th in metrics:
        x = sz[0] + (max_w - tw) // 2
        y = block_y + y_off

        # Adjust for font bbox offset
        bbox = draw.textbbox((0, 0), line_text, font=font)
        x -= bbox[0]
        y -= bbox[1]

        if shadow:
            draw_text_with_shadow(img, (x, y), line_text, font, fg_color)
        else:
            draw.text((x, y), line_text, font=font, fill=fg_color)
