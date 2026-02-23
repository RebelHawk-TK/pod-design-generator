"""Drop shadow effect for text and shapes."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def draw_text_with_shadow(
    img: Image.Image,
    position: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: str | tuple,
    shadow_color: str | tuple = (0, 0, 0, 160),
    offset: tuple[int, int] = (8, 8),
    blur_radius: int = 6,
) -> None:
    """Draw text with a drop shadow onto img (in-place via composite)."""
    # Create shadow layer
    shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    sx = position[0] + offset[0]
    sy = position[1] + offset[1]
    sd.text((sx, sy), text, font=font, fill=shadow_color)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))

    # Composite shadow then text
    img.paste(Image.alpha_composite(Image.new("RGBA", img.size, (0, 0, 0, 0)), shadow_layer), (0, 0), shadow_layer)

    draw = ImageDraw.Draw(img)
    draw.text(position, text, font=font, fill=fill)
