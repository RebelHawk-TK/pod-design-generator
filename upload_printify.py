#!/usr/bin/env python3
"""Printify API upload script for POD designs.

Uploads design images and creates products on Printify via REST API.
Supports t-shirts, posters, and stickers with configurable pricing.

Setup:
    1. Create a Printify account and store
    2. Generate an API token (Account → Connections → API)
    3. Save token in .printify_config.json (auto-created on first run)

Usage:
    python3 upload_printify.py --folder tshirt --limit 1       # Test one product
    python3 upload_printify.py --folder tshirt --dry-run        # Preview
    python3 upload_printify.py --folder tshirt --limit 50       # Upload batch
    python3 upload_printify.py --folder poster                  # Upload all posters
    python3 upload_printify.py --folder sticker --retry-failed  # Retry failures
    python3 upload_printify.py --folder tshirt --publish        # Create + publish
    python3 upload_printify.py --source-dir /path/to/designs --folder poster
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

from upload_common import (
    discover_designs,
    jittered_delay,
    load_tracker,
    save_tracker,
    tracker_key,
    CONSECUTIVE_FAILURE_LIMIT,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent

from keychain_config import load_config as _load_keychain_config
TRACKER_FILE = SCRIPT_DIR / "uploaded_printify.json"

DEFAULT_DELAY = 5  # seconds between API calls (no browser, can be fast)

# Product blueprints and print providers
PRODUCT_CONFIG = {
    "tshirt": {
        "blueprint_id": 6,           # Unisex Heavy Cotton Tee
        "print_provider_id": 103,    # Stacked Commerce
        "position": "front",
        # Popular colors with variant IDs (S through 3XL)
        "variant_groups": {
            "Black":        [11872, 11873, 11874, 11875, 11876, 11877],
            "White":        [12124, 12125, 12126, 12127, 12128, 12129],
            "Navy":         [11986, 11987, 11988, 11989, 11990, 11991],
            "Dark Heather": [11902, 11903, 11904, 11905, 11906, 11907],
            "Sport Grey":   [12070, 12071, 12072, 12073, 12074, 12075],
            "Royal":        [12022, 12023, 12024, 12025, 12026, 12027],
            "Red":          [12028, 12029, 12030, 12031, 12032, 12033],
            "Sand":         [12052, 12053, 12054, 12055, 12056, 12057],
        },
        "default_price": 2499,  # $24.99 in cents
        "default_colors": ["Black", "White", "Navy", "Dark Heather", "Sport Grey"],
    },
    "poster": {
        "blueprint_id": 282,         # Matte Vertical Posters
        "print_provider_id": 99,     # Printify Choice
        "position": "front",
        "variant_groups": {
            "8x10":   [114557],
            "11x14":  [43135],
            "12x16":  [101110],
            "12x18":  [43138],
            "16x20":  [43141],
            "18x24":  [43144],
            "24x36":  [43150],
        },
        "default_price": 1999,  # $19.99
        "default_sizes": ["12x16", "16x20", "18x24", "24x36"],
    },
    "sticker": {
        "blueprint_id": 600,         # Die-Cut Stickers
        "print_provider_id": 73,     # Printed Simply
        "position": "front",
        "variant_groups": {
            "2x2": [72006],
            "3x3": [72007],
            "4x4": [72008],
            "5x5": [72009],
            "6x6": [72010],
        },
        "default_price": 499,  # $4.99
        "default_sizes": ["3x3", "4x4", "5x5"],
    },
}


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def load_config() -> dict:
    return _load_keychain_config("printify")


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------

class PrintifyAPI:
    """Thin wrapper around the Printify REST API v1."""

    def __init__(self, api_token: str, shop_id: int):
        self.api_token = api_token
        self.shop_id = shop_id
        self.base_url = "https://api.printify.com/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        })

    def _request(self, method: str, endpoint: str, json_data: dict | None = None) -> dict:
        url = f"{self.base_url}{endpoint}"
        resp = self.session.request(method, url, json=json_data, timeout=120)

        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 60))
            print(f"  Rate limited. Waiting {retry_after}s...")
            time.sleep(retry_after)
            resp = self.session.request(method, url, json=json_data, timeout=120)

        if resp.status_code not in (200, 201):
            raise Exception(f"API {resp.status_code}: {resp.text[:500]}")

        return resp.json()

    def upload_image(self, file_name: str, image_path: Path) -> dict:
        """Upload an image to Printify. Returns {"id": "...", ...}."""
        image_b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
        return self._request("POST", "/uploads/images.json", {
            "file_name": file_name,
            "contents": image_b64,
        })

    def create_product(self, product_data: dict) -> dict:
        """Create a product in the shop."""
        return self._request(
            "POST",
            f"/shops/{self.shop_id}/products.json",
            product_data,
        )

    def publish_product(self, product_id: str) -> dict:
        """Publish a product to the connected sales channel."""
        return self._request(
            "POST",
            f"/shops/{self.shop_id}/products/{product_id}/publish.json",
            {
                "title": True,
                "description": True,
                "images": True,
                "variants": True,
                "tags": True,
            },
        )

    def list_products(self, page: int = 1, limit: int = 50) -> dict:
        """List products in the shop."""
        return self._request(
            "GET",
            f"/shops/{self.shop_id}/products.json?page={page}&limit={limit}",
        )


# ---------------------------------------------------------------------------
# Product builder
# ---------------------------------------------------------------------------

def build_product_data(
    config: dict,
    folder: str,
    image_id: str,
    metadata: dict,
    price_override: int | None = None,
    colors: list[str] | None = None,
    sizes: list[str] | None = None,
) -> dict:
    """Build a Printify product creation payload."""
    product_cfg = PRODUCT_CONFIG[folder]
    blueprint_id = product_cfg["blueprint_id"]
    provider_id = product_cfg["print_provider_id"]
    position = product_cfg["position"]
    price = price_override or product_cfg["default_price"]

    # Determine which variants to enable
    variant_groups = product_cfg["variant_groups"]

    if folder == "tshirt":
        selected = colors or product_cfg.get("default_colors", list(variant_groups.keys()))
        variant_ids = []
        for color in selected:
            if color in variant_groups:
                variant_ids.extend(variant_groups[color])
    else:
        selected = sizes or product_cfg.get("default_sizes", list(variant_groups.keys()))
        variant_ids = []
        for size in selected:
            if size in variant_groups:
                variant_ids.extend(variant_groups[size])

    # Build variants array with pricing
    variants = [
        {"id": vid, "price": price, "is_enabled": True}
        for vid in variant_ids
    ]

    # Build print areas
    print_areas = [
        {
            "variant_ids": variant_ids,
            "placeholders": [
                {
                    "position": position,
                    "images": [
                        {
                            "id": image_id,
                            "x": 0.5,
                            "y": 0.5,
                            "scale": 1,
                            "angle": 0,
                        }
                    ],
                }
            ],
        }
    ]

    # Tags (Printify max 13 tags)
    tags = metadata.get("tags", [])[:13]

    return {
        "title": metadata["title"],
        "description": metadata.get("description", ""),
        "blueprint_id": blueprint_id,
        "print_provider_id": provider_id,
        "variants": variants,
        "print_areas": print_areas,
        "tags": tags,
    }


# ---------------------------------------------------------------------------
# Upload single design
# ---------------------------------------------------------------------------

def upload_one_design(
    api: PrintifyAPI,
    folder: str,
    png_path: Path,
    metadata: dict,
    price_override: int | None = None,
    colors: list[str] | None = None,
    sizes: list[str] | None = None,
    publish: bool = False,
) -> dict:
    """Upload image, create product, optionally publish. Returns product dict."""
    # Step 1: Upload image
    print(f"  Uploading image: {png_path.name}")
    image_result = api.upload_image(png_path.name, png_path)
    image_id = image_result["id"]
    print(f"  Image ID: {image_id}")

    # Step 2: Create product
    product_data = build_product_data(
        load_config(), folder, image_id, metadata,
        price_override=price_override, colors=colors, sizes=sizes,
    )
    print(f"  Creating product: {metadata['title']}")
    product = api.create_product(product_data)
    product_id = product["id"]
    print(f"  Product ID: {product_id}")

    # Step 3: Optionally publish
    if publish:
        print(f"  Publishing product...")
        api.publish_product(product_id)
        print(f"  Published!")

    return product


# ---------------------------------------------------------------------------
# Main upload loop
# ---------------------------------------------------------------------------

def run_printify_upload(args: argparse.Namespace) -> None:
    """Main Printify upload flow."""
    config = load_config()
    api = PrintifyAPI(config["api_token"], config["shop_id"])

    folder = args.folder
    if folder not in PRODUCT_CONFIG:
        print(f"Error: unsupported folder '{folder}'. Use: {', '.join(PRODUCT_CONFIG.keys())}")
        sys.exit(1)

    # Parse optional colors/sizes
    colors = [c.strip() for c in args.colors.split(",")] if args.colors else None
    sizes = [s.strip() for s in args.sizes.split(",")] if args.sizes else None
    price_override = int(args.price * 100) if args.price else None

    # Discover designs
    source_dir = Path(args.source_dir) if args.source_dir else None
    designs = discover_designs(folder, shuffle_niches=args.shuffle, source_dir=source_dir)

    if not designs:
        location = str(source_dir / folder) if source_dir else f"output/{folder}/"
        print(f"No designs found in {location}")
        return

    location = str(source_dir / folder) if source_dir else f"output/{folder}/"
    print(f"Found {len(designs)} designs in {location}")

    # Load tracker and filter
    tracker = load_tracker(TRACKER_FILE)
    to_upload = []
    for png_path, meta in designs:
        key = tracker_key(folder, png_path, source_dir=source_dir)
        # Prefix with printify: for tracker isolation
        pf_key = f"printify:{key}"
        entry = tracker.get(pf_key, {})
        status = entry.get("status")

        if args.retry_failed and status == "failed":
            to_upload.append((png_path, meta, pf_key))
        elif status == "success":
            continue
        elif not args.retry_failed:
            to_upload.append((png_path, meta, pf_key))

    if not to_upload:
        print("No designs to upload (all already uploaded or no failures to retry).")
        return

    if args.limit and args.limit > 0:
        to_upload = to_upload[:args.limit]

    product_type = PRODUCT_CONFIG[folder]
    print(f"\nProduct type: Blueprint {product_type['blueprint_id']} / Provider {product_type['print_provider_id']}")
    print(f"Price: ${(price_override or product_type['default_price']) / 100:.2f}")
    print(f"Publish: {'yes' if args.publish else 'no (draft)'}")
    print(f"Will {'preview' if args.dry_run else 'upload'} {len(to_upload)} designs\n")

    # Dry run
    if args.dry_run:
        for i, (png_path, meta, key) in enumerate(to_upload, 1):
            print(f"  [{i}] {key}")
            print(f"       Title: {meta['title']}")
            print(f"       Tags:  {', '.join(meta.get('tags', [])[:8])}")
            print()
        print("Dry run complete — no products created.")
        return

    # Upload loop
    consecutive_failures = 0
    uploaded_count = 0
    session_start = time.time()

    for i, (png_path, meta, key) in enumerate(to_upload, 1):
        print(f"\n[{i}/{len(to_upload)}] {key}")

        try:
            product = upload_one_design(
                api, folder, png_path, meta,
                price_override=price_override,
                colors=colors, sizes=sizes,
                publish=args.publish,
            )

            tracker[key] = {
                "status": "success",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "product_id": product["id"],
                "error": None,
            }
            save_tracker(tracker, TRACKER_FILE)
            consecutive_failures = 0
            uploaded_count += 1
            print(f"  -> Success")

        except Exception as e:
            tracker[key] = {
                "status": "failed",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error": str(e),
            }
            save_tracker(tracker, TRACKER_FILE)
            consecutive_failures += 1
            print(f"  -> Failed: {e}")

        # Circuit breaker
        if consecutive_failures >= CONSECUTIVE_FAILURE_LIMIT:
            print(f"\n=== {CONSECUTIVE_FAILURE_LIMIT} consecutive failures — stopping ===")
            break

        # Progress stats every 10 uploads
        if uploaded_count > 0 and uploaded_count % 10 == 0:
            elapsed = time.time() - session_start
            rate = uploaded_count / (elapsed / 3600)
            remaining = len(to_upload) - i
            if rate > 0:
                eta_min = (remaining / rate) * 60
                print(f"\n  --- Progress: {uploaded_count}/{len(to_upload)} | {rate:.1f}/hr | ~{eta_min:.0f} min remaining ---")

        # Delay between uploads
        if i < len(to_upload):
            wait_time = jittered_delay(args.delay)
            print(f"  Waiting {wait_time:.0f}s...")
            time.sleep(wait_time)

    # Summary
    elapsed = time.time() - session_start
    print(f"\n=== Printify upload session complete ===")
    print(f"  Uploaded: {uploaded_count}/{len(to_upload)}")
    if elapsed > 0 and uploaded_count > 0:
        rate = uploaded_count / (elapsed / 3600)
        print(f"  Rate:     {rate:.1f} products/hour")
        print(f"  Duration: {elapsed / 60:.1f} minutes")
    failed = sum(1 for _, _, k in to_upload if tracker.get(k, {}).get("status") == "failed")
    if failed:
        print(f"  Failed:   {failed}")
        print(f"  Re-run with --retry-failed to retry")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upload POD designs to Printify via REST API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python3 %(prog)s --folder tshirt --limit 1           # Test one product
  python3 %(prog)s --folder tshirt --dry-run            # Preview
  python3 %(prog)s --folder tshirt --limit 50           # Upload batch
  python3 %(prog)s --folder poster --publish            # Create + publish posters
  python3 %(prog)s --folder sticker --retry-failed      # Retry failures
  python3 %(prog)s --folder tshirt --price 29.99        # Custom price
  python3 %(prog)s --folder tshirt --colors "Black,White,Navy"
  python3 %(prog)s --source-dir /path/to/designs --folder poster
""",
    )
    parser.add_argument(
        "--folder", required=True,
        help="Product type to upload (tshirt, poster, sticker)",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Max products to create (0 = all)",
    )
    parser.add_argument(
        "--delay", type=float, default=DEFAULT_DELAY,
        help=f"Seconds between uploads (default: {DEFAULT_DELAY})",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview without uploading",
    )
    parser.add_argument(
        "--retry-failed", action="store_true",
        help="Only retry previously failed uploads",
    )
    parser.add_argument(
        "--shuffle", action="store_true",
        help="Interleave niches for diverse ordering",
    )
    parser.add_argument(
        "--publish", action="store_true",
        help="Publish products after creation (default: draft only)",
    )
    parser.add_argument(
        "--price", type=float, default=0,
        help="Override retail price in dollars (e.g., 29.99)",
    )
    parser.add_argument(
        "--colors",
        help="Comma-separated t-shirt colors (e.g., 'Black,White,Navy')",
    )
    parser.add_argument(
        "--sizes",
        help="Comma-separated poster/sticker sizes (e.g., '16x20,18x24,24x36')",
    )
    parser.add_argument(
        "--source-dir",
        help="External image source directory (PNG+JSON pairs in source-dir/folder/)",
    )
    args = parser.parse_args()

    if args.limit == 0:
        args.limit = None

    run_printify_upload(args)


if __name__ == "__main__":
    main()
