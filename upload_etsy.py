#!/usr/bin/env python3
"""Etsy auto-upload script using the Etsy Open API v3.

Creates draft listings with images and metadata from paired JSON files.
Uses OAuth 2.0 with PKCE for authentication (one-time browser login, then auto-refresh).
Listings are created as drafts; activate manually or with --activate flag.

Setup:
    1. Create an Etsy shop at etsy.com
    2. Register as a developer at etsy.com/developers/register
    3. Create an app to get your API keystring and shared secret
    4. First run will open browser for OAuth login

Usage:
    python3 upload_etsy.py --folder tshirt --limit 1         # Test one listing
    python3 upload_etsy.py --folder tshirt --dry-run          # Preview
    python3 upload_etsy.py --folder tshirt --limit 10         # Upload batch
    python3 upload_etsy.py --folder tshirt --retry-failed     # Retry failures
    python3 upload_etsy.py --folder tshirt --activate         # Create + activate
    python3 upload_etsy.py --setup-shop                       # Fetch shop info & sections
    python3 upload_etsy.py --lookup-taxonomy                  # Browse categories
"""

from __future__ import annotations

import argparse
import hashlib
import http.server
import json
import os
import random
import secrets
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
    maybe_take_break,
    CONSECUTIVE_FAILURE_LIMIT,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).parent / "output"
TRACKER_FILE = Path(__file__).parent / "uploaded_etsy.json"
CONFIG_FILE = Path(__file__).parent / ".etsy_config.json"
TOKEN_FILE = Path(__file__).parent / ".etsy_session" / "tokens.json"
SECTION_CACHE_FILE = Path(__file__).parent / ".etsy_sections.json"
TAXONOMY_CACHE_FILE = Path(__file__).parent / ".etsy_taxonomy.json"

# Etsy API v3
API_BASE = "https://openapi.etsy.com/v3/application"
OAUTH_CONNECT_URL = "https://www.etsy.com/oauth/connect"
TOKEN_URL = "https://api.etsy.com/v3/public/oauth/token"
REDIRECT_URI = "http://localhost:9877/callback"
SCOPES = "listings_r listings_w shops_r"

# Pacing
ETSY_DEFAULT_DELAY = 8            # 8s between listings (10 QPS limit)
ETSY_DAILY_LIMIT = 500            # conservative daily cap (API allows 10k calls)
ETSY_BREAK_INTERVAL = 50          # break after every 50 listings
ETSY_BREAK_RANGE = (120, 300)     # 2-5 minute break

# Default listing values
DEFAULT_PRICE = 19.99
DEFAULT_QUANTITY = 999
DEFAULT_WHO_MADE = "i_did"
DEFAULT_WHEN_MADE = "2020_2025"
DEFAULT_LISTING_TYPE = "physical"

# Niche -> Etsy shop section mapping
NICHE_SECTIONS = {
    "coffee":       "Coffee Lover Designs",
    "dad":          "Dad Jokes & Gifts",
    "drinking":     "Drinking Humor",
    "fitness":      "Gym & Fitness",
    "funny":        "Funny & Humor",
    "gaming":       "Gamer Designs",
    "hobby":        "Hobby & Craft",
    "introvert":    "Introvert Life",
    "mom":          "Mom Life",
    "motivational": "Motivational Quotes",
    "pets":         "Pet Lover",
    "profession":   "Work & Career",
    "sarcasm":      "Sarcastic & Witty",
    "seasonal":     "Holiday & Seasonal",
}
DEFAULT_SECTION = "All Designs"

# Taxonomy IDs for common POD products (look up with --lookup-taxonomy)
# These are placeholders — run --lookup-taxonomy to find the right IDs for your shop
PRODUCT_TAXONOMY = {
    "tshirt": None,     # Clothing > Shirts & Tees
    "sticker": None,    # Paper & Party Supplies > Stickers
    "poster": None,     # Art & Collectibles > Prints
}

# Tags that are too generic for Etsy (max 20 chars each, max 13 tags)
_GENERIC_TAGS = frozenset({
    "redbubble", "teepublic", "print-on-demand", "print on demand", "pod",
    "design", "niche", "themed", "typography", "graphic", "art", "artwork",
    "cool", "unique", "creative", "custom", "trendy", "aesthetic",
})


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
# OAuth 2.0 with PKCE
# ---------------------------------------------------------------------------

