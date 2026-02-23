"""Linear and radial gradient generation."""

from __future__ import annotations

import math

from PIL import Image

from src.colors import hex_to_rgba


def linear_gradient(
    width: int,
    height: int,
    color_start: str,
    color_end: str,
    direction: str = "vertical",
) -> Image.Image:
    """
    Generate a linear gradient image.
    direction: 'vertical', 'horizontal', or 'diagonal'.
    """
    c1 = hex_to_rgba(color_start)
    c2 = hex_to_rgba(color_end)
    img = Image.new("RGBA", (width, height))
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            if direction == "vertical":
                t = y / max(height - 1, 1)
            elif direction == "horizontal":
                t = x / max(width - 1, 1)
            else:  # diagonal
                t = (x + y) / max(width + height - 2, 1)

            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            a = int(c1[3] + (c2[3] - c1[3]) * t)
            pixels[x, y] = (r, g, b, a)

    return img


def radial_gradient(
    width: int,
    height: int,
    color_center: str,
    color_edge: str,
) -> Image.Image:
    """Generate a radial gradient from center to edges."""
    c1 = hex_to_rgba(color_center)
    c2 = hex_to_rgba(color_edge)
    img = Image.new("RGBA", (width, height))
    pixels = img.load()
    cx, cy = width / 2, height / 2
    max_dist = math.sqrt(cx * cx + cy * cy)

    for y in range(height):
        for x in range(width):
            dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            t = min(dist / max_dist, 1.0)
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            a = int(c1[3] + (c2[3] - c1[3]) * t)
            pixels[x, y] = (r, g, b, a)

    return img
