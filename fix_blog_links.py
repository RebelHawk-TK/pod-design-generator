#!/usr/bin/env python3
"""Fix broken links in all published Shopify blog posts.

Replaces:
1. Old myshopify domain with moderndesignconcept.com
2. Broken collection links (Phase 3 landmarks without collections) with store homepage
3. Wrong great-wave handle

Usage:
    python3 fix_blog_links.py --dry-run    # Preview changes
    python3 fix_blog_links.py              # Apply fixes
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from blog.shopify_blog import ShopifyBlogAPI

# ---------------------------------------------------------------------------
# Known-good collection handles (verified 200 on live site)
# ---------------------------------------------------------------------------

WORKING_COLLECTIONS = {
    # Styles
    "starry-night-collection",
    "the-great-wave-collection",
    "water-lilies-collection",
    "cafe-terrace-collection",
    "composition-vii-collection",
    "the-scream-collection",
    # Phase 1+2 landmarks (verified working)
    "eiffel-tower-art",
    "taj-mahal-art",
    "colosseum-art",
    "great-wall-art",
    "notre-dame-art",
    "neuschwanstein-art",
    "mount-fuji-art",
    "golden-gate-art",
    "sydney-opera-art",
    "santorini-art",
    "angkor-wat-art",
    "machu-picchu-art",
    "sagrada-familia-art",
    "parthenon-art",
    "stonehenge-art",
    "moai-art",
    "petra-art",
    "st-basils-art",
    "chichen-itza-art",
    "christ-redeemer-art",
    "hagia-sophia-art",
    "tower-of-pisa-art",
    "big-ben-art",
    "statue-of-liberty-art",
    "great-barrier-reef-art",
    "venice-grand-canal-art",
    "forbidden-city-art",
}

OLD_DOMAIN = "modern-design-concept-2.myshopify.com"
NEW_DOMAIN = "moderndesignconcept.com"
STORE_URL = f"https://{NEW_DOMAIN}"

# Wrong handle -> correct handle
HANDLE_FIXES = {
    "great-wave-collection": "the-great-wave-collection",
}


def fix_html(body_html: str) -> tuple[str, list[str]]:
    """Fix links in blog post HTML. Returns (fixed_html, list_of_changes)."""
    changes = []
    fixed = body_html

    # Fix 1: Replace old myshopify domain
    if OLD_DOMAIN in fixed:
        fixed = fixed.replace(OLD_DOMAIN, NEW_DOMAIN)
        changes.append(f"Replaced {OLD_DOMAIN} → {NEW_DOMAIN}")

    # Fix 2: Fix known wrong handles
    for old_handle, new_handle in HANDLE_FIXES.items():
        old_path = f"/collections/{old_handle}"
        new_path = f"/collections/{new_handle}"
        if old_path in fixed:
            fixed = fixed.replace(old_path, new_path)
            changes.append(f"Fixed handle: {old_handle} → {new_handle}")

    # Fix 3: Replace broken collection links with store homepage
    # Find all collection links
    collection_pattern = re.compile(
        r'href="https?://[^"]*?/collections/([^"]+)"'
    )
    for match in collection_pattern.finditer(fixed):
        handle = match.group(1)
        if handle not in WORKING_COLLECTIONS:
            old_url = match.group(0)
            # Replace with store homepage link
            new_url = f'href="{STORE_URL}"'
            fixed = fixed.replace(old_url, new_url, 1)
            changes.append(f"Broken collection → homepage: {handle}")

    return fixed, changes


def main():
    parser = argparse.ArgumentParser(description="Fix broken links in blog posts")
    parser.add_argument("--dry-run", action="store_true", help="Preview without updating")
    parser.add_argument("--limit", type=int, default=0, help="Limit articles to process")
    args = parser.parse_args()

    api = ShopifyBlogAPI()
    blog_id = api.get_or_create_blog("Art & Travel")

    print(f"Fetching all articles from blog {blog_id}...")
    articles = api.list_articles(blog_id)
    print(f"Found {len(articles)} articles\n")

    if args.limit:
        articles = articles[:args.limit]

    total_fixed = 0
    total_changes = 0
    domain_fixes = 0
    handle_fixes = 0
    broken_fixes = 0

    for i, article in enumerate(articles, 1):
        title = article["title"]
        article_id = article["id"]
        body_html = article.get("body_html", "")

        if not body_html:
            continue

        fixed_html, changes = fix_html(body_html)

        if not changes:
            continue

        total_fixed += 1
        total_changes += len(changes)

        for c in changes:
            if "Replaced" in c:
                domain_fixes += 1
            elif "Fixed handle" in c:
                handle_fixes += 1
            elif "Broken collection" in c:
                broken_fixes += 1

        if args.dry_run:
            print(f"[{i}/{len(articles)}] {title}")
            for c in changes:
                print(f"  {c}")
            if i <= 3:  # Show first 3 in detail
                print()
        else:
            try:
                api.update_article(blog_id, article_id, body_html=fixed_html)
                print(f"[{i}/{len(articles)}] Updated: {title} ({len(changes)} fixes)")
                # Rate limit: Shopify allows ~2 req/sec
                time.sleep(0.5)
            except Exception as e:
                print(f"[{i}/{len(articles)}] FAILED: {title} — {e}")

    print(f"\n=== Summary ===")
    print(f"Articles scanned: {len(articles)}")
    print(f"Articles {'needing' if args.dry_run else 'with'} fixes: {total_fixed}")
    print(f"Total changes: {total_changes}")
    print(f"  Domain fixes: {domain_fixes}")
    print(f"  Handle fixes: {handle_fixes}")
    print(f"  Broken → homepage: {broken_fixes}")

    if args.dry_run:
        print(f"\nDry run — no changes made. Run without --dry-run to apply.")


if __name__ == "__main__":
    main()