_auth_code_result: dict[str, str | None] = {"code": None, "state": None}


class _OAuthHandler(http.server.BaseHTTPRequestHandler):
    """Handle the OAuth redirect callback."""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            _auth_code_result["code"] = params["code"][0]
            _auth_code_result["state"] = params.get("state", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h2>Etsy authorization successful!</h2>"
                b"<p>You can close this window and return to the terminal.</p>"
                b"</body></html>"
            )
        else:
            self.send_response(400)
            self.end_headers()
            error = params.get("error", ["unknown"])[0]
            self.wfile.write(f"Error: {error}".encode())

    def log_message(self, format, *args):
        pass


def _generate_pkce_pair() -> tuple[str, str]:
    """Generate a PKCE code_verifier and code_challenge (S256)."""
    code_verifier = secrets.token_urlsafe(64)[:128]
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    # base64url encode without padding
    code_challenge = (
        digest.hex()  # not used, replaced below
    )
    import base64
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return code_verifier, code_challenge


def authorize(api_keystring: str) -> dict:
    """Run the full OAuth 2.0 + PKCE flow. Returns token dict."""
    state = secrets.token_urlsafe(16)
    code_verifier, code_challenge = _generate_pkce_pair()

    auth_url = (
        f"{OAUTH_CONNECT_URL}"
        f"?response_type=code"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
        f"&scope={urllib.parse.quote(SCOPES)}"
        f"&client_id={api_keystring}"
        f"&state={state}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )

    # Start local server to catch the redirect
    server = http.server.HTTPServer(("localhost", 9877), _OAuthHandler)
    server_thread = threading.Thread(target=server.handle_request, daemon=True)
    server_thread.start()

    print("\nOpening browser for Etsy authorization...")
    print(f"  If the browser doesn't open, visit:\n  {auth_url}\n")
    webbrowser.open(auth_url)

    # Wait for the callback
    server_thread.join(timeout=120)
    server.server_close()

    code = _auth_code_result["code"]
    if not code:
        print("ERROR: Did not receive authorization code.")
        sys.exit(1)

    # Verify state
    if _auth_code_result["state"] != state:
        print("ERROR: State mismatch — possible CSRF attack.")
        sys.exit(1)

    # Exchange code for tokens
    print("Exchanging authorization code for tokens...")
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "client_id": api_keystring,
            "redirect_uri": REDIRECT_URI,
            "code": code,
            "code_verifier": code_verifier,
        },
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


def refresh_access_token(api_keystring: str, refresh_token: str) -> dict:
    """Use refresh token to get a new access token."""
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "client_id": api_keystring,
            "refresh_token": refresh_token,
        },
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
                config["api_keystring"], refresh_tok
            )
            if new_tokens:
                return new_tokens.get("access_token")
        return None

    return access_token


# ---------------------------------------------------------------------------
# Etsy API client
# ---------------------------------------------------------------------------

def api_request(
    method: str,
    endpoint: str,
    api_keystring: str,
    access_token: str | None = None,
    json_data: dict | None = None,
    params: dict | None = None,
    files: dict | None = None,
) -> dict:
    """Make an Etsy API request. All requests need x-api-key; most need Bearer token."""
    url = f"{API_BASE}{endpoint}"
    headers = {
        "x-api-key": api_keystring,
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    kwargs: dict = {"headers": headers, "timeout": 60}

    if files:
        # multipart/form-data — don't set Content-Type, requests handles it
        kwargs["files"] = files
        if json_data:
            kwargs["data"] = json_data
    elif json_data:
        headers["Content-Type"] = "application/json"
        kwargs["json"] = json_data

    if params:
        kwargs["params"] = params

    resp = requests.request(method, url, **kwargs)

    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 5))
        print(f"  Rate limited. Waiting {retry_after}s...")
        time.sleep(retry_after)
        resp = requests.request(method, url, **kwargs)

    if resp.status_code not in (200, 201):
        raise Exception(f"Etsy API error {resp.status_code}: {resp.text[:500]}")

    return resp.json()


