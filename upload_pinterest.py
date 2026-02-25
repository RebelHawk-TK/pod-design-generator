#!/usr/bin/env python3
"""Pinterest auto-upload script using the Pinterest API v5.

Uploads product mockup images as pins with metadata from paired JSON files.
Uses OAuth 2.0 for authentication (one-time browser login, then auto-refresh).
Pins are paced conservatively to avoid account suspension.

Setup:
    1. Create a Pinterest Business account
    2. Create a Pinterest app at developers.pinterest.com
    3. First run will open browser for OAuth login

Usage:
    python3 upload_pinterest.py --folder tshirt --limit 1       # Test one pin
    python3 upload_pinterest.py --folder tshirt --dry-run        # Preview
    python3 upload_pinterest.py --folder tshirt --limit 10       # Upload batch
    python3 upload_pinterest.py --folder tshirt --retry-failed   # Retry failures
    python3 upload_pinterest.py --setup-boards                   # Create boards only
"""

from __future__ import annotations

import argparse
import base64
import http.server
import json
import random
import sys
import threading
import time
import urllib.parse
import webbrowser
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

from upload_common import (
    load_tracker,
    save_tracker,
    jittered_delay,
    CONSECUTIVE_FAILURE_LIMIT,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).parent / "output"
MOCKUP_DIR = OUTPUT_DIR / "mockups"
TRACKER_FILE = Path(__file__).parent / "uploaded_pinterest.json"
CONFIG_FILE = Path(__file__).parent / ".pinterest_config.json"
TOKEN_FILE = Path(__file__).parent / ".pinterest_session" / "tokens.json"
BOARD_CACHE_FILE = Path(__file__).parent / ".pinterest_boards.json"

# Pinterest API
API_BASE = "https://api.pinterest.com/v5"
OAUTH_URL = "https://api.pinterest.com/oauth/"
TOKEN_URL = "https://api.pinterest.com/v5/oauth/token"
REDIRECT_URI = "http://localhost:9876/callback"
SCOPES = "boards:read,boards:write,pins:read,pins:write"

# Pacing — conservative to avoid suspension
PINTEREST_DEFAULT_DELAY = 240      # 4 minutes between pins
PINTEREST_DAILY_LIMIT = 10         # trial tier limit
PINTEREST_BREAK_INTERVAL = 10      # break after every 10 pins
PINTEREST_BREAK_RANGE = (900, 1800)  # 15-30 minute break

# Link template
DEFAULT_SHOP_NAME = "ModernDesignCo"

# Board configuration per niche
NICHE_BOARDS = {
    "coffee":       "Coffee Lover T-Shirts & Gifts",
    "dad":          "Dad Jokes & Father's Day Gifts",
    "drinking":     "Drinking Humor T-Shirts & Gifts",
    "fitness":      "Gym & Fitness Motivation Shirts",
    "fridge":       "Funny Fridge Magnets & Kitchen Decor",
    "funny":        "Funny T-Shirts & Sarcastic Gifts",
    "gaming":       "Gamer T-Shirts & Gifts",
    "hobby":        "Hobby & Craft Lover Shirts",
    "hustle":       "Hustle & Entrepreneur Motivation",
    "introvert":    "Introvert Life T-Shirts & Gifts",
    "mom":          "Mom Life T-Shirts & Gifts",
    "motivational": "Motivational & Inspirational Quotes",
    "pets":         "Pet Lover T-Shirts & Gifts",
    "profession":   "Work & Career Humor Shirts",
    "sarcasm":      "Sarcastic T-Shirts & Gifts",
    "seasonal":     "Holiday & Seasonal T-Shirts",
    "stacked":      "Quote T-Shirts & Statement Tees",
    "stay":         "Travel & Adventure T-Shirts",
}
DEFAULT_BOARD = "Print-on-Demand Designs"


# ---------------------------------------------------------------------------
# Config management
# ---------------------------------------------------------------------------

def load_config() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {}


def save_config(config: dict) -> None:
    CONFIG_FILE.write_text(json.dumps(config, indent=2) + "\n")
    CONFIG_FILE.chmod(0o600)


# ---------------------------------------------------------------------------
# OAuth 2.0
# ---------------------------------------------------------------------------

_auth_code_result = {"code": None}


