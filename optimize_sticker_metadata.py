#!/usr/bin/env python3
"""Optimize sticker metadata for Printify uploads.

Rewrites titles, descriptions, and tags for sticker designs that currently
have t-shirt-oriented metadata (from optimize_seo.py which targeted shirts).

Changes:
    - Title suffixes: "Coffee Lover T-Shirt" → "Coffee Lover Sticker"
    - Descriptions: generic "Available on t-shirts..." → sticker-specific copy
    - Tags: remove hyphens (Printify limit), swap product refs, cap at 13

Usage:
    python3 optimize_sticker_metadata.py --preview --limit 5   # Preview changes
    python3 optimize_sticker_metadata.py --apply                # Apply to all 705
    python3 optimize_sticker_metadata.py --restore              # Restore from backup
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"
STICKER_DIR = OUTPUT_DIR / "sticker"
BACKUP_DIR = OUTPUT_DIR / "sticker_backup"

MAX_TAGS = 13  # Printify limit

# Title suffix map: old (t-shirt) → new (sticker)
TITLE_SUFFIX_MAP = {
    "Coffee Lover T-Shirt": "Coffee Lover Sticker",
    "Funny Dad T-Shirt Gift": "Funny Dad Sticker",
    "Drinking Humor Shirt": "Drinking Humor Sticker",
    "Gym Motivation Shirt": "Gym Motivation Sticker",
    "Funny T-Shirt Gift": "Funny Sticker",
    "Gamer T-Shirt Gift": "Gamer Sticker",
    "Hobby Lover Shirt": "Hobby Lover Sticker",
    "Introvert T-Shirt Gift": "Introvert Sticker",
    "Mom Life T-Shirt Gift": "Mom Life Sticker",
    "Motivational T-Shirt": "Motivational Sticker",
    "Pet Lover T-Shirt Gift": "Pet Lover Sticker",
    "Funny Work T-Shirt": "Funny Work Sticker",
    "Sarcastic T-Shirt Gift": "Sarcastic Sticker",
    "Holiday T-Shirt": "Holiday Sticker",
    "Graphic T-Shirt Gift": "Graphic Sticker",
}

# Description templates — rotated per design for variety
DESCRIPTION_TEMPLATES = [
    '"{phrase}" — premium die-cut vinyl sticker. Weatherproof and durable, perfect for laptops, water bottles, notebooks, and phone cases. Made with high-quality adhesive that won\'t leave residue. A fun way to express your personality or a great gift idea for any occasion.',
    '"{phrase}" — die-cut vinyl sticker built to last. Stick it on your laptop, water bottle, skateboard, or notebook. UV and weather resistant so it won\'t fade or peel. Makes an awesome gift for birthdays, holidays, or just because.',
    '"{phrase}" — high-quality die-cut sticker made from durable vinyl. Perfect for decorating laptops, tumblers, car bumpers, notebooks, and more. Waterproof and scratch-resistant. An easy, affordable way to add personality to your everyday gear.',
    '"{phrase}" — express yourself with this vibrant die-cut vinyl sticker. Designed to stick strong on water bottles, laptops, phone cases, journals, and toolboxes. Weatherproof and long-lasting. Great as a small gift, stocking stuffer, or personal treat.',
    '"{phrase}" — bold die-cut vinyl sticker that makes a statement. Apply to your laptop, hydro flask, car window, or planner. Durable, waterproof, and easy to apply with no bubbles. Perfect for anyone who loves to customize their stuff.',
]

# Tags to remove (t-shirt specific)
TAGS_TO_REMOVE = {
    "coffee-shirt", "shirt", "tshirt", "t-shirt", "tee", "graphic-tee",
    "graphic-shirt", "funny-shirt", "work-shirt",
}

# Tags to add (sticker specific) — rotated per design
STICKER_TAGS = [
    "sticker", "vinyl sticker", "die cut sticker", "laptop sticker",
    "water bottle sticker", "funny sticker", "cute sticker",
    "weatherproof sticker", "decal",
]


# ---------------------------------------------------------------------------
# Title rewriting
# ---------------------------------------------------------------------------

def rewrite_title(title: str) -> str:
    """Replace t-shirt title suffix with sticker equivalent."""
    if " - " not in title:
        return title

    phrase, suffix = title.rsplit(" - ", 1)

    new_suffix = TITLE_SUFFIX_MAP.get(suffix)
    if new_suffix:
        return f"{phrase} - {new_suffix}"

    # Fallback: if suffix contains "T-Shirt" or "Shirt", replace generically
    if "T-Shirt" in suffix or "Shirt" in suffix:
        new_suffix = suffix.replace("T-Shirt Gift", "Sticker").replace("T-Shirt", "Sticker").replace("Shirt", "Sticker")
        return f"{phrase} - {new_suffix}"

    return title


# ---------------------------------------------------------------------------
# Description rewriting
# ---------------------------------------------------------------------------

def rewrite_description(title: str, description: str, design_index: int) -> str:
    """Replace generic description with sticker-specific copy."""
    # Extract the phrase (before " - ")
    if " - " in title:
        phrase = title.rsplit(" - ", 1)[0].strip()
    else:
        phrase = title.strip()

    template = DESCRIPTION_TEMPLATES[design_index % len(DESCRIPTION_TEMPLATES)]
    return template.format(phrase=phrase)


# ---------------------------------------------------------------------------
# Tag rewriting
# ---------------------------------------------------------------------------

def rewrite_tags(tags: list[str], design_index: int) -> list[str]:
    """Fix tags for Printify sticker products.

    - Remove hyphens (Printify doesn't support them)
    - Remove t-shirt-specific tags
    - Add sticker-specific tags
    - Cap at 13
    """
    new_tags: list[str] = []
    seen: set[str] = set()

    def add_tag(tag: str) -> bool:
        t = tag.lower().strip()
        if t and t not in seen and len(new_tags) < MAX_TAGS:
            seen.add(t)
            new_tags.append(t)
            return True
        return False

    # 1. Add 3 rotated sticker-specific tags first (high priority)
    offset = design_index % len(STICKER_TAGS)
    for j in range(3):
        idx = (offset + j) % len(STICKER_TAGS)
        add_tag(STICKER_TAGS[idx])

    # 2. Keep existing tags (dehyphenated, skip t-shirt ones)
    for tag in tags:
        tag_lower = tag.lower().strip()
        if tag_lower in TAGS_TO_REMOVE:
            continue
        # Remove hyphens
        cleaned = tag_lower.replace("-", " ")
        add_tag(cleaned)

    return new_tags[:MAX_TAGS]


# ---------------------------------------------------------------------------
# Backup / restore
# ---------------------------------------------------------------------------

def backup_metadata() -> int:
    """Back up all sticker JSON metadata files."""
    if BACKUP_DIR.exists():
        count = len(list(BACKUP_DIR.glob("*.json")))
        print(f"Backup already exists at {BACKUP_DIR} ({count} files)")
        print("  Delete it first or use --restore to revert.")
        return 0

    BACKUP_DIR.mkdir(parents=True)
    count = 0
    for jf in STICKER_DIR.glob("*.json"):
        shutil.copy2(jf, BACKUP_DIR / jf.name)
        count += 1

    print(f"Backed up {count} sticker metadata files to {BACKUP_DIR}/")
    return count


def restore_metadata() -> None:
    """Restore sticker metadata from backup."""
    if not BACKUP_DIR.exists():
        print("No backup found. Nothing to restore.")
        return

    count = 0
    for jf in BACKUP_DIR.glob("*.json"):
        shutil.copy2(jf, STICKER_DIR / jf.name)
        count += 1

    print(f"Restored {count} sticker metadata files from backup.")
    print(f"  You can delete the backup with: rm -rf {BACKUP_DIR}")


# ---------------------------------------------------------------------------
# Preview / Apply
# ---------------------------------------------------------------------------

def process_stickers(apply: bool = False, preview_limit: int = 0) -> None:
    """Preview or apply sticker metadata optimizations."""
    jsons = sorted(STICKER_DIR.glob("*.json"))

    if not jsons:
        print("No sticker metadata files found.")
        return

    print(f"Found {len(jsons)} sticker metadata files\n")

    modified = 0
    previewed = 0
    title_fixes = 0
    desc_fixes = 0
    tag_fixes = 0
    hyphen_tags_found = 0

    for i, jf in enumerate(jsons):
        meta = json.loads(jf.read_text())
        old_title = meta.get("title", "")
        old_desc = meta.get("description", "")
        old_tags = meta.get("tags", [])

        new_title = rewrite_title(old_title)
        new_desc = rewrite_description(new_title, old_desc, i)
        new_tags = rewrite_tags(old_tags, i)

        title_changed = new_title != old_title
        desc_changed = new_desc != old_desc
        tags_changed = new_tags != old_tags

        if title_changed:
            title_fixes += 1
        if desc_changed:
            desc_fixes += 1
        if tags_changed:
            tag_fixes += 1
        if any("-" in t for t in old_tags):
            hyphen_tags_found += 1

        if not (title_changed or desc_changed or tags_changed):
            continue

        if not apply:
            if preview_limit and previewed >= preview_limit:
                continue
            previewed += 1
            print(f"[sticker/{jf.stem}]")
            if title_changed:
                print(f"  Title:  \"{old_title}\"")
                print(f"      ->  \"{new_title}\"")
            if desc_changed:
                print(f"  Desc:   \"{old_desc[:80]}...\"")
                print(f"      ->  \"{new_desc[:80]}...\"")
            if tags_changed:
                old_set = set(old_tags)
                new_set = set(new_tags)
                removed = sorted(old_set - {t.replace("-", " ") for t in old_tags} | (old_set - set(old_tags)))
                print(f"  Tags ({len(new_tags)}): {', '.join(new_tags)}")
            print()
        else:
            meta["title"] = new_title
            meta["description"] = new_desc
            meta["tags"] = new_tags
            jf.write_text(json.dumps(meta, indent=2) + "\n")
            modified += 1

    print(f"--- Summary ---")
    print(f"  Total files:     {len(jsons)}")
    print(f"  Title fixes:     {title_fixes}")
    print(f"  Description fixes: {desc_fixes}")
    print(f"  Tag fixes:       {tag_fixes}")
    print(f"  Files with hyphenated tags: {hyphen_tags_found}")

    if apply:
        print(f"\n  Updated {modified} metadata files.")
    elif previewed:
        remaining = title_fixes - previewed
        print(f"\n  Previewed {previewed} changes{f' ({remaining} more not shown)' if remaining > 0 else ''}.")
        print("  Run with --apply to write them.")
    else:
        print("\n  No changes needed.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Optimize sticker metadata (titles, descriptions, tags) for Printify.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python3 optimize_sticker_metadata.py --preview --limit 5   # Preview 5 changes
  python3 optimize_sticker_metadata.py --apply                # Apply to all stickers
  python3 optimize_sticker_metadata.py --restore              # Restore from backup
""",
    )
    parser.add_argument(
        "--preview", action="store_true",
        help="Preview changes without writing",
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Apply optimizations (backs up originals first)",
    )
    parser.add_argument(
        "--restore", action="store_true",
        help="Restore metadata from backup",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Limit preview output to N designs",
    )
    args = parser.parse_args()

    if args.restore:
        restore_metadata()
        return

    if args.preview:
        process_stickers(apply=False, preview_limit=args.limit)
        return

    if args.apply:
        if not BACKUP_DIR.exists():
            backup_metadata()
        process_stickers(apply=True)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
