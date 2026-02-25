#!/usr/bin/env python3
"""Clean up tags across all design metadata JSON files.

Removes platform-specific, generic filler, and stop-word fragment tags.
Backfills with niche-relevant tags to maintain 15 tags per design.

Usage:
    python3 fix_tags.py --dry-run          # Preview changes
    python3 fix_tags.py                    # Apply changes
    python3 fix_tags.py --folder tshirt    # Only fix one folder
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"

# ---------------------------------------------------------------------------
# Tags to remove
# ---------------------------------------------------------------------------

# Platform/generic filler — never useful as search terms
PLATFORM_TAGS = {
    "design", "designs", "niche", "print-on-demand", "print on demand",
    "redbubble", "teepublic", "society6", "pod", "themed", "typography",
    "graphic", "art", "artwork", "cool", "unique", "creative", "custom",
    "trendy", "aesthetic", "modern", "vintage", "retro", "classic",
}

# English stop words / phrase fragments — not meaningful search terms
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "for", "not", "can", "has", "had",
    "all", "one", "don", "isn", "let", "ago", "out", "got", "its", "did",
    "was", "are", "been", "who", "what", "just", "than", "too", "very",
    "will", "with", "that", "this", "from", "they", "your", "about",
    "would", "there", "their", "which", "could", "other", "into", "some",
    "only", "over", "such", "also", "more", "been", "being", "have",
    "does", "how", "may", "most", "much", "must", "need", "now", "own",
    "same", "should", "still", "then", "these", "those", "through",
    "under", "until", "upon", "were", "while",
}

# Common words that are useless as standalone tags (phrase fragments)
FRAGMENT_WORDS = {
    "first", "second", "led", "followed", "save", "saving", "big",
    "hard", "harder", "every", "always", "never", "really", "thing",
    "things", "make", "makes", "made", "good", "better", "best",
    "like", "keep", "keeps", "give", "gives", "take", "takes",
    "way", "even", "back", "know", "go", "going", "come", "coming",
    "see", "say", "said", "told", "put", "set", "get", "got",
}

ALL_JUNK = PLATFORM_TAGS | STOP_WORDS | FRAGMENT_WORDS

# ---------------------------------------------------------------------------
# Niche-specific backfill tags (buyer search terms)
# ---------------------------------------------------------------------------

NICHE_BACKFILL = {
    "coffee": [
        "coffee-shirt", "coffee-gift", "coffee-humor", "caffeine-addict",
        "coffee-quote", "java", "brew", "mocha", "cappuccino",
        "coffee-beans", "cafe", "coffee-obsessed", "tired", "need-coffee",
    ],
    "dad": [
        "dad-gift", "dad-humor", "dad-shirt", "best-dad", "new-dad",
        "super-dad", "papa", "grandpa", "dad-life", "funny-dad",
        "husband", "step-dad", "bonus-dad", "cool-dad",
    ],
    "drinking": [
        "wine", "whiskey", "brewery", "pub", "drinking-humor",
        "wine-lover", "beer-lover", "brunch", "bar-humor", "shots",
        "drunk", "sober", "hangover", "weekend", "friday",
    ],
    "fitness": [
        "workout", "training", "fit", "cardio", "powerlifting",
        "squat", "deadlift", "bench-press", "no-excuses", "fitness-motivation",
        "gym-humor", "gym-rat", "weightlifting", "athlete", "sweat",
    ],
    "fridge": [
        "fridge-magnet", "kitchen", "home-decor", "funny-magnet",
        "refrigerator", "kitchen-humor", "food", "cooking",
        "magnet-art", "kitchen-decor", "housewarming-gift",
    ],
    "funny": [
        "funny-shirt", "sarcastic", "meme-shirt", "viral", "relatable",
        "adult-humor", "witty", "pun", "ironic", "savage",
        "no-filter", "mood", "vibe", "same", "dead-inside",
    ],
    "gaming": [
        "video-games", "rpg", "fps", "streamer", "twitch",
        "gamer-shirt", "gamer-gift", "level-up", "respawn", "noob",
        "pro-gamer", "gaming-humor", "player", "multiplayer", "co-op",
    ],
    "hobby": [
        "hobby-shirt", "creative", "maker", "diy", "handmade",
        "nature", "hiking", "camping", "gardening", "reading",
        "painting", "photography", "music", "cooking", "travel",
    ],
    "hustle": [
        "entrepreneur", "grind", "boss", "self-made", "success",
        "startup", "side-hustle", "money", "ambition", "work-hard",
        "business", "ceo", "mindset", "goals", "discipline",
    ],
    "introvert": [
        "introvert-shirt", "introvert-gift", "social-anxiety",
        "people-person", "leave-me-alone", "no-thanks", "quiet",
        "reading", "cats", "netflix", "solitude", "inner-peace",
        "personal-space", "do-not-disturb",
    ],
    "mom": [
        "mom-gift", "mom-shirt", "mom-humor", "best-mom", "new-mom",
        "super-mom", "tired-mom", "wine-mom", "mom-boss", "mama-shirt",
        "grandma", "step-mom", "bonus-mom", "cool-mom",
    ],
    "motivational": [
        "motivation", "positive", "inspire", "never-give-up",
        "self-improvement", "growth", "strength", "courage",
        "confidence", "winner", "champion", "perseverance",
        "focus", "persistence", "resilience",
    ],
    "pets": [
        "pet-lover", "fur-baby", "paw", "woof", "meow",
        "pet-parent", "crazy-cat-lady", "dog-lover", "cat-lover",
        "pet-gift", "puppy", "kitten", "shelter", "furry-friend",
    ],
    "profession": [
        "work-humor", "office", "coworker", "boss-gift",
        "retirement", "work-life", "9-to-5", "corporate",
        "professional", "expert", "specialist", "skilled",
        "graduation-gift", "career-humor",
    ],
    "sarcasm": [
        "sarcastic-shirt", "sarcastic-gift", "eye-roll", "whatever",
        "savage", "unbothered", "zero-filter", "mood", "judging",
        "toxic", "shady", "extra", "over-it", "done",
    ],
    "seasonal": [
        "holiday-shirt", "festive", "celebration", "winter",
        "pumpkin", "spooky", "santa", "valentines", "new-year",
        "4th-of-july", "memorial-day", "labor-day", "harvest",
    ],
    "stacked": [
        "quote-shirt", "statement", "bold", "empowerment",
        "motivational-shirt", "word-art", "text-shirt", "slogan",
        "message", "expression", "declaration", "mantra",
    ],
    "stay": [
        "wanderlust", "explore", "free-spirit", "nomad",
        "travel-shirt", "outdoors", "nature-lover", "wild-child",
        "road-trip", "escape", "freedom", "journey",
    ],
}

# Fallback tags for niches not in the dictionary
DEFAULT_BACKFILL = [
    "gift-idea", "funny-shirt", "graphic-tee", "statement-shirt",
    "birthday-gift", "christmas-gift", "unisex", "men", "women",
    "humor", "quote-shirt", "casual", "streetwear", "pop-culture",
]


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def clean_tags(tags: list[str], niche: str) -> list[str]:
    """Remove junk tags, deduplicate, and backfill with niche tags."""
    # Step 1: Remove junk
    clean = []
    seen = set()
    for tag in tags:
        t = tag.strip()
        key = t.lower()
        if key in ALL_JUNK:
            continue
        if key in seen:
            continue
        seen.add(key)
        clean.append(t)

    # Step 2: Backfill to 15 tags
    backfill_pool = NICHE_BACKFILL.get(niche, DEFAULT_BACKFILL)
    for tag in backfill_pool:
        if len(clean) >= 15:
            break
        if tag.lower() not in seen:
            seen.add(tag.lower())
            clean.append(tag)

    # Step 3: If still short, use default backfill
    if len(clean) < 15:
        for tag in DEFAULT_BACKFILL:
            if len(clean) >= 15:
                break
            if tag.lower() not in seen:
                seen.add(tag.lower())
                clean.append(tag)

    return clean[:15]


def process_folder(folder: str, dry_run: bool) -> dict:
    """Process all JSON files in a folder. Returns stats."""
    folder_path = OUTPUT_DIR / folder
    if not folder_path.is_dir():
        print(f"Folder not found: {folder_path}")
        return {"total": 0, "modified": 0}

    total = 0
    modified = 0
    tags_removed_total = 0
    tags_added_total = 0

    for jf in sorted(folder_path.glob("*.json")):
        with open(jf) as f:
            meta = json.load(f)

        old_tags = meta.get("tags", [])
        niche = jf.stem.split("_")[0]
        new_tags = clean_tags(old_tags, niche)
        total += 1

        if old_tags != new_tags:
            modified += 1
            removed = set(t.lower() for t in old_tags) - set(t.lower() for t in new_tags)
            added = set(t.lower() for t in new_tags) - set(t.lower() for t in old_tags)
            tags_removed_total += len(removed)
            tags_added_total += len(added)

            if dry_run and modified <= 5:
                print(f"  {jf.name}:")
                print(f"    Before ({len(old_tags)}): {old_tags}")
                print(f"    After  ({len(new_tags)}): {new_tags}")
                if removed:
                    print(f"    Removed: {sorted(removed)}")
                if added:
                    print(f"    Added:   {sorted(added)}")
                print()

            if not dry_run:
                meta["tags"] = new_tags
                with open(jf, "w") as f:
                    json.dump(meta, f, indent=2)

    return {
        "total": total,
        "modified": modified,
        "tags_removed": tags_removed_total,
        "tags_added": tags_added_total,
    }


def main():
    parser = argparse.ArgumentParser(description="Clean up POD design tags")
    parser.add_argument("--folder", help="Only process this folder (e.g. tshirt)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without modifying")
    args = parser.parse_args()

    folders = [args.folder] if args.folder else ["tshirt", "sticker", "poster"]
    grand_total = 0
    grand_modified = 0
    grand_removed = 0
    grand_added = 0

    for folder in folders:
        folder_path = OUTPUT_DIR / folder
        if not folder_path.is_dir():
            continue
        print(f"{'[DRY RUN] ' if args.dry_run else ''}Processing {folder}/...")
        stats = process_folder(folder, args.dry_run)
        grand_total += stats["total"]
        grand_modified += stats["modified"]
        grand_removed += stats["tags_removed"]
        grand_added += stats["tags_added"]
        print(f"  {stats['total']} files, {stats['modified']} modified, "
              f"-{stats['tags_removed']} removed, +{stats['tags_added']} added")
        print()

    print(f"{'[DRY RUN] ' if args.dry_run else ''}=== Summary ===")
    print(f"  Total files:  {grand_total}")
    print(f"  Modified:     {grand_modified}")
    print(f"  Tags removed: {grand_removed}")
    print(f"  Tags added:   {grand_added}")
    if args.dry_run:
        print("\nRun without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