class _OAuthHandler(http.server.BaseHTTPRequestHandler):
    """Handle the OAuth redirect callback."""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            _auth_code_result["code"] = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h2>Authorization successful!</h2>"
                b"<p>You can close this window and return to the terminal.</p>"
                b"</body></html>"
            )
        else:
            self.send_response(400)
            self.end_headers()
            error = params.get("error", ["unknown"])[0]
            self.wfile.write(f"Error: {error}".encode())

    def log_message(self, format, *args):
        pass  # suppress HTTP logs


def authorize(app_id: str, app_secret: str) -> dict:
    """Run the full OAuth 2.0 flow. Returns token dict."""
    state = str(random.randint(100000, 999999))

    auth_url = (
        f"{OAUTH_URL}?response_type=code"
        f"&client_id={app_id}"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
        f"&scope={SCOPES}"
        f"&state={state}"
    )

    # Start local server to catch the redirect
    server = http.server.HTTPServer(("localhost", 9876), _OAuthHandler)
    server_thread = threading.Thread(target=server.handle_request, daemon=True)
    server_thread.start()

    print("\nOpening browser for Pinterest authorization...")
    print(f"  If the browser doesn't open, visit:\n  {auth_url}\n")
    webbrowser.open(auth_url)

    # Wait for the callback
    server_thread.join(timeout=120)
    server.server_close()

    code = _auth_code_result["code"]
    if not code:
        print("ERROR: Did not receive authorization code.")
        sys.exit(1)

    # Exchange code for tokens
    print("Exchanging authorization code for tokens...")
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        auth=(app_id, app_secret),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if resp.status_code != 200:
        print(f"ERROR: Token exchange failed ({resp.status_code}): {resp.text}")
        sys.exit(1)

    tokens = resp.json()
    tokens["obtained_at"] = time.time()
    _save_tokens(tokens)
    print("Authorization successful!")
    return tokens


def refresh_access_token(app_id: str, app_secret: str, refresh_token: str) -> dict:
    """Use refresh token to get a new access token."""
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        auth=(app_id, app_secret),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if resp.status_code != 200:
        print(f"Token refresh failed ({resp.status_code}): {resp.text}")
        return {}

    tokens = resp.json()
    tokens["obtained_at"] = time.time()
    _save_tokens(tokens)
    return tokens


def _load_tokens() -> dict:
    if TOKEN_FILE.exists():
        return json.loads(TOKEN_FILE.read_text())
    return {}


def _save_tokens(tokens: dict) -> None:
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(tokens, indent=2) + "\n")
    TOKEN_FILE.chmod(0o600)


def get_access_token(config: dict) -> str | None:
    """Get a valid access token, refreshing if needed."""
    tokens = _load_tokens()
    if not tokens:
        return None

    access_token = tokens.get("access_token")
    expires_in = tokens.get("expires_in", 3600)
    obtained_at = tokens.get("obtained_at", 0)

    # Refresh if expiring within 5 minutes
    if time.time() - obtained_at > (expires_in - 300):
        refresh_tok = tokens.get("refresh_token")
        if refresh_tok:
            print("Access token expired, refreshing...")
            new_tokens = refresh_access_token(
                config["app_id"], config["app_secret"], refresh_tok
            )
            if new_tokens:
                return new_tokens.get("access_token")
        return None

    return access_token


# ---------------------------------------------------------------------------
# Pinterest API client
# ---------------------------------------------------------------------------

def api_request(
    method: str,
    endpoint: str,
    access_token: str,
    json_data: dict | None = None,
    params: dict | None = None,
) -> dict:
    """Make an authenticated Pinterest API request."""
    url = f"{API_BASE}{endpoint}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    resp = requests.request(
        method, url, headers=headers, json=json_data, params=params, timeout=60
    )

    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 60))
        print(f"  Rate limited. Waiting {retry_after}s...")
        time.sleep(retry_after)
        resp = requests.request(
            method, url, headers=headers, json=json_data, params=params, timeout=60
        )

    if resp.status_code not in (200, 201):
        raise Exception(f"API error {resp.status_code}: {resp.text[:500]}")

    return resp.json()


def create_pin(
    access_token: str,
    board_id: str,
    title: str,
    description: str,
    link: str,
    image_path: Path,
) -> dict:
    """Create a pin with a base64-encoded image."""
    image_data = base64.b64encode(image_path.read_bytes()).decode("ascii")

    pin_data = {
        "board_id": board_id,
        "title": title[:100],
        "description": description[:500],
        "link": link,
        "media_source": {
            "source_type": "image_base64",
            "content_type": "image/png",
            "data": image_data,
        },
        "alt_text": title[:500],
    }

    return api_request("POST", "/pins", access_token, json_data=pin_data)


