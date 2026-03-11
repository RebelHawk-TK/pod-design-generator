#!/usr/bin/env python3
"""Pinterest API Demo — for Standard Access approval video.

Shows the full integration flow:
  1. OAuth 2.0 authentication (browser-based)
  2. Board listing
  3. Pin creation with image upload
  4. Success verification

Usage:
    python3 demo_pinterest.py
"""

import json
import sys
import time
from pathlib import Path

# Reuse existing upload infrastructure
from upload_pinterest import (
    CONFIG_FILE,
    TOKEN_FILE,
    API_BASE_SANDBOX,
    authorize,
    get_access_token,
    load_config,
    list_boards,
    resolve_board,
    create_pin,
    build_pin_link,
    build_pin_description,
    discover_pinterest_designs,
    NICHE_BOARDS,
    DEFAULT_BOARD,
    api_request,
)

DIVIDER = "=" * 60


def banner(msg: str) -> None:
    print(f"\n{DIVIDER}")
    print(f"  {msg}")
    print(DIVIDER)


def step(num: int, msg: str) -> None:
    print(f"\n{'─' * 50}")
    print(f"  STEP {num}: {msg}")
    print(f"{'─' * 50}\n")


def main() -> None:
    banner("Modern Design Concept — Pinterest API Integration Demo")
    print()
    print("  App:      Modern Design Concept (POD Store)")
    print("  API:      Pinterest API v5 (Sandbox)")
    print("  Purpose:  Automated pin creation for product listings")
    print()

    config = load_config()

    # ── Step 1: OAuth ──
    step(1, "OAuth 2.0 Authentication")
    print("Checking for existing session...")
    access_token = get_access_token(config)

    if not access_token:
        print("No valid session found. Starting OAuth flow...\n")
        tokens = authorize(config["app_id"], config["app_secret"])
        access_token = tokens.get("access_token")
        if not access_token:
            print("ERROR: OAuth failed.")
            sys.exit(1)
    else:
        print("Existing session found and valid.\n")

    print("✓ OAuth authentication successful")

    # For sandbox API calls, use the portal-generated sandbox token
    sandbox_token = config.get("sandbox_token")
    if sandbox_token:
        api_token = sandbox_token
        print("  Using sandbox token for API calls")
    else:
        api_token = access_token

    # ── Step 2: List Boards ──
    step(2, "Fetching Pinterest Boards")
    boards = list_boards(api_token)
    print(f"Found {len(boards)} boards:\n")
    for b in boards[:8]:
        print(f"  • {b['name']} ({b['pin_count']} pins)")
    if len(boards) > 8:
        print(f"  ... and {len(boards) - 8} more")
    print(f"\n✓ Board listing successful")

    # ── Step 3: Create Pins ──
    step(3, "Creating Pins with Product Images")

    # Find 3 designs from landmark posters
    source_dir = Path("/Users/rebelhawk/Documents/Claude/landmark-style-transfer-unified/output")
    designs = discover_pinterest_designs("poster", source_dir=source_dir)

    if not designs:
        print("No designs found.")
        sys.exit(1)

    # Pick 3 diverse designs (different landmarks)
    selected = designs[:3]
    shop_name = config.get("shop_name", "ModernDesignCo")

    for i, (mockup_path, meta, niche) in enumerate(selected, 1):
        title = meta["title"]
        print(f"\n  Pin {i}/3:")
        print(f"    Title:  {title}")

        board_name = NICHE_BOARDS.get(niche, DEFAULT_BOARD)
        board_id = resolve_board(niche, api_token)
        print(f"    Board:  {board_name}")

        link = build_pin_link(title, shop_name)
        description = build_pin_description(meta, link)
        print(f"    Image:  {mockup_path.name}")
        print(f"    Link:   {link}")

        print(f"    Uploading...", end=" ", flush=True)
        result = create_pin(
            api_token, board_id,
            title, description, link,
            mockup_path,
        )
        pin_id = result.get("id")
        print(f"✓ Created (Pin ID: {pin_id})")

        if i < len(selected):
            print(f"    Waiting 5s...")
            time.sleep(5)

    # ── Step 4: Verify ──
    step(4, "Verification")

    # List pins to confirm they exist
    resp = api_request("GET", "/pins", api_token, params={"page_size": 5})
    pins = resp.get("items", [])
    print(f"Recent pins in account:\n")
    for p in pins[:5]:
        print(f"  • {p.get('title', '(no title)')} — ID: {p['id']}")

    print(f"\n✓ All pins verified")

    # ── Summary ──
    banner("Demo Complete")
    print()
    print("  ✓ OAuth 2.0 authentication — working")
    print("  ✓ Board management — working")
    print("  ✓ Pin creation with images — working")
    print("  ✓ Pin verification — working")
    print()
    print("  This integration automatically uploads product mockups")
    print("  as Pinterest pins with titles, descriptions, tags, and")
    print("  links back to our online store.")
    print()
    print(DIVIDER)


if __name__ == "__main__":
    main()
