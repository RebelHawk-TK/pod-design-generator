"""Product specs, margins, and constants for Redbubble POD designs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FONTS_DIR = PROJECT_ROOT / "fonts"
OUTPUT_DIR = PROJECT_ROOT / "output"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

DPI = 300


@dataclass(frozen=True)
class ProductSpec:
    name: str
    width: int
    height: int
    transparent: bool
    margin_pct: float = 0.05  # 5% safe zone on each side

    @property
    def mode(self) -> str:
        return "RGBA" if self.transparent else "RGB"

    @property
    def safe_zone(self) -> tuple[int, int, int, int]:
        """Returns (left, top, right, bottom) pixel boundaries for safe zone."""
        mx = int(self.width * self.margin_pct)
        my = int(self.height * self.margin_pct)
        return (mx, my, self.width - mx, self.height - my)

    @property
    def safe_width(self) -> int:
        sz = self.safe_zone
        return sz[2] - sz[0]

    @property
    def safe_height(self) -> int:
        sz = self.safe_zone
        return sz[3] - sz[1]


PRODUCTS: dict[str, ProductSpec] = {
    "tshirt": ProductSpec("tshirt", 2875, 3900, transparent=True),
    "sticker": ProductSpec("sticker", 2800, 2800, transparent=True),
    "poster": ProductSpec("poster", 3840, 3840, transparent=False),
}

DEFAULT_PRODUCTS = ["tshirt"]

FONT_CATEGORIES = {
    "bold": ["RussoOne-Regular", "Anton-Regular", "BebasNeue-Regular"],
    "script": ["Pacifico-Regular", "Caveat-VariableFont_wght", "ShadowsIntoLight-Regular"],
    "clean": ["PatrickHand-Regular"],
}

# Flat lookup: font shortname -> filename stem
FONT_REGISTRY: dict[str, str] = {
    "russo": "RussoOne-Regular",
    "russoone": "RussoOne-Regular",
    "anton": "Anton-Regular",
    "bebas": "BebasNeue-Regular",
    "bebasneue": "BebasNeue-Regular",
    "pacifico": "Pacifico-Regular",
    "caveat": "Caveat-VariableFont_wght",
    "shadows": "ShadowsIntoLight-Regular",
    "shadowsintolight": "ShadowsIntoLight-Regular",
    "patrickhand": "PatrickHand-Regular",
    "patrick": "PatrickHand-Regular",
}