def list_boards(access_token: str) -> list[dict]:
    """List all boards for the authenticated user."""
    boards = []
    bookmark = None

    while True:
        params = {"page_size": 25}
        if bookmark:
            params["bookmark"] = bookmark
        resp = api_request("GET", "/boards", access_token, params=params)
        boards.extend(resp.get("items", []))
        bookmark = resp.get("bookmark")
        if not bookmark:
            break

    return boards


def create_board(access_token: str, name: str, description: str = "") -> dict:
    """Create a new board."""
    return api_request("POST", "/boards", access_token, json_data={
        "name": name[:50],
        "description": description[:500],
        "privacy": "PUBLIC",
    })


# ---------------------------------------------------------------------------
# Board management
# ---------------------------------------------------------------------------

def _load_board_cache() -> dict:
    if BOARD_CACHE_FILE.exists():
        return json.loads(BOARD_CACHE_FILE.read_text())
    return {}


def _save_board_cache(cache: dict) -> None:
    BOARD_CACHE_FILE.write_text(json.dumps(cache, indent=2) + "\n")


def resolve_board(niche: str, access_token: str) -> str:
    """Get or create the board for a niche. Returns board_id."""
    cache = _load_board_cache()

    # Check cache first
    if niche in cache:
        return cache[niche]["board_id"]

    board_name = NICHE_BOARDS.get(niche, DEFAULT_BOARD)

    # Check if board already exists on Pinterest
    existing = list_boards(access_token)
    for board in existing:
        if board["name"].lower() == board_name.lower():
            cache[niche] = {"board_id": board["id"], "name": board["name"]}
            _save_board_cache(cache)
            return board["id"]

    # Create new board
    print(f"  Creating board: {board_name}")
    board = create_board(access_token, board_name, f"{board_name} - Shop our collection!")
    cache[niche] = {"board_id": board["id"], "name": board["name"]}
    _save_board_cache(cache)
    return board["id"]


def setup_all_boards(access_token: str) -> None:
    """Pre-create all niche boards."""
    print("Setting up Pinterest boards...\n")
    for niche, board_name in NICHE_BOARDS.items():
        board_id = resolve_board(niche, access_token)
        print(f"  {niche:15s} -> {board_name} (ID: {board_id})")
    # Also create default board
    resolve_board("_default", access_token)
    print("\nAll boards ready!")


# ---------------------------------------------------------------------------
# Design discovery (mockups + metadata)
# ---------------------------------------------------------------------------

def discover_pinterest_designs(folder: str) -> list[tuple[Path, dict, str]]:
    """Find mockup images and pair them with metadata.

    Returns list of (mockup_path, metadata_dict, niche) tuples.
    """
    mockup_dir = MOCKUP_DIR / folder
    meta_dir = OUTPUT_DIR / folder

    if not mockup_dir.is_dir():
        print(f"Error: mockup folder not found: {mockup_dir}")
        sys.exit(1)

    designs = []
    for mockup_png in sorted(mockup_dir.glob("*_mockup.png")):
        # Derive original design name by stripping _mockup suffix
        stem = mockup_png.stem.replace("_mockup", "")
        meta_path = meta_dir / f"{stem}.json"

        if not meta_path.exists():
            continue

        with open(meta_path) as f:
            metadata = json.load(f)

        # Extract niche from filename (first part before _NNN_)
        niche = stem.split("_")[0]
        designs.append((mockup_png, metadata, niche))

    return designs


# ---------------------------------------------------------------------------
# Pin description builder
# ---------------------------------------------------------------------------

def build_pin_description(metadata: dict, link: str) -> str:
    """Build an SEO-optimized pin description."""
    title = metadata.get("title", "")
    desc = metadata.get("description", "")
    tags = metadata.get("tags", [])

    parts = []
    if desc:
        parts.append(desc)
    parts.append(f"Shop this design: {link}")
    if tags:
        tag_str = " ".join(f"#{t.replace('-', '').replace(' ', '')}" for t in tags[:10])
        parts.append(tag_str)

    full = "\n\n".join(parts)
    return full[:500]


def build_pin_link(title: str, shop_name: str) -> str:
    """Build a Redbubble search link from the design title."""
    query = urllib.parse.quote_plus(title.split(" - ")[0].strip())
    return f"https://www.redbubble.com/people/{shop_name}/shop?query={query}"


