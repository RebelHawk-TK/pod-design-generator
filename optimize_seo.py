#!/usr/bin/env python3
"""SEO optimizer for POD design metadata (tags + titles).

Analyzes existing tags and titles, then rewrites them with better
search-optimized keywords. Backs up originals before modifying.

Problems this fixes:
    - 80%+ tag overlap within each niche (designs compete with each other)
    - Generic title suffixes ("- Coffee Design" → "- Coffee Lover T-Shirt")
    - Missing phrase-derived tags (the actual quote IS the search term)
    - No product-type or gift-occasion tags
    - Duplicate titles

Usage:
    python3 optimize_seo.py --analyze                  # Show current issues
    python3 optimize_seo.py --preview --limit 10       # Preview changes
    python3 optimize_seo.py --apply                    # Apply to all designs
    python3 optimize_seo.py --apply --folder tshirt    # Apply to one folder
    python3 optimize_seo.py --restore                  # Restore from backup
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).parent / "output"
BACKUP_DIR = Path(__file__).parent / "output_metadata_backup"
FOLDERS = ["tshirt", "sticker", "poster"]

# Core niche tags — the 5 strongest per niche (kept for every design)
CORE_NICHE_TAGS = {
    "coffee": ["coffee", "coffee-lover", "caffeine", "barista", "espresso"],
    "dad": ["dad", "fathers-day", "father", "daddy", "dadlife"],
    "drinking": ["drinking", "beer", "wine", "cocktail", "happy-hour"],
    "fitness": ["fitness", "gym", "workout", "exercise", "lifting"],
    "funny": ["funny", "humor", "comedy", "hilarious", "joke"],
    "gaming": ["gaming", "gamer", "video-games", "controller", "nerd"],
    "hobby": ["hobby", "craft", "creative", "maker", "diy"],
    "introvert": ["introvert", "antisocial", "homebody", "introvert-life", "alone"],
    "mom": ["mom", "mama", "mothers-day", "momlife", "mother"],
    "motivational": ["motivation", "inspire", "hustle", "grind", "mindset"],
    "pets": ["pet-lover", "dog", "cat", "animal-lover", "fur-baby"],
    "profession": ["work", "career", "boss", "office", "job"],
    "sarcasm": ["sarcasm", "sarcastic", "attitude", "petty", "savage"],
    "seasonal": ["holiday", "christmas", "halloween", "seasonal", "festive"],
}

# Title suffix improvements per niche
TITLE_SUFFIXES = {
    "coffee": "Coffee Lover T-Shirt",
    "dad": "Funny Dad T-Shirt Gift",
    "drinking": "Drinking Humor Shirt",
    "fitness": "Gym Motivation Shirt",
    "funny": "Funny T-Shirt Gift",
    "gaming": "Gamer T-Shirt Gift",
    "hobby": "Hobby Lover Shirt",
    "introvert": "Introvert T-Shirt Gift",
    "mom": "Mom Life T-Shirt Gift",
    "motivational": "Motivational T-Shirt",
    "pets": "Pet Lover T-Shirt Gift",
    "profession": "Funny Work T-Shirt",
    "sarcasm": "Sarcastic T-Shirt Gift",
    "seasonal": "Holiday T-Shirt",
}
DEFAULT_SUFFIX = "Graphic T-Shirt Gift"

# Gift/occasion tags to sprinkle in (rotated per design)
GIFT_TAGS = [
    "gift-for-him", "gift-for-her", "birthday-gift", "christmas-gift",
    "gift-idea", "funny-gift", "unique-gift", "stocking-stuffer",
]

# Stopwords to exclude from phrase-derived tags
STOPWORDS = frozenset({
    "i", "im", "me", "my", "we", "you", "your", "he", "she", "it", "its",
    "a", "an", "the", "and", "or", "but", "if", "in", "on", "at", "to",
    "of", "for", "is", "am", "are", "was", "be", "do", "did", "dont",
    "not", "no", "so", "up", "out", "just", "that", "this", "with",
    "have", "has", "had", "can", "will", "would", "could", "should",
    "all", "than", "then", "too", "very", "been", "being", "let",
    "got", "get", "ive", "ill", "wont", "cant", "doesnt",
})


# ---------------------------------------------------------------------------
# Phrase analysis
# ---------------------------------------------------------------------------

def extract_phrase(title: str) -> str:
    """Extract the design phrase from the title (before the ' - ' suffix)."""
    if " - " in title:
        return title.split(" - ")[0].strip()
    return title.strip()


def phrase_to_compound_tag(phrase: str) -> str | None:
    """Convert a phrase to a hyphenated compound tag if it's short enough."""
    words = re.findall(r"[a-zA-Z]+", phrase.lower())
    words = [w for w in words if w not in STOPWORDS and len(w) > 1]
    if 2 <= len(words) <= 5:
        tag = "-".join(words)
        if len(tag) <= 20:  # Etsy max tag length
            return tag
    return None


