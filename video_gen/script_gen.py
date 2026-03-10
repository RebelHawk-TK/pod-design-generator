"""Generate voiceover scripts from landmark/style data."""

from __future__ import annotations

from .config import LANDMARKS, STYLES


def generate_script(landmark_id: str, style_ids: list[str]) -> str:
    """Build a ~15-20 word voiceover script for a landmark video (~7s spoken).

    Args:
        landmark_id: Key into LANDMARKS dict.
        style_ids: List of style keys (only first used for short format).

    Returns:
        Voiceover script string.
    """
    lm = LANDMARKS[landmark_id]
    name = lm["display_name"]

    script = (
        f"Discover the {name} reimagined as fine art. "
        f"Shop the collection at moderndesignconcept.com."
    )
    return script