# ---------------------------------------------------------------------------
# Daily limit tracking
# ---------------------------------------------------------------------------

def pins_uploaded_today(tracker: dict) -> int:
    """Count pins with status=success uploaded today (EST)."""
    today = datetime.now(ZoneInfo("America/New_York")).date()
    count = 0
    for entry in tracker.values():
        if entry.get("status") != "success":
            continue
        try:
            ts = datetime.fromisoformat(entry["timestamp"])
            if ts.astimezone(ZoneInfo("America/New_York")).date() == today:
                count += 1
        except (ValueError, KeyError):
            continue
    return count


# ---------------------------------------------------------------------------
# Tracker helpers (extended)
# ---------------------------------------------------------------------------

def record_pin(
    tracker: dict, path: Path, key: str, status: str,
    error: str | None = None, pin_id: str | None = None,
    board_id: str | None = None, board_name: str | None = None,
) -> None:
    """Record a pin upload result with extended metadata."""
    from datetime import timezone
    tracker[key] = {
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error": error,
        "pin_id": pin_id,
        "board_id": board_id,
        "board_name": board_name,
    }
    save_tracker(tracker, path)


# ---------------------------------------------------------------------------
# Main upload loop
# ---------------------------------------------------------------------------

def run_pinterest_upload(args: argparse.Namespace) -> None:
    """Main Pinterest upload flow."""
    config = load_config()

    if not config.get("app_id") or not config.get("app_secret"):
        print("Pinterest app credentials not configured.")
        app_id = input("Enter your Pinterest App ID: ").strip()
        app_secret = input("Enter your Pinterest App Secret: ").strip()
        config["app_id"] = app_id
        config["app_secret"] = app_secret
        save_config(config)

    shop_name = args.shop_name or config.get("shop_name", DEFAULT_SHOP_NAME)
    if shop_name != config.get("shop_name"):
        config["shop_name"] = shop_name
        save_config(config)

    daily_limit = args.daily_limit

    # Get access token (or authorize)
    access_token = get_access_token(config)
    if not access_token:
        tokens = authorize(config["app_id"], config["app_secret"])
        access_token = tokens.get("access_token")
        if not access_token:
            print("ERROR: Could not obtain access token.")
            sys.exit(1)

    # Setup boards mode
    if args.setup_boards:
        setup_all_boards(access_token)
        return

    # Discover designs
    designs = discover_pinterest_designs(args.folder)
    if not designs:
        print(f"No mockup designs found in output/mockups/{args.folder}/")
        return
    print(f"Found {len(designs)} mockup designs in output/mockups/{args.folder}/")

    # Load tracker and filter
    tracker = load_tracker(TRACKER_FILE)
    to_upload = []
    for mockup_path, meta, niche in designs:
        key = f"{args.folder}/{mockup_path.stem.replace('_mockup', '')}"
        entry = tracker.get(key, {})
        status = entry.get("status")

        if args.retry_failed and status == "failed":
            to_upload.append((mockup_path, meta, niche, key))
        elif status == "success":
            continue
        elif not args.retry_failed:
            to_upload.append((mockup_path, meta, niche, key))

    if not to_upload:
        print("No designs to upload (all already pinned or no failures to retry).")
        return

    # Apply session limit
    if args.limit and args.limit > 0:
        to_upload = to_upload[:args.limit]

    # Check daily limit
    already_today = pins_uploaded_today(tracker)
    remaining = daily_limit - already_today
    if remaining <= 0:
        print(f"Daily limit reached ({already_today} pins today, limit {daily_limit}).")
        print("Try again tomorrow.")
        return
    if len(to_upload) > remaining:
        print(f"Daily limit: {remaining} pins remaining today ({already_today}/{daily_limit} used)")
        to_upload = to_upload[:remaining]

    print(f"Will {'preview' if args.dry_run else 'upload'} {len(to_upload)} pins")
    print(f"  Daily usage: {already_today}/{daily_limit} (remaining: {remaining})")
    print()

    # Dry run
    if args.dry_run:
        for i, (mockup_path, meta, niche, key) in enumerate(to_upload, 1):
            board_name = NICHE_BOARDS.get(niche, DEFAULT_BOARD)
            link = build_pin_link(meta["title"], shop_name)
            print(f"  [{i}] {key}")
            print(f"       Title: {meta['title']}")
            print(f"       Board: {board_name}")
            print(f"       Link:  {link}")
            print(f"       Tags:  {', '.join(meta.get('tags', [])[:8])}")
            print()
        print("Dry run complete — no pins created.")
        return

    # Upload loop
    consecutive_failures = 0
    uploaded_count = 0

    for i, (mockup_path, meta, niche, key) in enumerate(to_upload, 1):
        print(f"[{i}/{len(to_upload)}] Pinning: {key}")
        print(f"  Title: {meta['title']}")

        try:
            # Refresh token if needed
            access_token = get_access_token(config) or access_token

            # Resolve board
            board_id = resolve_board(niche, access_token)
            board_name = NICHE_BOARDS.get(niche, DEFAULT_BOARD)
            print(f"  Board: {board_name}")

            # Build pin data
            link = build_pin_link(meta["title"], shop_name)
            description = build_pin_description(meta, link)

            # Create pin
            result = create_pin(
                access_token, board_id,
                meta["title"], description, link,
                mockup_path,
            )

            pin_id = result.get("id")
            record_pin(
                tracker, TRACKER_FILE, key, "success",
                pin_id=pin_id, board_id=board_id, board_name=board_name,
            )
            consecutive_failures = 0
            uploaded_count += 1
            print(f"  -> Success (pin ID: {pin_id})")

        except Exception as e:
            record_pin(tracker, TRACKER_FILE, key, "failed", error=str(e))
            consecutive_failures += 1
            print(f"  -> Failed: {e}")

        # Circuit breaker
        if consecutive_failures >= CONSECUTIVE_FAILURE_LIMIT:
            print(f"\n=== {CONSECUTIVE_FAILURE_LIMIT} consecutive failures ===")
            print("  Something may be wrong. Stopping.")
            break

        # Pacing
        if i < len(to_upload):
            # Break after every N pins
            if uploaded_count > 0 and uploaded_count % PINTEREST_BREAK_INTERVAL == 0:
                pause = random.uniform(*PINTEREST_BREAK_RANGE)
                print(f"\n--- Break ({uploaded_count} pins): pausing {pause / 60:.0f} min ---")
                time.sleep(pause)

            wait_time = jittered_delay(args.delay)
            print(f"  Waiting {wait_time:.0f}s before next pin...")
            time.sleep(wait_time)

    # Summary
    print(f"\n=== Pinterest session complete ===")
    print(f"  Pinned: {uploaded_count}/{len(to_upload)}")
    total_today = pins_uploaded_today(tracker)
    print(f"  Daily usage: {total_today}/{daily_limit}")
    failed = sum(1 for _, _, _, k in to_upload if tracker.get(k, {}).get("status") == "failed")
    if failed:
        print(f"  Failed: {failed}")
        print(f"  Re-run with --retry-failed to retry")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upload product mockups to Pinterest as pins via API v5.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python3 upload_pinterest.py --folder tshirt --limit 1       # Test one pin
  python3 upload_pinterest.py --folder tshirt --dry-run        # Preview
  python3 upload_pinterest.py --folder tshirt --limit 10       # Batch upload
  python3 upload_pinterest.py --folder tshirt --retry-failed   # Retry failures
  python3 upload_pinterest.py --setup-boards                   # Create boards only
""",
    )
    parser.add_argument(
        "--folder", default="tshirt",
        help="Mockup folder to pin (tshirt, poster, sticker) (default: tshirt)",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Max pins this session (0 = up to daily limit)",
    )
    parser.add_argument(
        "--delay", type=float, default=PINTEREST_DEFAULT_DELAY,
        help=f"Seconds between pins (default: {PINTEREST_DEFAULT_DELAY})",
    )
    parser.add_argument(
        "--daily-limit", type=int, default=PINTEREST_DAILY_LIMIT,
        help=f"Max pins per day (default: {PINTEREST_DAILY_LIMIT})",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview pins without uploading",
    )
    parser.add_argument(
        "--retry-failed", action="store_true",
        help="Only retry previously failed pins",
    )
    parser.add_argument(
        "--shop-name",
        help=f"Redbubble shop name for links (default: {DEFAULT_SHOP_NAME})",
    )
    parser.add_argument(
        "--setup-boards", action="store_true",
        help="Create all niche boards and exit",
    )
    args = parser.parse_args()

    if args.limit == 0:
        args.limit = None

    run_pinterest_upload(args)


if __name__ == "__main__":
    main()