# Single words too vague to be useful as standalone tags
_WEAK_SINGLE_WORDS = frozenset({
    "don", "wont", "cant", "doesnt", "let", "run", "say", "put", "try",
    "into", "over", "turn", "first", "second", "talk", "make", "take",
    "still", "ever", "never", "always", "much", "well", "way", "day",
    "thing", "things", "man", "men", "one", "every", "after", "before",
    "need", "want", "know", "think", "look", "give", "keep", "made",
    "going", "come", "right", "good", "new", "old", "big", "little",
})


def phrase_to_keyword_tags(phrase: str) -> list[str]:
    """Extract meaningful keyword tags from a phrase.

    Prioritizes 2-word compound tags over weak single words.
    """
    words = re.findall(r"[a-zA-Z]+", phrase.lower())
    tags = []
    seen = set()

    # First: 2-word compound tags (higher search value)
    clean_words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    for i in range(len(clean_words) - 1):
        compound = f"{clean_words[i]}-{clean_words[i + 1]}"
        if len(compound) <= 20 and compound not in seen:
            seen.add(compound)
            tags.append(compound)

    # Then: strong single words (4+ chars, not in weak list)
    for word in clean_words:
        if word in seen or word in _WEAK_SINGLE_WORDS:
            continue
        if len(word) >= 4:
            seen.add(word)
            tags.append(word)

    return tags


def _phrase_has_word(phrase_lower: str, word: str) -> bool:
    """Check if a word appears as a whole word in the phrase (not as a substring)."""
    return bool(re.search(rf'\b{re.escape(word)}\b', phrase_lower))


def detect_special_context(phrase: str, niche: str) -> list[str]:
    """Detect special context in the phrase that should generate extra tags."""
    p = phrase.lower()
    extra = []

    # Fishing puns in dad niche
    fishing_words = ["reel", "fishing", "catch", "bass", "rod", "tackle", "hooked"]
    if any(_phrase_has_word(p, w) for w in fishing_words):
        extra.extend(["fishing", "fishing-gift", "fisherman"])

    # Beer/drinking references
    beer_words = ["beer", "brew", "ale", "ipa", "pint", "keg", "draft"]
    if any(_phrase_has_word(p, w) for w in beer_words):
        extra.extend(["beer-lover", "craft-beer"])

    # Pet-specific (whole-word matching to avoid "education" → "cat")
    if any(_phrase_has_word(p, w) for w in ["dog", "puppy", "bark", "woof", "paw"]):
        extra.extend(["dog-lover", "dog-mom"])
    if any(_phrase_has_word(p, w) for w in ["cat", "kitten", "meow", "purr"]):
        extra.extend(["cat-lover", "cat-mom"])

    # Food references in coffee
    food_words = ["espresso", "latte", "cappuccino", "mocha", "brew"]
    if niche == "coffee" and any(_phrase_has_word(p, w) for w in food_words):
        extra.extend(["coffee-drinker", "morning-coffee"])

    # Gaming specific
    game_words = ["level", "respawn", "noob", "rage", "loot", "quest"]
    if any(_phrase_has_word(p, w) for w in game_words):
        extra.extend(["video-game", "gamer-life"])

    # Gym/fitness specific
    gym_words = ["squat", "deadlift", "bench", "protein", "gains", "swole", "beast"]
    if any(_phrase_has_word(p, w) for w in gym_words):
        extra.extend(["gym-rat", "bodybuilder"])

    return extra


# ---------------------------------------------------------------------------
# Tag optimization
# ---------------------------------------------------------------------------

