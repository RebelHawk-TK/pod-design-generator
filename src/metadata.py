"""Metadata generator — title, description, and tags for Redbubble uploads."""

from __future__ import annotations

import json
import re
from pathlib import Path


def generate_metadata(
    text: str,
    design_type: str = "text",
    theme: str | None = None,
    style: str | None = None,
    extra_tags: list[str] | None = None,
) -> dict[str, str | list[str]]:
    """
    Generate upload metadata (title, description, tags) for a design.
    Returns dict with 'title', 'description', 'tags'.
    """
    # Clean text for use in metadata
    clean = text.strip().replace("\n", " ")

    # Title
    title = _generate_title(clean, design_type, theme)

    # Description
    description = _generate_description(clean, design_type, theme, style)

    # Tags (up to 15)
    tags = _generate_tags(clean, design_type, theme, style, extra_tags)

    return {
        "title": title,
        "description": description,
        "tags": tags[:15],
    }


def save_metadata(metadata: dict, output_path: Path) -> Path:
    """Save metadata as JSON next to the design file."""
    meta_path = output_path.with_suffix(".json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    return meta_path


def _generate_title(text: str, design_type: str, theme: str | None) -> str:
    # Truncate long text
    short = text[:60].strip()
    if len(text) > 60:
        short = short.rsplit(" ", 1)[0] + "..."

    if design_type == "pattern":
        return f"Abstract Pattern Design"
    if theme:
        return f"{short} - {theme.title()} Design"
    return f"{short} - Typography Design"


def _generate_description(
    text: str, design_type: str, theme: str | None, style: str | None
) -> str:
    parts = []
    if design_type == "text":
        parts.append(f'"{text}" typography design.')
    elif design_type == "pattern":
        style_desc = style or "geometric"
        parts.append(f"Abstract {style_desc} pattern design.")
    elif design_type == "niche" and theme:
        parts.append(f'"{text}" — {theme} themed design.')

    parts.append("Available on t-shirts, stickers, posters, and more.")
    parts.append("High-quality print-on-demand artwork.")

    return " ".join(parts)


def _generate_tags(
    text: str,
    design_type: str,
    theme: str | None,
    style: str | None,
    extra_tags: list[str] | None,
) -> list[str]:
    tags = set()

    # Extract words from text
    words = re.findall(r"[a-zA-Z]+", text.lower())
    # Add meaningful words (skip very short ones)
    for w in words:
        if len(w) >= 3:
            tags.add(w)

    # Type-based tags
    if design_type == "text":
        tags.update(["typography", "quote", "text-design", "lettering"])
    elif design_type == "pattern":
        tags.update(["pattern", "abstract", "geometric"])
        if style:
            tags.add(style)
    elif design_type == "niche":
        tags.update(["themed", "niche"])

    if theme:
        tags.add(theme.lower())

    # Standard POD tags
    tags.update(["redbubble", "print-on-demand", "design"])

    if extra_tags:
        tags.update(t.lower() for t in extra_tags)

    return sorted(tags)[:15]
