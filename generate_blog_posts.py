#!/usr/bin/env python3
"""Generate SEO-optimized blog posts for landmark + art style combinations.

Usage:
    # Preview a single combo as local HTML
    python3 generate_blog_posts.py --landmark eiffel_tower --style starry_night --preview

    # Preview all 150 posts
    python3 generate_blog_posts.py --preview

    # Upload to Shopify (published)
    python3 generate_blog_posts.py --upload

    # Upload as drafts
    python3 generate_blog_posts.py --upload --draft

    # Show status
    python3 generate_blog_posts.py --status

    # Publish next batch of 3 drafts
    python3 generate_blog_posts.py --publish-batch

    # Publish a custom number of drafts
    python3 generate_blog_posts.py --publish-batch 5
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, date
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TRACKER_PATH = SCRIPT_DIR / "uploaded_blog_posts.json"
OUTPUT_DIR = SCRIPT_DIR / "blog" / "output"


def load_tracker() -> dict:
    if TRACKER_PATH.exists():
        return json.loads(TRACKER_PATH.read_text())
    return {}


def save_tracker(tracker: dict) -> None:
    TRACKER_PATH.write_text(json.dumps(tracker, indent=2))


def tracker_key(post: dict) -> str:
    return f"{post['landmark_key']}/{post['style_key']}"


def cmd_preview(args: argparse.Namespace) -> None:
    """Generate blog posts as local HTML files."""
    from blog.generator import generate_all_posts

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    count = 0
    for post in generate_all_posts(args.landmark, args.style):
        filename = f"{post['slug']}.html"
        filepath = OUTPUT_DIR / filename

        # Wrap in a minimal HTML document for browser preview
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="description" content="{post['summary']}">
<title>{post['title']}</title>
<style>
  body {{ max-width: 720px; margin: 2em auto; padding: 0 1em; font-family: Georgia, serif; line-height: 1.7; color: #2C2420; }}
  h2 {{ color: #8B6B4A; }}
  h3 {{ color: #7A8B6F; }}
  a {{ color: #C4944A; }}
  .meta {{ color: #888; font-size: 0.9em; margin-bottom: 2em; }}
</style>
</head>
<body>
<div class="meta">
<strong>Tags:</strong> {post['tags']}<br>
<strong>Slug:</strong> {post['slug']}<br>
<strong>Meta description ({len(post['summary'])} chars):</strong> {post['summary']}
</div>
{post['body_html']}
</body>
</html>"""

        filepath.write_text(html)
        count += 1
        print(f"  [{count}] {filename}")

    print(f"\nGenerated {count} posts in {OUTPUT_DIR}/")


def cmd_upload(args: argparse.Namespace) -> None:
    """Upload blog posts to Shopify."""
    try:
        from blog.shopify_blog import ShopifyBlogAPI
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Create .shopify_config.json with shop_domain, api_token, api_version")
        sys.exit(1)

    from blog.generator import generate_all_posts

    tracker = load_tracker()
    api = ShopifyBlogAPI()
    blog_id = api.get_or_create_blog("Art & Travel")

    published = not args.draft
    mode = "draft" if args.draft else "published"
    print(f"\nUploading as {mode} to blog id {blog_id}...\n")

    uploaded = 0
    skipped = 0
    failed = 0

    for post in generate_all_posts(args.landmark, args.style):
        key = tracker_key(post)

        if key in tracker and tracker[key].get("status") == "success":
            skipped += 1
            continue

        try:
            article = api.create_article(
                blog_id=blog_id,
                title=post["title"],
                body_html=post["body_html"],
                tags=post["tags"],
                summary=post["summary"],
                published=published,
            )
            tracker[key] = {
                "status": "success",
                "article_id": article["id"],
                "title": post["title"],
                "uploaded_at": datetime.now().isoformat(),
            }
            uploaded += 1
            # Small delay to avoid rate limits
            time.sleep(0.5)
        except Exception as e:
            tracker[key] = {
                "status": "failed",
                "error": str(e),
                "title": post["title"],
                "uploaded_at": datetime.now().isoformat(),
            }
            failed += 1
            print(f"  FAILED: {post['title']} — {e}")

        save_tracker(tracker)

    print(f"\nDone: {uploaded} uploaded, {skipped} skipped, {failed} failed")


