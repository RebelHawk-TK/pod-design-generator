"""Niche/themed template-based design generator."""

from __future__ import annotations

import json
import random
from pathlib import Path

from PIL import Image

from src.canvas import create_canvas
from src.colors import resolve_colors, hex_to_rgba
from src.config import ProductSpec, TEMPLATES_DIR
from src.fonts import font_manager
from src.generators.base import BaseGenerator
from src.layouts.centered import render_centered
from src.layouts.stacked import render_stacked
from src.layouts.arced import render_arced


LAYOUT_MAP = {
    "centered": render_centered,
    "stacked": render_stacked,
    "arced": render_arced,
}


class NicheDesignGenerator(BaseGenerator):
    """Generate designs from niche theme templates (JSON configs)."""

    def __init__(
        self,
        theme: str,
        text: str | None = None,
        products: list[str] | None = None,
        template_dir: Path = TEMPLATES_DIR,
    ):
        super().__init__(products)
        self.theme = theme
        self.custom_text = text
        self.template_dir = template_dir
        self.template = self._load_template()

    def _load_template(self) -> dict:
        path = self.template_dir / f"{self.theme}.json"
        if not path.exists():
            available = [f.stem for f in self.template_dir.glob("*.json")]
            raise FileNotFoundError(
                f"Theme '{self.theme}' not found. Available: {available}"
            )
        with open(path) as f:
            return json.load(f)

    def generate(self, product: ProductSpec, **kwargs) -> Image.Image:
        tmpl = self.template
        rng = random.Random()

        # Pick text: custom > random from template phrases
        if self.custom_text:
            text = self.custom_text
        else:
            phrases = tmpl.get("phrases", ["Design"])
            text = rng.choice(phrases)

        # Style from template
        style = tmpl.get("style", {})
        font_name = style.get("font", "anton")
        color_key = style.get("colors", "white-on-black")
        layout = style.get("layout", "centered")
        shadow = style.get("shadow", True)

        fg_hex, bg_hex = resolve_colors(
            color_key, None, transparent_bg=product.transparent
        )
        fg_color = hex_to_rgba(fg_hex)

        canvas = create_canvas(product, bg_hex)
        if canvas.mode != "RGBA":
            canvas = canvas.convert("RGBA")

        def font_loader(size: int):
            return font_manager.get(font_name, size)

        renderer = LAYOUT_MAP.get(layout, render_centered)
        if layout == "arced":
            renderer(canvas, text, font_loader, fg_color, product.safe_zone, shadow=shadow)
        else:
            renderer(canvas, text, font_loader, fg_color, product.safe_zone, shadow=shadow)

        if product.mode == "RGB":
            canvas = canvas.convert("RGB")
        return canvas

    def get_theme_info(self) -> dict:
        """Return template metadata for metadata generation."""
        return {
            "theme": self.theme,
            "category": self.template.get("category", ""),
            "tags": self.template.get("tags", []),
            "description_hint": self.template.get("description", ""),
        }
