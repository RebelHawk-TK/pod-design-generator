"""Canvas creation, safe zones, and saving."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from src.config import PRODUCTS, OUTPUT_DIR, ProductSpec
from src.colors import hex_to_rgba, hex_to_rgb


def create_canvas(product: ProductSpec, bg_color: str | None = None) -> Image.Image:
    """
    Create a blank canvas for the given product.
    bg_color: hex string or None for transparent.
    """
    if bg_color is None:
        return Image.new("RGBA", (product.width, product.height), (0, 0, 0, 0))

    if product.transparent:
        fill = hex_to_rgba(bg_color)
        return Image.new("RGBA", (product.width, product.height), fill)
    else:
        fill = hex_to_rgb(bg_color)
        return Image.new("RGB", (product.width, product.height), fill)


def get_safe_zone(product: ProductSpec) -> tuple[int, int, int, int]:
    """Return (left, top, right, bottom) safe zone boundaries."""
    return product.safe_zone


def save_design(
    image: Image.Image,
    product_name: str,
    filename: str,
    output_dir: Path = OUTPUT_DIR,
) -> Path:
    """Save a design image to output/<product>/<filename>.png."""
    product_dir = output_dir / product_name
    product_dir.mkdir(parents=True, exist_ok=True)
    path = product_dir / f"{filename}.png"
    image.save(str(path), "PNG")
    return path