def cmd_publish_batch(args: argparse.Namespace) -> None:
    """Publish the next N draft articles on the Shopify blog."""
    try:
        from blog.shopify_blog import ShopifyBlogAPI
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Check if today is a publish day (Mon=0, Wed=2, Fri=4)
    today = date.today()
    publish_days = {0: "Monday", 2: "Wednesday", 4: "Friday"}
    if today.weekday() not in publish_days and not args.force:
        day_name = today.strftime("%A")
        print(f"Today is {day_name} — not a publish day (Mon/Wed/Fri).")
        print("Use --force to publish anyway.")
        return

    batch_size = args.publish_batch
    api = ShopifyBlogAPI()
    blog_id = api.get_or_create_blog("Art & Travel")

    # Get all draft articles
    all_articles = api.list_articles(blog_id)
    drafts = [a for a in all_articles if not a.get("published_at")]

    if not drafts:
        print("No draft articles to publish.")
        return

    # Sort by ID (oldest first) for consistent ordering
    drafts.sort(key=lambda a: a["id"])

    to_publish = drafts[:batch_size]
    print(f"Publishing {len(to_publish)} of {len(drafts)} drafts...\n")

    published = 0
    for article in to_publish:
        try:
            api.update_article(blog_id, article["id"], published=True)
            print(f"  Published: {article['title']}")
            published += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  FAILED: {article['title']} — {e}")

    remaining = len(drafts) - published
    print(f"\nDone: {published} published, {remaining} drafts remaining")
    if remaining > 0:
        weeks_left = remaining / 3
        print(f"At 3/week (Mon/Wed/Fri), remaining drafts will take ~{weeks_left:.0f} weeks")


def cmd_status(args: argparse.Namespace) -> None:
    """Show status of generated/uploaded blog posts."""
    from blog.data.landmarks import LANDMARKS
    from blog.data.styles import STYLES

    total_possible = len(LANDMARKS) * len(STYLES)
    tracker = load_tracker()

    success = sum(1 for v in tracker.values() if v.get("status") == "success")
    failed = sum(1 for v in tracker.values() if v.get("status") == "failed")
    remaining = total_possible - success

    print(f"Blog Post Status")
    print(f"{'=' * 40}")
    print(f"Total combinations:  {total_possible}")
    print(f"Uploaded (success):  {success}")
    print(f"Failed:              {failed}")
    print(f"Remaining:           {remaining}")

    # Check preview files
    if OUTPUT_DIR.exists():
        preview_count = len(list(OUTPUT_DIR.glob("*.html")))
        print(f"Preview files:       {preview_count}")

    if failed > 0:
        print(f"\nFailed posts:")
        for key, val in tracker.items():
            if val.get("status") == "failed":
                print(f"  {key}: {val.get('error', 'unknown')}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate SEO blog posts for landmark art prints"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Generate HTML files locally (no upload)",
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload posts to Shopify",
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Upload as drafts (unpublished)",
    )
    parser.add_argument(
        "--landmark",
        type=str,
        default=None,
        help="Filter to a single landmark (e.g., eiffel_tower)",
    )
    parser.add_argument(
        "--style",
        type=str,
        default=None,
        help="Filter to a single art style (e.g., starry_night)",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show upload status",
    )
    parser.add_argument(
        "--publish-batch",
        type=int,
        nargs="?",
        const=1,
        default=None,
        metavar="N",
        help="Publish next N drafts (default: 1). Only runs on Mon/Wed/Fri unless --force",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Bypass day-of-week check for --publish-batch",
    )

    args = parser.parse_args()

    if args.status:
        cmd_status(args)
    elif args.publish_batch is not None:
        cmd_publish_batch(args)
    elif args.preview:
        cmd_preview(args)
    elif args.upload:
        cmd_upload(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