# ---------------------------------------------------------------------------
# Shop helpers
# ---------------------------------------------------------------------------

def get_me(api_keystring: str, access_token: str) -> dict:
    """Get the authenticated user's info via the /users/me endpoint."""
    url = "https://api.etsy.com/v3/application/users/me"
    headers = {
        "x-api-key": api_keystring,
        "Authorization": f"Bearer {access_token}",
    }
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code != 200:
        raise Exception(f"Failed to get user info ({resp.status_code}): {resp.text[:300]}")
    return resp.json()


def get_shop_id(api_keystring: str, access_token: str) -> int:
    """Get the authenticated user's shop ID."""
    user = get_me(api_keystring, access_token)
    user_id = user.get("user_id")
    if not user_id:
        raise Exception("Could not determine user ID from token")

    shop_resp = api_request(
        "GET", f"/users/{user_id}/shops",
        api_keystring, access_token,
    )
    shops = shop_resp.get("results", [])
    if not shops:
        raise Exception("No Etsy shop found for this account. Create one at etsy.com first.")
    return shops[0]["shop_id"]


def get_shipping_profiles(api_keystring: str, access_token: str, shop_id: int) -> list[dict]:
    """List shipping profiles for the shop."""
    resp = api_request(
        "GET", f"/shops/{shop_id}/shipping-profiles",
        api_keystring, access_token,
    )
    return resp.get("results", [])


def get_return_policies(api_keystring: str, access_token: str, shop_id: int) -> list[dict]:
    """List return policies for the shop."""
    resp = api_request(
        "GET", f"/shops/{shop_id}/policies/return",
        api_keystring, access_token,
    )
    return resp.get("results", [])


def get_shop_sections(api_keystring: str, access_token: str, shop_id: int) -> list[dict]:
    """List shop sections."""
    resp = api_request(
        "GET", f"/shops/{shop_id}/sections",
        api_keystring, access_token,
    )
    return resp.get("results", [])


def create_shop_section(api_keystring: str, access_token: str, shop_id: int, title: str) -> dict:
    """Create a new shop section."""
    return api_request(
        "POST", f"/shops/{shop_id}/sections",
        api_keystring, access_token,
        json_data={"title": title},
    )


# ---------------------------------------------------------------------------
# Taxonomy lookup
# ---------------------------------------------------------------------------

def get_seller_taxonomy(api_keystring: str) -> list[dict]:
    """Fetch the full seller taxonomy tree (public endpoint, no auth needed)."""
    resp = api_request("GET", "/seller-taxonomy/nodes", api_keystring)
    return resp.get("results", [])


def _flatten_taxonomy(nodes: list[dict], depth: int = 0) -> list[tuple[int, str, int]]:
    """Flatten taxonomy tree into (id, name, depth) tuples."""
    result = []
    for node in nodes:
        result.append((node["id"], node["name"], depth))
        if node.get("children"):
            result.extend(_flatten_taxonomy(node["children"], depth + 1))
    return result


def lookup_taxonomy(api_keystring: str, search: str | None = None) -> None:
    """Print taxonomy tree, optionally filtered by keyword."""
    # Check cache first
    if TAXONOMY_CACHE_FILE.exists():
        nodes = json.loads(TAXONOMY_CACHE_FILE.read_text())
    else:
        print("Fetching Etsy seller taxonomy...")
        nodes = get_seller_taxonomy(api_keystring)
        TAXONOMY_CACHE_FILE.write_text(json.dumps(nodes, indent=2) + "\n")
        print(f"  Cached {len(nodes)} top-level categories\n")

    flat = _flatten_taxonomy(nodes)

    if search:
        search_lower = search.lower()
        matches = [(tid, name, d) for tid, name, d in flat if search_lower in name.lower()]
        if not matches:
            print(f"No taxonomy nodes matching '{search}'")
            return
        print(f"Taxonomy nodes matching '{search}':\n")
        for tid, name, d in matches:
            indent = "  " * d
            print(f"  {tid:>8d}  {indent}{name}")
    else:
        print("Top-level Etsy categories:\n")
        for tid, name, d in flat:
            if d <= 1:
                indent = "  " * d
                print(f"  {tid:>8d}  {indent}{name}")
        print("\n  Use --taxonomy-search 'keyword' to drill deeper")


