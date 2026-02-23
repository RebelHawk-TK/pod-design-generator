"""Font management — loading, caching, category lookup."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

from src.config import FONTS_DIR, FONT_CATEGORIES, FONT_REGISTRY


class FontManager:
    """Loads and caches TrueType fonts from the fonts/ directory."""

    def __init__(self, fonts_dir: Path = FONTS_DIR):
        self.fonts_dir = fonts_dir

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, name: str, size: int) -> ImageFont.FreeTypeFont:
        """Load a font by shortname or filename stem at given size."""
        stem = self._resolve(name)
        return self._load(stem, size)

    def get_by_category(self, category: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
        """Load a font from a category (bold/script/clean)."""
        stems = FONT_CATEGORIES.get(category, [])
        if not stems:
            raise ValueError(f"Unknown font category: {category}")
        stem = stems[index % len(stems)]
        return self._load(stem, size)

    def list_available(self) -> list[str]:
        """Return shortnames of all available (downloaded) fonts."""
        available = []
        for shortname, stem in FONT_REGISTRY.items():
            path = self.fonts_dir / f"{stem}.ttf"
            if path.exists():
                available.append(shortname)
        return sorted(set(available))

    def list_categories(self) -> dict[str, list[str]]:
        return dict(FONT_CATEGORIES)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _resolve(self, name: str) -> str:
        """Resolve a shortname or stem to a filename stem."""
        key = name.lower().replace(" ", "").replace("-", "").replace("_", "")
        if key in FONT_REGISTRY:
            return FONT_REGISTRY[key]
        # Try direct stem match
        path = self.fonts_dir / f"{name}.ttf"
        if path.exists():
            return name
        raise ValueError(
            f"Unknown font '{name}'. Available: {', '.join(self.list_available())}"
        )

    @lru_cache(maxsize=64)
    def _load(self, stem: str, size: int) -> ImageFont.FreeTypeFont:
        path = self.fonts_dir / f"{stem}.ttf"
        if not path.exists():
            raise FileNotFoundError(
                f"Font file not found: {path}. Run setup_fonts.py first."
            )
        return ImageFont.truetype(str(path), size)


# Module-level singleton
font_manager = FontManager()