def optimize_tags(
    current_tags: list[str],
    phrase: str,
    niche: str,
    design_index: int,
    max_tags: int = 15,
) -> list[str]:
    """Generate an optimized tag set for a design."""
    new_tags: list[str] = []
    seen: set[str] = set()

    def add_tag(tag: str) -> bool:
        t = tag.lower().strip()
        if t and t not in seen and len(new_tags) < max_tags:
            seen.add(t)
            new_tags.append(t)
            return True
        return False

    # 1. Phrase compound tag (highest value — exact match for search)
    compound = phrase_to_compound_tag(phrase)
    if compound:
        add_tag(compound)

    # 2. Core niche tags (5 tags)
    core = CORE_NICHE_TAGS.get(niche, [])
    for tag in core:
        add_tag(tag)

    # 3. Phrase-derived keyword tags
    phrase_tags = phrase_to_keyword_tags(phrase)
    for tag in phrase_tags:
        add_tag(tag)

    # 4. Special context tags
    special = detect_special_context(phrase, niche)
    for tag in special:
        add_tag(tag)

    # 5. Rotate gift/occasion tags (different ones per design to diversify)
    gift_offset = design_index % len(GIFT_TAGS)
    for j in range(3):
        idx = (gift_offset + j) % len(GIFT_TAGS)
        add_tag(GIFT_TAGS[idx])

    # 6. Fill remaining from original tags (prefer ones not already added)
    for tag in current_tags:
        add_tag(tag)

    return new_tags[:max_tags]


# ---------------------------------------------------------------------------
# Title optimization
# ---------------------------------------------------------------------------

def optimize_title(title: str, niche: str) -> str:
    """Improve the title suffix for better search targeting."""
    phrase = extract_phrase(title)
    suffix = TITLE_SUFFIXES.get(niche, DEFAULT_SUFFIX)
    return f"{phrase} - {suffix}"


# ---------------------------------------------------------------------------
# Duplicate detection
# ---------------------------------------------------------------------------

def find_duplicate_titles(folder: str) -> dict[str, list[Path]]:
    """Find designs with identical titles within a folder."""
    title_to_files: dict[str, list[Path]] = {}
    for jf in sorted((OUTPUT_DIR / folder).glob("*.json")):
        meta = json.loads(jf.read_text())
        title = meta.get("title", "")
        title_to_files.setdefault(title, []).append(jf)
    return {t: files for t, files in title_to_files.items() if len(files) > 1}


# ---------------------------------------------------------------------------
# Backup / restore
# ---------------------------------------------------------------------------

def backup_metadata() -> None:
    """Back up all JSON metadata files."""
    if BACKUP_DIR.exists():
        print(f"Backup already exists at {BACKUP_DIR}")
        print("  Delete it first or use --restore to revert.")
        return

    BACKUP_DIR.mkdir(parents=True)
    count = 0
    for folder in FOLDERS:
        src_dir = OUTPUT_DIR / folder
        dst_dir = BACKUP_DIR / folder
        dst_dir.mkdir(parents=True, exist_ok=True)
        for jf in src_dir.glob("*.json"):
            shutil.copy2(jf, dst_dir / jf.name)
            count += 1

    print(f"Backed up {count} metadata files to {BACKUP_DIR}/")


def restore_metadata() -> None:
    """Restore metadata from backup."""
    if not BACKUP_DIR.exists():
        print("No backup found. Nothing to restore.")
        return

    count = 0
    for folder in FOLDERS:
        src_dir = BACKUP_DIR / folder
        dst_dir = OUTPUT_DIR / folder
        if not src_dir.exists():
            continue
        for jf in src_dir.glob("*.json"):
            shutil.copy2(jf, dst_dir / jf.name)
            count += 1

    print(f"Restored {count} metadata files from backup.")
    print(f"  You can delete the backup with: rm -rf {BACKUP_DIR}")


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze() -> None:
    """Print a detailed SEO analysis of current tags and titles."""
    print("=== SEO ANALYSIS ===\n")

    for niche in sorted(CORE_NICHE_TAGS.keys()):
        designs = list((OUTPUT_DIR / "tshirt").glob(f"{niche}_*.json"))
        if not designs:
            continue

        all_tags: list[list[str]] = []
        for jf in designs:
            meta = json.loads(jf.read_text())
            all_tags.append(meta.get("tags", []))

        # Compute overlap
        tag_sets = [set(tags) for tags in all_tags]
        overlaps = []
        for i in range(len(tag_sets) - 1):
            a, b = tag_sets[i], tag_sets[i + 1]
            if a | b:
                overlaps.append(len(a & b) / len(a | b))

        avg_overlap = sum(overlaps) / len(overlaps) if overlaps else 0

        # Count universal tags
        tag_counter = Counter(t for tags in all_tags for t in tags)
        universal = sum(1 for _, c in tag_counter.items() if c == len(designs))

        severity = "!!!" if avg_overlap > 0.75 else "! " if avg_overlap > 0.60 else "ok"
        print(f"  {niche:15s}  {len(designs):3d} designs  overlap={avg_overlap:.0%}  universal={universal:2d}/15  {severity}")

    # Duplicates
    print("\nDuplicate titles:")
    for folder in FOLDERS:
        dupes = find_duplicate_titles(folder)
        if dupes:
            for title, files in dupes.items():
                print(f"  [{folder}] \"{title[:60]}\" x{len(files)}")

    # Title suffix analysis
    print("\nTitle suffixes (tshirt):")
    suffixes = Counter()
    for jf in (OUTPUT_DIR / "tshirt").glob("*.json"):
        meta = json.loads(jf.read_text())
        title = meta.get("title", "")
        if " - " in title:
            suffixes[title.split(" - ")[-1]] += 1
    for s, c in suffixes.most_common(10):
        print(f"  \"{s}\": {c}")