# ---------------------------------------------------------------------------
# Section management
# ---------------------------------------------------------------------------

def _load_section_cache() -> dict:
    if SECTION_CACHE_FILE.exists():
        return json.loads(SECTION_CACHE_FILE.read_text())
    return {}


def _save_section_cache(cache: dict) -> None:
    SECTION_CACHE_FILE.write_text(json.dumps(cache, indent=2) + "\n")


def resolve_section(
    niche: str, api_keystring: str, access_token: str, shop_id: int,
) -> int | None:
    """Get or create the shop section for a niche. Returns section_id."""
    cache = _load_section_cache()

    if niche in cache:
        return cache[niche]["section_id"]

    section_title = NICHE_SECTIONS.get(niche, DEFAULT_SECTION)

    # Check existing sections
    existing = get_shop_sections(api_keystring, access_token, shop_id)
    for section in existing:
        if section["title"].lower() == section_title.lower():
            cache[niche] = {"section_id": section["shop_section_id"], "title": section["title"]}
            _save_section_cache(cache)
            return section["shop_section_id"]

    # Create new section
    print(f"  Creating shop section: {section_title}")
    section = create_shop_section(api_keystring, access_token, shop_id, section_title)
    section_id = section.get("shop_section_id")
    cache[niche] = {"section_id": section_id, "title": section_title}
    _save_section_cache(cache)
    return section_id


# ---------------------------------------------------------------------------
# Listing creation
# ---------------------------------------------------------------------------

def create_draft_listing(
    api_keystring: str,
    access_token: str,
    shop_id: int,
    title: str,
    description: str,
    tags: list[str],
    price: float,
    quantity: int,
    taxonomy_id: int | None = None,
    section_id: int | None = None,
    shipping_profile_id: int | None = None,
    return_policy_id: int | None = None,
    production_partner_ids: list[int] | None = None,
) -> dict:
    """Create a draft listing on Etsy."""
    listing_data: dict = {
        "title": title[:140],
        "description": description,
        "quantity": quantity,
        "price": price,
        "who_made": DEFAULT_WHO_MADE,
        "when_made": DEFAULT_WHEN_MADE,
        "type": DEFAULT_LISTING_TYPE,
        "is_supply": False,
    }

    # Etsy allows max 13 tags, each max 20 chars
    clean_tags = _prepare_tags(tags)
    if clean_tags:
        listing_data["tags"] = clean_tags

    if taxonomy_id:
        listing_data["taxonomy_id"] = taxonomy_id
    if section_id:
        listing_data["shop_section_id"] = section_id
    if shipping_profile_id:
        listing_data["shipping_profile_id"] = shipping_profile_id
    if return_policy_id:
        listing_data["return_policy_id"] = return_policy_id
    if production_partner_ids:
        listing_data["production_partner_ids"] = production_partner_ids

    return api_request(
        "POST", f"/shops/{shop_id}/listings",
        api_keystring, access_token,
        json_data=listing_data,
    )


def upload_listing_image(
    api_keystring: str,
    access_token: str,
    shop_id: int,
    listing_id: int,
    image_path: Path,
    rank: int = 1,
    alt_text: str = "",
) -> dict:
    """Upload an image to a listing via multipart/form-data."""
    url = f"{API_BASE}/shops/{shop_id}/listings/{listing_id}/images"
    headers = {
        "x-api-key": api_keystring,
        "Authorization": f"Bearer {access_token}",
    }

    with open(image_path, "rb") as f:
        files = {"image": (image_path.name, f, "image/png")}
        data = {"rank": str(rank)}
        if alt_text:
            data["alt_text"] = alt_text[:250]

        resp = requests.post(url, headers=headers, files=files, data=data, timeout=120)

    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 5))
        print(f"  Rate limited. Waiting {retry_after}s...")
        time.sleep(retry_after)
        with open(image_path, "rb") as f:
            files = {"image": (image_path.name, f, "image/png")}
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=120)

    if resp.status_code not in (200, 201):
        raise Exception(f"Image upload failed ({resp.status_code}): {resp.text[:500]}")

    return resp.json()


