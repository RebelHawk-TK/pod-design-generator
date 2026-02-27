#!/usr/bin/env python3
"""Generate a Google Shopping product feed from Shopify store data.

Usage:
    python3 generate_google_feed.py              # Generate feed
    python3 generate_google_feed.py --stats       # Generate and show stats
    python3 generate_google_feed.py --type poster  # Filter by product type
    python3 generate_google_feed.py --output /path/to/feed.xml
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from google_feed.shopify_products import fetch_all_products
from google_feed.feed_builder import build_feed

DEFAULT_OUTPUT = Path(__file__).parent / "feed" / "google_shopping_feed.xml"
PAGES_DIR = Path(__file__).parent / "docs" / "feed"
FEED_URL = "https://rebelhawk-tk.github.io/pod-design-generator/feed/google_shopping_feed.xml"


def main():
    parser = argparse.ArgumentParser(description="Generate Google Shopping XML feed")
    parser.add_argument(
        "--output", "-o",
        default=str(DEFAULT_OUTPUT),
        help=f"Output XML file path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--type", "-t",
        dest="product_type",
        help="Filter by product type (e.g., poster, tshirt)",
    )
    parser.add_argument(
        "--stats", "-s",
        action="store_true",
        help="Show feed statistics after generation",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Fetching products from Shopify...")
    products = fetch_all_products(product_type_filter=args.product_type)

    if not products:
        print("No products found.")
        sys.exit(1)

    print(f"Building feed for {len(products)} products...")
    stats = build_feed(products, str(output_path))
    print(f"Feed written to {output_path}")

    # Copy to GitHub Pages directory for hosting
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    pages_path = PAGES_DIR / "google_shopping_feed.xml"
    shutil.copy2(str(output_path), str(pages_path))
    print(f"Copied to {pages_path} (GitHub Pages)")

    if args.stats:
        print(f"\n--- Feed Statistics ---")
        print(f"Products:  {stats['product_count']}")
        print(f"Variants:  {stats['variant_count']}")
        print(f"Categories:")
        for cat, count in sorted(stats["categories"].items()):
            print(f"  {cat}: {count}")

    print(f"\nFeed URL: {FEED_URL}")
    print("Push to GitHub to update: git add docs/feed/ && git commit && git push")


if __name__ == "__main__":
    main()