# ---------------------------------------------------------------------------
# Preview / Apply
# ---------------------------------------------------------------------------

def process_designs(
    apply: bool = False,
    preview_limit: int = 0,
    target_folder: str | None = None,
) -> None:
    """Preview or apply tag/title optimizations."""
    folders = [target_folder] if target_folder else FOLDERS
    total_modified = 0
    previewed = 0

    for folder in folders:
        folder_dir = OUTPUT_DIR / folder
        if not folder_dir.is_dir():
            continue

        jsons = sorted(folder_dir.glob("*.json"))
        niche_counters: dict[str, int] = {}

        for jf in jsons:
            meta = json.loads(jf.read_text())
            niche = jf.stem.split("_")[0]

            # Track per-niche index for gift tag rotation
            niche_counters[niche] = niche_counters.get(niche, 0)
            design_index = niche_counters[niche]
            niche_counters[niche] += 1

            phrase = extract_phrase(meta.get("title", ""))
            old_tags = meta.get("tags", [])
            old_title = meta.get("title", "")

            new_tags = optimize_tags(old_tags, phrase, niche, design_index)
            new_title = optimize_title(old_title, niche)

            # Check if anything changed
            if new_tags == old_tags and new_title == old_title:
                continue

            if not apply:
                # Preview mode
                if preview_limit and previewed >= preview_limit:
                    continue
                previewed += 1
                print(f"[{folder}/{jf.stem}]")
                if new_title != old_title:
                    print(f"  Title:  \"{old_title}\"")
                    print(f"      ->  \"{new_title}\"")
                # Show tag diff
                old_set = set(old_tags)
                new_set = set(new_tags)
                removed = old_set - new_set
                added = new_set - old_set
                if removed:
                    print(f"  Removed: {', '.join(sorted(removed))}")
                if added:
                    print(f"  Added:   {', '.join(sorted(added))}")
                print(f"  Tags:    {', '.join(new_tags)}")
                print()
            else:
                # Apply
                meta["tags"] = new_tags
                meta["title"] = new_title
                jf.write_text(json.dumps(meta, indent=2) + "\n")
                total_modified += 1

    if apply:
        print(f"Updated {total_modified} metadata files across {', '.join(folders)}")
    elif previewed:
        print(f"Previewed {previewed} changes. Run with --apply to write them.")
    else:
        print("No changes needed.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Optimize SEO tags and titles for POD design metadata.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python3 optimize_seo.py --analyze                  # Show current issues
  python3 optimize_seo.py --preview --limit 10       # Preview first 10 changes
  python3 optimize_seo.py --preview --folder tshirt   # Preview one folder
  python3 optimize_seo.py --apply                     # Apply to all designs
  python3 optimize_seo.py --restore                   # Undo all changes
""",
    )
    parser.add_argument(
        "--analyze", action="store_true",
        help="Analyze current tag/title quality",
    )
    parser.add_argument(
        "--preview", action="store_true",
        help="Preview optimized tags and titles without writing",
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
    parser.add_argument(
        "--folder",
        help="Target a specific folder (tshirt, sticker, poster)",
    )
    args = parser.parse_args()

    if args.restore:
        restore_metadata()
        return

    if args.analyze:
        analyze()
        return

    if args.preview:
        process_designs(apply=False, preview_limit=args.limit, target_folder=args.folder)
        return

    if args.apply:
        # Back up first
        if not BACKUP_DIR.exists():
            backup_metadata()
        process_designs(apply=True, target_folder=args.folder)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