def activate_listing(
    api_keystring: str,
    access_token: str,
    shop_id: int,
    listing_id: int,
) -> dict:
    """Set a listing from draft to active state."""
    return api_request(
        "PUT", f"/shops/{shop_id}/listings/{listing_id}",
        api_keystring, access_token,
        json_data={"state": "active"},
    )


# ---------------------------------------------------------------------------
# Tag preparation
# ---------------------------------------------------------------------------

def _prepare_tags(tags: list[str]) -> list[str]:
    """Clean and prepare tags for Etsy (max 13 tags, max 20 chars each)."""
    clean = []
    for tag in tags:
        t = tag.strip().replace("-", " ")
        if t.lower() in _GENERIC_TAGS:
            continue
        if len(t) > 20:
            t = t[:20]
        if t and t not in clean:
            clean.append(t)
        if len(clean) >= 13:
            break
    return clean


# ---------------------------------------------------------------------------
# Design discovery
# ---------------------------------------------------------------------------

def discover_etsy_designs(folder: str) -> list[tuple[Path, dict, str]]:
    """Find design images and pair them with metadata.

    Returns list of (image_path, metadata_dict, niche) tuples.
    Uses the original high-res designs (not mockups) since Etsy wants product images.
    """
    design_dir = OUTPUT_DIR / folder

    if not design_dir.is_dir():
        print(f"Error: design folder not found: {design_dir}")
        sys.exit(1)

    designs = []
    for png_path in sorted(design_dir.glob("*.png")):
        meta_path = png_path.with_suffix(".json")
        if not meta_path.exists():
            continue

        with open(meta_path) as f:
            metadata = json.load(f)

        niche = png_path.stem.split("_")[0]
        designs.append((png_path, metadata, niche))

    return designs


# ---------------------------------------------------------------------------
# Description builder
# ---------------------------------------------------------------------------

def build_etsy_description(metadata: dict, folder: str) -> str:
    """Build an Etsy listing description from metadata."""
    title = metadata.get("title", "")
    desc = metadata.get("description", "")
    tags = metadata.get("tags", [])

    product_types = {
        "tshirt": "t-shirt",
        "sticker": "sticker",
        "poster": "poster",
    }
    product_name = product_types.get(folder, "design")

    parts = []
    if desc:
        parts.append(desc)

    parts.append(f"\nThis {product_name} features the design: \"{title.split(' - ')[0].strip()}\"")
    parts.append(
        "\nPerfect as a gift or treat for yourself. "
        "High-quality print-on-demand product made to order."
    )

    if tags:
        keyword_str = ", ".join(t.replace("-", " ") for t in tags[:8])
        parts.append(f"\nKeywords: {keyword_str}")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Daily limit tracking
# ---------------------------------------------------------------------------

def listings_created_today(tracker: dict) -> int:
    """Count listings with status=success created today (EST)."""
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
# Tracker helpers
# ---------------------------------------------------------------------------

def record_listing(
    tracker: dict, key: str, status: str,
    error: str | None = None, listing_id: int | None = None,
    section_name: str | None = None, activated: bool = False,
) -> None:
    """Record a listing upload result."""
    from datetime import timezone
    tracker[key] = {
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error": error,
        "listing_id": listing_id,
        "section": section_name,
        "activated": activated,
    }
    save_tracker(tracker, TRACKER_FILE)


# ---------------------------------------------------------------------------
# Shop setup / info
# ---------------------------------------------------------------------------

