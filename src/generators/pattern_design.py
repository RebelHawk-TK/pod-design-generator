"""Geometric/abstract pattern generator."""

from __future__ import annotations

import random

from PIL import Image, ImageDraw

from src.canvas import create_canvas
from src.colors import get_palette, hex_to_rgba, resolve_colors
from src.config import ProductSpec
from src.effects.shapes import draw_circle, draw_triangle, draw_diamond, draw_hexagon, draw_star
from src.generators.base import BaseGenerator


class PatternDesignGenerator(BaseGenerator):
    """Generate geometric and abstract pattern designs."""

    def __init__(
        self,
        style: str = "geometric",
        palette: str = "neon",
        seed: int | None = None,
        color_shortcut: str | None = None,
        products: list[str] | None = None,
    ):
        super().__init__(products)
        self.style = style
        self.palette_name = palette
        self.seed = seed
        self.color_shortcut = color_shortcut

    def generate(self, product: ProductSpec, **kwargs) -> Image.Image:
        rng = random.Random(self.seed)
        _, bg_hex = resolve_colors(
            self.color_shortcut, self.palette_name, transparent_bg=product.transparent
        )
        canvas = create_canvas(product, bg_hex)
        if canvas.mode != "RGBA":
            canvas = canvas.convert("RGBA")

        colors = get_palette(self.palette_name)
        draw = ImageDraw.Draw(canvas)
        sz = product.safe_zone

        dispatch = {
            "geometric": self._geometric,
            "circles": self._circles,
            "triangles": self._triangles,
            "grid": self._grid,
            "tessellation": self._tessellation,
        }

        renderer = dispatch.get(self.style)
        if renderer is None:
            raise ValueError(f"Unknown pattern style: {self.style}. Available: {list(dispatch.keys())}")

        renderer(draw, canvas, sz, colors, rng, product)

        if product.mode == "RGB":
            canvas = canvas.convert("RGB")
        return canvas

    def _geometric(self, draw, canvas, sz, colors, rng, product):
        """Random mix of shapes."""
        shape_funcs = [draw_circle, draw_triangle, draw_diamond, draw_hexagon, draw_star]
        count = rng.randint(20, 40)
        for _ in range(count):
            func = rng.choice(shape_funcs)
            x = rng.randint(sz[0], sz[2])
            y = rng.randint(sz[1], sz[3])
            size = rng.randint(40, 200)
            color = hex_to_rgba(rng.choice(colors))
            if func == draw_circle:
                func(draw, (x, y), size, fill=color)
            elif func == draw_star:
                func(draw, (x, y), size, fill=color)
            else:
                func(draw, (x, y), size, fill=color)

    def _circles(self, draw, canvas, sz, colors, rng, product):
        """Concentric and scattered circles."""
        count = rng.randint(25, 50)
        for _ in range(count):
            x = rng.randint(sz[0], sz[2])
            y = rng.randint(sz[1], sz[3])
            r = rng.randint(20, 250)
            color = hex_to_rgba(rng.choice(colors))
            # Mix filled and outlined
            if rng.random() > 0.5:
                draw_circle(draw, (x, y), r, fill=color)
            else:
                outline_color = (*color[:3], 200)
                draw_circle(draw, (x, y), r, outline=outline_color, width=rng.randint(3, 10))

    def _triangles(self, draw, canvas, sz, colors, rng, product):
        """Scattered triangles with rotation."""
        count = rng.randint(20, 40)
        for _ in range(count):
            x = rng.randint(sz[0], sz[2])
            y = rng.randint(sz[1], sz[3])
            size = rng.randint(40, 200)
            rotation = rng.uniform(0, 360)
            color = hex_to_rgba(rng.choice(colors))
            draw_triangle(draw, (x, y), size, fill=color, rotation=rotation)

    def _grid(self, draw, canvas, sz, colors, rng, product):
        """Regular grid of shapes."""
        cell_size = rng.choice([120, 160, 200])
        shape_funcs = [draw_circle, draw_diamond, draw_hexagon]
        func = rng.choice(shape_funcs)

        for x in range(sz[0], sz[2], cell_size):
            for y in range(sz[1], sz[3], cell_size):
                color = hex_to_rgba(rng.choice(colors))
                s = cell_size // 3
                cx = x + cell_size // 2
                cy = y + cell_size // 2
                func(draw, (cx, cy), s, fill=color)

    def _tessellation(self, draw, canvas, sz, colors, rng, product):
        """Hexagonal tessellation pattern."""
        hex_size = rng.choice([60, 80, 100])
        h = int(hex_size * 1.732)  # sqrt(3)
        row = 0
        y = sz[1]
        while y < sz[3] + hex_size:
            x_offset = (hex_size * 1.5) if row % 2 else 0
            x = sz[0] + int(x_offset)
            while x < sz[2] + hex_size:
                color = hex_to_rgba(rng.choice(colors))
                draw_hexagon(draw, (x, y), hex_size - 4, fill=color)
                x += int(hex_size * 3)
            y += h // 2
            row += 1
