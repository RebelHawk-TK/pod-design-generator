"""Color palettes, named shortcuts, and hex parsing."""

from __future__ import annotations


def hex_to_rgba(h: str) -> tuple[int, int, int, int]:
    """Parse '#RRGGBB' or '#RRGGBBAA' to an RGBA tuple."""
    h = h.lstrip("#")
    if len(h) == 6:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
    if len(h) == 8:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))
    raise ValueError(f"Invalid hex color: #{h}")


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    r, g, b, _ = hex_to_rgba(h)
    return (r, g, b)


# ---- Named color shortcuts (foreground, background) ----

COLOR_SHORTCUTS: dict[str, tuple[str, str | None]] = {
    "white-on-black": ("#FFFFFF", "#000000"),
    "black-on-white": ("#000000", "#FFFFFF"),
    "neon-on-dark": ("#39FF14", "#1A1A2E"),
    "gold-on-black": ("#FFD700", "#000000"),
    "pink-on-dark": ("#FF69B4", "#2D1B3D"),
    "cyan-on-dark": ("#00FFFF", "#0D1B2A"),
    "white-on-transparent": ("#FFFFFF", None),
    "black-on-transparent": ("#000000", None),
    "red-on-black": ("#FF3333", "#000000"),
    "sunset": ("#FF6B35", "#1A0A2E"),
}


# ---- Palettes (list of foreground-friendly colors) ----

PALETTES: dict[str, list[str]] = {
    "warm": ["#FF6B35", "#F7931E", "#FFD700", "#FF3333", "#FF69B4"],
    "cool": ["#00BFFF", "#00FFFF", "#7B68EE", "#4169E1", "#48D1CC"],
    "neon": ["#39FF14", "#FF073A", "#00FFFF", "#FF61F6", "#FFE600"],
    "pastel": ["#FFB3BA", "#BAFFC9", "#BAE1FF", "#FFFFBA", "#E8BAFF"],
    "earth": ["#8B4513", "#D2691E", "#DEB887", "#556B2F", "#BC8F8F"],
}


def resolve_colors(
    color_arg: str | None,
    palette_arg: str | None,
    transparent_bg: bool = False,
) -> tuple[str, str | None]:
    """
    Resolve CLI color arguments into (foreground_hex, background_hex_or_None).
    Returns None for background when transparent.
    """
    if color_arg:
        key = color_arg.lower().replace(" ", "-")
        if key in COLOR_SHORTCUTS:
            fg, bg = COLOR_SHORTCUTS[key]
            if transparent_bg:
                bg = None
            return fg, bg
        # Try as raw hex
        if color_arg.startswith("#"):
            return color_arg, None if transparent_bg else "#000000"

    if palette_arg:
        pal = PALETTES.get(palette_arg.lower())
        if pal:
            return pal[0], None if transparent_bg else "#1A1A2E"

    # Default
    return "#FFFFFF", None if transparent_bg else "#000000"


def get_palette(name: str) -> list[str]:
    """Get a named palette's color list."""
    if name.lower() not in PALETTES:
        raise ValueError(f"Unknown palette: {name}. Available: {list(PALETTES.keys())}")
    return PALETTES[name.lower()]