def setup_shop(config: dict, access_token: str) -> None:
    """Fetch and display shop info, shipping profiles, return policies."""
    api_key = config["api_keystring"]
    shop_id = config.get("shop_id")

    if not shop_id:
        print("Looking up your shop...")
        shop_id = get_shop_id(api_key, access_token)
        config["shop_id"] = shop_id
        save_config(config)

    print(f"\nShop ID: {shop_id}")

    # Shipping profiles
    print("\nShipping profiles:")
    profiles = get_shipping_profiles(api_key, access_token, shop_id)
    if profiles:
        for p in profiles:
            flag = " (configured)" if p["shipping_profile_id"] == config.get("shipping_profile_id") else ""
            print(f"  {p['shipping_profile_id']:>10d}  {p['title']}{flag}")
        if not config.get("shipping_profile_id") and profiles:
            config["shipping_profile_id"] = profiles[0]["shipping_profile_id"]
            save_config(config)
            print(f"\n  Auto-selected: {profiles[0]['title']} (ID: {profiles[0]['shipping_profile_id']})")
    else:
        print("  None found — create one at etsy.com/your/shops/me/tools/shipping-profiles")

    # Return policies
    print("\nReturn policies:")
    policies = get_return_policies(api_key, access_token, shop_id)
    if policies:
        for p in policies:
            flag = " (configured)" if p.get("return_policy_id") == config.get("return_policy_id") else ""
            print(f"  {p.get('return_policy_id', 'N/A'):>10}  accepts_returns={p.get('accepts_returns')}{flag}")
        if not config.get("return_policy_id") and policies:
            config["return_policy_id"] = policies[0].get("return_policy_id")
            save_config(config)
            print(f"\n  Auto-selected first return policy")
    else:
        print("  None found — configure one at etsy.com/your/shops/me/tools/return-policy")

    # Sections
    print("\nShop sections:")
    sections = get_shop_sections(api_key, access_token, shop_id)
    if sections:
        for s in sections:
            print(f"  {s['shop_section_id']:>10d}  {s['title']}")
    else:
        print("  None — sections will be created automatically during upload")

    print("\nShop setup complete!")
    print("  Config saved to .etsy_config.json")


# ---------------------------------------------------------------------------
# Main upload loop
# ---------------------------------------------------------------------------

def _dry_run(args: argparse.Namespace) -> None:
    """Preview designs without needing API credentials."""
    designs = discover_etsy_designs(args.folder)
    if not designs:
        print(f"No designs found in output/{args.folder}/")
        return
    print(f"Found {len(designs)} designs in output/{args.folder}/")

    tracker = load_tracker(TRACKER_FILE)
    to_upload = []
    for png_path, meta, niche in designs:
        key = f"{args.folder}/{png_path.stem}"
        entry = tracker.get(key, {})
        status = entry.get("status")

        if args.retry_failed and status == "failed":
            to_upload.append((png_path, meta, niche, key))
        elif status == "success":
            continue
        elif not args.retry_failed:
            to_upload.append((png_path, meta, niche, key))

    if not to_upload:
        print("No designs to upload (all already listed or no failures to retry).")
        return

    if args.limit and args.limit > 0:
        to_upload = to_upload[:args.limit]

    price = args.price or DEFAULT_PRICE
    print(f"Will preview {len(to_upload)} listings (price: ${price:.2f})\n")

    for i, (png_path, meta, niche, key) in enumerate(to_upload, 1):
        section_name = NICHE_SECTIONS.get(niche, DEFAULT_SECTION)
        tags = _prepare_tags(meta.get("tags", []))
        print(f"  [{i}] {key}")
        print(f"       Title:   {meta['title'][:140]}")
        print(f"       Section: {section_name}")
        print(f"       Tags:    {', '.join(tags[:8])}")
        print(f"       Image:   {png_path.name}")
        print()

    print("Dry run complete — no listings created.")


