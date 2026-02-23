"""Text/quote design generator."""

from __future__ import annotations

from PIL import Image

from src.canvas import create_canvas
from src.colors import resolve_colors, hex_to_rgba
from src.config import ProductSpec
from src.fonts import font_manager
from src.generators.base import BaseGenerator
from src.layouts.centered import render_centered
from src.layouts.stacked import render_stacked
from src.layouts.arced import render_arced


LAYOUT_RENDERERS = {
    "centered": render_centered,
    "stacked": render_stacked,
    "arced": render_arced,
}


class TextDesignGenerator(BaseGenerator):
    """Generate text-based designs (quotes, slogans, phrases)."""

    def __init__(
        self,
        text: str,
        font_name: str = "anton",
        color_shortcut: str | None = None,
        palette: str | None = None,
        layout: str = "centered",
        shadow: bool = True,
        products: list[str] | None = None,
    ):
        super().__init__(products)
        self.text = text
        self.font_name = font_name
        self.color_shortcut = color_shortcut
        self.palette = palette
        self.layout = layout
        self.shadow = shadow

    def generate(self, product: ProductSpec, **kwargs) -> Image.Image:
        fg_hex, bg_hex = resolve_colors(
            self.color_shortcut, self.palette, transparent_bg=product.transparent
        )
        fg_color = hex_to_rgba(fg_hex)

        canvas = create_canvas(product, bg_hex)
        # Ensure we work in RGBA for compositing
        if canvas.mode != "RGBA":
            canvas = canvas.convert("RGBA")

        safe_zone = product.safe_zone

        def font_loader(size: int):
            return font_manager.get(self.font_name, size)

        renderer = LAYOUT_RENDERERS.get(self.layout)
        if renderer is None:
            raise ValueError(
                f"Unknown layout: {self.layout}. Available: {list(LAYOUT_RENDERERS.keys())}"
            )

        if self.layout == "arced":
            renderer(canvas, self.text, font_loader, fg_color, safe_zone, shadow=self.shadow)
        else:
            renderer(canvas, self.text, font_loader, fg_color, safe_zone, shadow=self.shadow)

        # Convert back to product mode
        if product.mode == "RGB":
            canvas = canvas.convert("RGB")

        return canvas
