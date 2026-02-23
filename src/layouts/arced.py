"""Curved/arced text layout — renders characters along a circular arc."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFont


def render_arced(
    img: Image.Image,
    text: str,
    font_loader,
    fg_color: str | tuple,
    safe_zone: tuple[int, int, int, int],
    arc_degrees: float = 180,
    arc_offset: float = -90,
    font_size: int | None = None,
    shadow: bool = False,
) -> None:
    """
    Render text along a circular arc within the safe zone.
    Characters are placed individually along the arc.
    """
    sz = safe_zone
    max_w = sz[2] - sz[0]
    max_h = sz[3] - sz[1]
    cx = sz[0] + max_w // 2
    cy = sz[1] + max_h // 2

    # Auto-size font if not specified
    if font_size is None:
        font_size = max(40, min(max_w, max_h) // 8)

    font = font_loader(font_size)
    draw = ImageDraw.Draw(img)

    # Calculate radius — fit within safe zone
    radius = min(max_w, max_h) * 0.38

    # Measure total text width to distribute characters
    char_widths = []
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=font)
        char_widths.append(bbox[2] - bbox[0])

    total_width = sum(char_widths)
    if total_width == 0:
        return

    # Convert arc degrees to radians
    arc_rad = math.radians(arc_degrees)
    start_angle = math.radians(arc_offset) - arc_rad / 2

    # Place each character
    angle_consumed = 0
    for i, ch in enumerate(text):
        # Fraction of total width this char represents
        frac = char_widths[i] / total_width
        char_angle = frac * arc_rad
        angle = start_angle + angle_consumed + char_angle / 2

        # Character position on arc
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)

        # Render character onto a temp image and rotate
        bbox = draw.textbbox((0, 0), ch, font=font)
        cw = bbox[2] - bbox[0] + 10
        ch_h = bbox[3] - bbox[1] + 10
        char_img = Image.new("RGBA", (cw, ch_h), (0, 0, 0, 0))
        cd = ImageDraw.Draw(char_img)
        cd.text((-bbox[0] + 5, -bbox[1] + 5), ch, font=font, fill=fg_color)

        # Rotate to follow the arc (angle + 90 degrees so text faces outward)
        rot_deg = math.degrees(angle) + 90
        char_img = char_img.rotate(-rot_deg, expand=True, resample=Image.BICUBIC)

        # Paste centered at calculated position
        paste_x = int(px - char_img.width / 2)
        paste_y = int(py - char_img.height / 2)
        img.paste(char_img, (paste_x, paste_y), char_img)

        angle_consumed += char_angle