def run_etsy_upload(args: argparse.Namespace) -> None:
    """Main Etsy upload flow."""
    config = load_config()
    api_key = config.get("api_keystring", "")

    # Taxonomy lookup mode (needs API key but not OAuth)
    if args.lookup_taxonomy:
        if not api_key:
            print("ERROR: API keystring required. Run once without --lookup-taxonomy to configure.")
            sys.exit(1)
        lookup_taxonomy(api_key, args.taxonomy_search)
        return

    # Dry-run can work without credentials (just previews designs)
    if args.dry_run:
        _dry_run(args)
        return

    # From here on, we need real credentials
    if not api_key:
        print("Etsy app credentials not configured.")
        api_keystring = input("Enter your Etsy API keystring (App ID): ").strip()
        config["api_keystring"] = api_keystring
        api_key = api_keystring
        save_config(config)

    # Get access token (or authorize)
    access_token = get_access_token(config)
    if not access_token:
        tokens = authorize(api_key)
        access_token = tokens.get("access_token")
        if not access_token:
            print("ERROR: Could not obtain access token.")
            sys.exit(1)

    # Shop setup mode
    if args.setup_shop:
        setup_shop(config, access_token)
        return

    # Ensure shop_id is known
    shop_id = config.get("shop_id")
    if not shop_id:
        print("Looking up your shop ID...")
        shop_id = get_shop_id(api_key, access_token)
        config["shop_id"] = shop_id
        save_config(config)
        print(f"  Shop ID: {shop_id}")

    # Listing configuration
    price = args.price or config.get("price", DEFAULT_PRICE)
    taxonomy_id = config.get(f"taxonomy_{args.folder}") or PRODUCT_TAXONOMY.get(args.folder)
    shipping_profile_id = config.get("shipping_profile_id")
    return_policy_id = config.get("return_policy_id")

    if not taxonomy_id:
        print(f"WARNING: No taxonomy_id configured for '{args.folder}' products.")
        print("  Listings will be created without a category.")
        print("  Run --lookup-taxonomy --taxonomy-search 'tshirt' to find the right ID.")
        print("  Then add it to .etsy_config.json as \"taxonomy_tshirt\": <id>")
        print()

    # Discover designs
    designs = discover_etsy_designs(args.folder)
    if not designs:
        print(f"No designs found in output/{args.folder}/")
        return
    print(f"Found {len(designs)} designs in output/{args.folder}/")

    # Load tracker and filter
    tracker = load_tracker(TRACKER_FILE)
    to_upload = []
    for png_path, meta, niche in designs:
        key = f"{args.folder}/{png_path.stem}"
        entry = tracker.get(key, {})
        status = entry.get("status")

        if args.retry_failed and status == "failed":
            to_upload.append((png_path, meta, niche, key))
        elif status == "success":
            continue
        elif not args.retry_failed:
            to_upload.append((png_path, meta, niche, key))

    if not to_upload:
        print("No designs to upload (all already listed or no failures to retry).")
        return

    # Apply session limit
    if args.limit and args.limit > 0:
        to_upload = to_upload[:args.limit]

    # Check daily limit
    daily_limit = args.daily_limit
    already_today = listings_created_today(tracker)
    remaining = daily_limit - already_today
    if remaining <= 0:
        print(f"Daily limit reached ({already_today} listings today, limit {daily_limit}).")
        return
    if len(to_upload) > remaining:
        print(f"Daily limit: {remaining} listings remaining ({already_today}/{daily_limit} used)")
        to_upload = to_upload[:remaining]

    print(f"Will {'preview' if args.dry_run else 'upload'} {len(to_upload)} listings")
    print(f"  Price: ${price:.2f} | Activate: {args.activate}")
    print(f"  Daily usage: {already_today}/{daily_limit} (remaining: {remaining})")
    print()

    # Dry run
    if args.dry_run:
        for i, (png_path, meta, niche, key) in enumerate(to_upload, 1):
            section_name = NICHE_SECTIONS.get(niche, DEFAULT_SECTION)
            tags = _prepare_tags(meta.get("tags", []))
            print(f"  [{i}] {key}")
            print(f"       Title:   {meta['title'][:140]}")
            print(f"       Section: {section_name}")
            print(f"       Tags:    {', '.join(tags[:8])}")
            print(f"       Image:   {png_path.name}")
            print()
        print("Dry run complete — no listings created.")
        return

    # Upload loop
    consecutive_failures = 0
    uploaded_count = 0

    for i, (png_path, meta, niche, key) in enumerate(to_upload, 1):
        print(f"[{i}/{len(to_upload)}] Listing: {key}")
        print(f"  Title: {meta['title'][:140]}")

        try:
            # Refresh token if needed
            access_token = get_access_token(config) or access_token

            # Resolve shop section
            section_id = resolve_section(niche, api_key, access_token, shop_id)
            section_name = NICHE_SECTIONS.get(niche, DEFAULT_SECTION)
            print(f"  Section: {section_name}")

            # Build listing data
            description = build_etsy_description(meta, args.folder)
            tags = meta.get("tags", [])

            # Create draft listing
            listing = create_draft_listing(
                api_key, access_token, shop_id,
                title=meta["title"],
                description=description,
                tags=tags,
                price=price,
                quantity=DEFAULT_QUANTITY,
                taxonomy_id=taxonomy_id,
                section_id=section_id,
                shipping_profile_id=shipping_profile_id,
                return_policy_id=return_policy_id,
            )
            listing_id = listing.get("listing_id")
            print(f"  Draft created (ID: {listing_id})")

            # Upload image
            upload_listing_image(
                api_key, access_token, shop_id, listing_id,
                png_path, rank=1, alt_text=meta["title"][:250],
            )
            print(f"  Image uploaded")

            # Optionally activate
            activated = False
            if args.activate and shipping_profile_id and return_policy_id:
                activate_listing(api_key, access_token, shop_id, listing_id)
                activated = True
                print(f"  Listing activated")

            record_listing(
                tracker, key, "success",
                listing_id=listing_id,
                section_name=section_name,
                activated=activated,
            )
            consecutive_failures = 0
            uploaded_count += 1
            print(f"  -> Success")

        except Exception as e:
            record_listing(tracker, key, "failed", error=str(e))
            consecutive_failures += 1
            print(f"  -> Failed: {e}")

        # Circuit breaker
        if consecutive_failures >= CONSECUTIVE_FAILURE_LIMIT:
            print(f"\n=== {CONSECUTIVE_FAILURE_LIMIT} consecutive failures ===")
            print("  Something may be wrong. Stopping.")
            break

        # Pacing
        if i < len(to_upload):
            maybe_take_break(uploaded_count)
            wait_time = jittered_delay(args.delay)
            print(f"  Waiting {wait_time:.0f}s before next listing...")
            time.sleep(wait_time)

    # Summary
    print(f"\n=== Etsy session complete ===")
    print(f"  Created: {uploaded_count}/{len(to_upload)}")
    total_today = listings_created_today(tracker)
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
        description="Upload POD designs to Etsy as listings via API v3.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python3 upload_etsy.py --setup-shop                             # First run: configure
  python3 upload_etsy.py --lookup-taxonomy --taxonomy-search shirt  # Find category IDs
  python3 upload_etsy.py --folder tshirt --limit 1                 # Test one listing
  python3 upload_etsy.py --folder tshirt --dry-run                 # Preview
  python3 upload_etsy.py --folder tshirt --limit 10                # Upload batch
  python3 upload_etsy.py --folder tshirt --activate                # Create + activate
  python3 upload_etsy.py --folder tshirt --retry-failed            # Retry failures
