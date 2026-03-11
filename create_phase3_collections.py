"""Create Shopify smart collections for Phase 3 landmarks.

Usage:
    python3 create_phase3_collections.py [--dry-run]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keychain_config import load_config as _load_keychain_config


# Phase 3 landmarks
PHASE3_LANDMARKS = [
    "acropolis_athens", "amalfi_coast", "antelope_canyon",
    "banaue_rice_terraces", "blue_mosque", "bora_bora", "borobudur",
    "burj_khalifa", "cappadocia", "chichen_itza", "djemaa_el_fna",
    "dubrovnik_walls", "duomo_florence", "easter_island",
    "golden_temple_amritsar", "great_barrier_reef", "gyeongbokgung",
    "halong_bay", "iguazu_falls", "lake_louise", "lalibela_churches",
    "li_river_guilin", "matterhorn", "meiji_shrine", "meteora",
    "monument_valley", "mysore_palace", "niagara_falls",
    "northern_lights_iceland", "petronas_towers", "potala_palace",
    "pyramids_giza", "rothenburg", "santorini", "serengeti",
    "seville_alcazar", "sheikh_zayed_mosque", "sigiriya", "sugarloaf_rio",
    "table_mountain", "terracotta_warriors", "tikal", "tongariro",
    "tower_of_london", "trolltunga", "uluru", "victoria_falls",
    "wadi_rum", "yellowstone", "zhangjiajie",
]


def slug_to_display(slug: str) -> str:
    """Convert underscore slug to display title, e.g. 'acropolis_athens' -> 'Acropolis Athens Art'."""
    return slug.replace("_", " ").title() + " Art"


def slug_to_rule_term(slug: str) -> str:
    """Convert underscore slug to the search term used in product title matching.

    E.g. 'acropolis_athens' -> 'Acropolis Athens'
    """
    return slug.replace("_", " ").title()


def main():
    dry_run = "--dry-run" in sys.argv

    config = _load_keychain_config("shopify")
    for key in ("shop_domain", "api_token", "api_version"):
        if key not in config:
            raise ValueError(f"Missing '{key}' in shopify config")

    base_url = (
        f"https://{config['shop_domain']}/admin/api/"
        f"{config.get('api_version', '2024-01')}"
    )
    session = requests.Session()
    session.headers.update({
        "X-Shopify-Access-Token": config["api_token"],
        "Content-Type": "application/json",
    })

    # --- Fetch existing smart collections ---
    print("Fetching existing smart collections...")
    existing_titles: set[str] = set()
    import re
    params: dict = {"limit": 250}
    while True:
        resp = session.get(f"{base_url}/smart_collections.json", params=params, timeout=30)
        if resp.status_code == 429:
            time.sleep(float(resp.headers.get("Retry-After", 2)))
            resp = session.get(f"{base_url}/smart_collections.json", params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        for c in data.get("smart_collections", []):
            existing_titles.add(c["title"].strip().lower())

        # Pagination
        link = resp.headers.get("Link", "")
        match = re.search(r'<([^>]+)>;\s*rel="next"', link)
        if not match:
            break
        info_match = re.search(r"page_info=([^&]+)", match.group(1))
        if not info_match:
            break
        params = {"limit": 250, "page_info": info_match.group(1)}

    print(f"Found {len(existing_titles)} existing smart collections.")

    # Known title overrides: some Phase 1/2 collections use different names
    TITLE_OVERRIDES = {
        "pyramids_giza": None,  # Already exists as "Pyramids of Giza Art"
    }

    # --- Create new collections ---
    created = []
    skipped = []
    failed = []

    for landmark in PHASE3_LANDMARKS:
        # Check for manual overrides (already exists under different name)
        if landmark in TITLE_OVERRIDES:
            skipped.append((landmark, slug_to_display(landmark), "already exists under different name"))
            print(f"  SKIP: {slug_to_display(landmark)} (already exists as different title)")
            continue

        title = slug_to_display(landmark)
        rule_term = slug_to_rule_term(landmark)

        if title.strip().lower() in existing_titles:
            skipped.append((landmark, title, "already exists"))
            print(f"  SKIP: {title} (already exists)")
            continue

        payload = {
            "smart_collection": {
                "title": title,
                "rules": [
                    {
                        "column": "title",
                        "relation": "contains",
                        "condition": rule_term,
                    }
                ],
                "published": True,
            }
        }

        if dry_run:
            print(f"  DRY RUN: Would create '{title}' (rule: title contains '{rule_term}')")
            created.append((landmark, title))
            continue

        resp = session.post(
            f"{base_url}/smart_collections.json",
            json=payload,
            timeout=30,
        )

        if resp.status_code == 429:
            retry_after = float(resp.headers.get("Retry-After", 2))
            print(f"  Rate limited, waiting {retry_after}s...")
            time.sleep(retry_after)
            resp = session.post(
                f"{base_url}/smart_collections.json",
                json=payload,
                timeout=30,
            )

        if resp.status_code in (200, 201):
            coll = resp.json().get("smart_collection", {})
            created.append((landmark, title))
            print(f"  CREATED: {title} (ID: {coll.get('id')})")
        else:
            failed.append((landmark, title, resp.status_code, resp.text[:200]))
            print(f"  FAILED: {title} — {resp.status_code}: {resp.text[:200]}")

        # Small delay to respect rate limits
        time.sleep(0.5)

    # --- Summary ---
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Created: {len(created)}")
    for lm, title in created:
        print(f"  + {title}")
    print(f"\nSkipped (already exist): {len(skipped)}")
    for lm, title, reason in skipped:
        print(f"  - {title} ({reason})")
    if failed:
        print(f"\nFailed: {len(failed)}")
        for lm, title, code, msg in failed:
            print(f"  ! {title} — HTTP {code}: {msg}")

    print(f"\nTotal Phase 3 landmarks: {len(PHASE3_LANDMARKS)}")


if __name__ == "__main__":
    main()
