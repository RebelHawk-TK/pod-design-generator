"""Abstract base generator for POD designs."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from PIL import Image

from src.canvas import create_canvas, save_design
from src.config import PRODUCTS, ProductSpec


class BaseGenerator(ABC):
    """Base class for all design generators."""

    def __init__(self, products: list[str] | None = None):
        self.product_names = products or ["tshirt"]

    @abstractmethod
    def generate(self, product: ProductSpec, **kwargs) -> Image.Image:
        """Generate a design for a single product spec. Must be implemented by subclasses."""
        ...

    def generate_all(self, **kwargs) -> dict[str, Image.Image]:
        """Generate designs for all configured products."""
        results = {}
        for name in self.product_names:
            spec = PRODUCTS[name]
            results[name] = self.generate(spec, **kwargs)
        return results

    def generate_and_save(self, filename: str, **kwargs) -> list[Path]:
        """Generate and save designs for all products. Returns list of saved paths."""
        saved = []
        for name in self.product_names:
            spec = PRODUCTS[name]
            img = self.generate(spec, **kwargs)
            path = save_design(img, name, filename)
            saved.append(path)
        return saved