""",
    )
    parser.add_argument(
        "--folder", default="tshirt",
        help="Design folder to list (tshirt, poster, sticker) (default: tshirt)",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Max listings this session (0 = up to daily limit)",
    )
    parser.add_argument(
        "--delay", type=float, default=ETSY_DEFAULT_DELAY,
        help=f"Seconds between listings (default: {ETSY_DEFAULT_DELAY})",
    )
    parser.add_argument(
        "--daily-limit", type=int, default=ETSY_DAILY_LIMIT,
        help=f"Max listings per day (default: {ETSY_DAILY_LIMIT})",
    )
    parser.add_argument(
        "--price", type=float, default=None,
        help=f"Listing price in USD (default: {DEFAULT_PRICE})",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview listings without creating them",
    )
    parser.add_argument(
        "--retry-failed", action="store_true",
        help="Only retry previously failed listings",
    )
    parser.add_argument(
        "--activate", action="store_true",
        help="Activate listings after creating (requires shipping profile + return policy)",
    )
    parser.add_argument(
        "--setup-shop", action="store_true",
        help="Fetch shop info, shipping profiles, return policies, and exit",
    )
    parser.add_argument(
        "--lookup-taxonomy", action="store_true",
        help="Browse Etsy product categories and exit",
    )
    parser.add_argument(
        "--taxonomy-search",
        help="Filter taxonomy results by keyword (use with --lookup-taxonomy)",
    )
    args = parser.parse_args()

    if args.limit == 0:
        args.limit = None

    run_etsy_upload(args)


if __name__ == "__main__":
    main()
