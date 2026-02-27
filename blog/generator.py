"""Blog post generator — combines landmark + style data into SEO-optimized HTML posts."""

from __future__ import annotations

import re
from typing import Iterator

from .data.landmarks import LANDMARKS, LANDMARKS_BY_KEY
from .data.styles import STYLES, STYLES_BY_KEY
from .templates import get_template


def _slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[''']", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def generate_post(landmark: dict, style: dict, template_index: int = 0) -> dict:
    """Generate a single blog post for a landmark + style combination.

    Returns dict with: title, body_html, tags, summary, slug
    """
    template_fn = get_template(template_index)
    body_html = template_fn(landmark, style)

    title = (
        f"{landmark['name']} Meets {style['name']}: "
        f"{style['artist']}'s Style as Wall Art"
    )
    # Trim title to ~70 chars if needed
    if len(title) > 75:
        title = (
            f"{landmark['name']} in {style['artist']}'s "
            f"{style['name']} Style"
        )

    summary = (
        f"Discover {landmark['name']} reimagined in the style of "
        f"{style['artist']}'s {style['name']}. "
        f"Shop unique wall art prints and tees inspired by {landmark['location']}."
    )
    # Trim meta description to ~160 chars
    if len(summary) > 160:
        summary = summary[:157].rsplit(" ", 1)[0] + "..."

    tag_parts = [
        landmark["name"],
        style["name"],
        style["artist"],
        style["movement"],
        "wall art",
        "art print",
        landmark["location"],
        landmark["country"],
        "neural style transfer",
        "landmark art",
    ]
    tags = ", ".join(tag_parts)

    slug = _slugify(f"{landmark['key']}-{style['key']}-wall-art")

    return {
        "title": title,
        "body_html": body_html,
        "tags": tags,
        "summary": summary,
        "slug": slug,
        "landmark_key": landmark["key"],
        "style_key": style["key"],
    }


def generate_all_posts(
    landmark_key: str | None = None,
    style_key: str | None = None,
) -> Iterator[dict]:
    """Generate blog posts for all (or filtered) landmark+style combinations.

    Rotates through 3 template variations to avoid repetitive structure.
    """
    landmarks = [LANDMARKS_BY_KEY[landmark_key]] if landmark_key else LANDMARKS
    styles = [STYLES_BY_KEY[style_key]] if style_key else STYLES

    index = 0
    for lm in landmarks:
        for st in styles:
            yield generate_post(lm, st, template_index=index)
            index += 1
