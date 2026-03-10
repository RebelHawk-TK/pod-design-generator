#!/usr/bin/env python3
"""Shared utilities for POD platform upload scripts.

Provides tracker, design discovery, delay/break scheduling, browser launch,
Cloudflare handling, selector helpers, and a generic upload loop with
circuit breaker and session recovery.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).parent / "output"

DEFAULT_DELAY = 45  # seconds between uploads
MIN_DELAY = 10
JITTER_FACTOR = 0.3  # +/- 30%
BREAK_INTERVAL_SMALL = 20
BREAK_INTERVAL_LARGE = 100
BREAK_SMALL_RANGE = (120, 300)   # 2-5 minutes
BREAK_LARGE_RANGE = (300, 600)   # 5-10 minutes
CONSECUTIVE_FAILURE_LIMIT = 5


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class SessionExpiredError(Exception):
    pass


class CaptchaError(Exception):
    pass


class UploadError(Exception):
    pass


# ---------------------------------------------------------------------------
# Tracker
# ---------------------------------------------------------------------------

def load_tracker(path: Path) -> dict:
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def save_tracker(tracker: dict, path: Path) -> None:
    with open(path, "w") as f:
        json.dump(tracker, f, indent=2)


def record_upload(tracker: dict, path: Path, key: str, status: str, error: str | None = None) -> None:
    tracker[key] = {
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error": error,
    }
    save_tracker(tracker, path)


# ---------------------------------------------------------------------------
# Design discovery
# ---------------------------------------------------------------------------

def discover_designs(folder: str, shuffle_niches: bool = False, source_dir: Path | None = None) -> list[tuple[Path, dict]]:
    """Find PNG files with paired JSON metadata.

    If source_dir is provided, looks in source_dir/folder/.
    Otherwise uses the default output/<folder>/ layout.

    If shuffle_niches is True, interleave designs from different niches
    so uploads are diverse (avoids uploading 50 coffees in a row).
    """
    folder_path = (source_dir / folder) if source_dir else (OUTPUT_DIR / folder)
    if not folder_path.is_dir():
        print(f"Error: folder not found: {folder_path}")
        sys.exit(1)

    designs = []
    for png in sorted(folder_path.glob("*.png")):
        meta_path = png.with_suffix(".json")
        if not meta_path.exists():
            print(f"  Skipping {png.name} — no metadata JSON found")
            continue
        with open(meta_path) as f:
            metadata = json.load(f)
        designs.append((png, metadata))

    if shuffle_niches and designs:
        designs = _interleave_by_niche(designs)

    return designs


def _interleave_by_niche(designs: list[tuple[Path, dict]]) -> list[tuple[Path, dict]]:
    """Interleave designs round-robin by niche for diverse upload ordering."""
    from collections import defaultdict

    buckets: dict[str, list] = defaultdict(list)
    for png, meta in designs:
        niche = png.stem.split("_")[0]
        buckets[niche].append((png, meta))

    # Round-robin through niches
    result = []
    niche_names = sorted(buckets.keys())
    max_len = max(len(b) for b in buckets.values())
    for i in range(max_len):
        for niche in niche_names:
            if i < len(buckets[niche]):
                result.append(buckets[niche][i])

    return result


def tracker_key(folder: str, png_path: Path, source_dir: Path | None = None) -> str:
    stem = png_path.stem
    # Strip product suffixes for cleaner keys
    for suffix in ("_poster", "_tshirt", "_sticker"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    if source_dir:
        return f"ext:{source_dir.name}/{folder}/{stem}"
    return f"{folder}/{stem}"


# ---------------------------------------------------------------------------
# Delay helpers
# ---------------------------------------------------------------------------

def jittered_delay(base: float) -> float:
    lo = max(MIN_DELAY, base * (1 - JITTER_FACTOR))
    hi = base * (1 + JITTER_FACTOR)
    return random.uniform(lo, hi)


def maybe_take_break(upload_count: int) -> None:
    if upload_count > 0 and upload_count % BREAK_INTERVAL_LARGE == 0:
        pause = random.uniform(*BREAK_LARGE_RANGE)
        print(f"\n--- Large break ({upload_count} uploads): pausing {pause:.0f}s ---")
        time.sleep(pause)
    elif upload_count > 0 and upload_count % BREAK_INTERVAL_SMALL == 0:
        pause = random.uniform(*BREAK_SMALL_RANGE)
        print(f"\n--- Break ({upload_count} uploads): pausing {pause:.0f}s ---")
        time.sleep(pause)


# ---------------------------------------------------------------------------
# Selector helpers
# ---------------------------------------------------------------------------

def find_element(page, selectors: list[str], description: str, timeout: int = 15000):
    """Try multiple selectors, return the first match."""
    for sel in selectors:
        try:
            el = page.wait_for_selector(sel, timeout=timeout, state="attached")
            if el:
                return el
        except Exception:
            continue
    raise RuntimeError(f"Could not find element: {description} (tried {len(selectors)} selectors)")


# ---------------------------------------------------------------------------
# Cloudflare / challenge detection
# ---------------------------------------------------------------------------

def is_cloudflare_challenge(page) -> bool:
    """Check if the page is showing a Cloudflare Turnstile or challenge screen."""
    title = page.title().lower()
    if "just a moment" in title or "attention required" in title:
        return True
    if page.query_selector('iframe[src*="challenges.cloudflare.com"]'):
        return True
    if page.query_selector('iframe[src*="turnstile"]'):
        return True
    if page.query_selector('#cf-chl-widget-container'):
        return True
    return False


def wait_for_cloudflare(page, timeout: int = 120) -> None:
    """If a Cloudflare challenge is present, wait for the user to solve it."""
    if not is_cloudflare_challenge(page):
        return

    print("\n=== Cloudflare challenge detected ===")
    print("  Click the checkbox in the browser to verify you are human.")
    print(f"  Waiting up to {timeout}s for the challenge to clear...")

    start = time.time()
    while time.time() - start < timeout:
        time.sleep(2)
        if not is_cloudflare_challenge(page):
            print("  Cloudflare challenge cleared.")
            time.sleep(3)
            return

    print("  Challenge did not auto-clear within timeout. Waiting 60 more seconds...")
    extra_start = time.time()
    while time.time() - extra_start < 60:
        time.sleep(3)
        if not is_cloudflare_challenge(page):
            print("  Cloudflare challenge cleared (extended wait).")
            time.sleep(3)
            return
    print("  Continuing despite challenge — may need manual intervention in browser.")


def page_has_captcha(page) -> bool:
    """Check if a CAPTCHA or Cloudflare challenge is present on the page."""
    if is_cloudflare_challenge(page):
        return True
    captcha_selectors = [
        'iframe[src*="captcha"]',
        'iframe[src*="recaptcha"]',
        'iframe[src*="hcaptcha"]',
        '.g-recaptcha',
        '#captcha',
        '[data-captcha]',
    ]
    for sel in captcha_selectors:
        if page.query_selector(sel):
            return True
    return False


# ---------------------------------------------------------------------------
# Browser launch
# ---------------------------------------------------------------------------

def launch_browser(playwright, session_dir: Path):
    """Launch a persistent Chrome browser context with anti-detection measures.

    Returns the browser context and the first page.
    """
    session_dir.mkdir(parents=True, exist_ok=True)

    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(session_dir),
        channel="chrome",
        headless=False,
        slow_mo=100,
        viewport={"width": 1280, "height": 900},
        args=[
            "--disable-blink-features=AutomationControlled",
        ],
        ignore_default_args=["--enable-automation"],
    )

    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    """)

    page = context.pages[0] if context.pages else context.new_page()
    return context, page


# ---------------------------------------------------------------------------
# CLI builder
# ---------------------------------------------------------------------------

def build_arg_parser(platform_name: str, default_delay: float = DEFAULT_DELAY) -> argparse.ArgumentParser:
    """Build a standard argument parser for upload scripts."""
    parser = argparse.ArgumentParser(
        description=f"Upload POD designs to {platform_name} via browser automation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""\
Examples:
  python3 %(prog)s --folder tshirt --limit 1       # First run: log in
  python3 %(prog)s --folder tshirt --dry-run        # Preview
  python3 %(prog)s --folder tshirt --limit 50       # Upload batch
  python3 %(prog)s --folder sticker                 # Upload all
  python3 %(prog)s --folder tshirt --retry-failed   # Retry failures
""",
    )
    parser.add_argument(
        "--folder", required=True,
        help="Subfolder under output/ to upload (e.g. tshirt, sticker, poster)",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Max number of designs to upload (0 = all)",
    )
    parser.add_argument(
        "--delay", type=float, default=default_delay,
        help=f"Seconds between uploads (default: {default_delay})",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="List designs without uploading",
    )
    parser.add_argument(
        "--retry-failed", action="store_true",
        help="Only retry previously failed uploads",
    )
    parser.add_argument(
        "--shuffle", action="store_true",
        help="Interleave niches for diverse upload ordering",
    )
    parser.add_argument(
        "--source-dir",
        help="External image source directory (PNG+JSON pairs in source-dir/folder/)",
    )
    return parser


# ---------------------------------------------------------------------------
# Generic upload loop
# ---------------------------------------------------------------------------

def run_upload_loop(
    args: argparse.Namespace,
    tracker_file: Path,
    session_dir: Path,
    check_session_fn,
    wait_for_login_fn,
    upload_single_fn,
) -> None:
    """Main upload loop with circuit breaker, CAPTCHA/session recovery, and break scheduling.

    Platform scripts supply three callbacks:
        check_session_fn(page) -> bool
        wait_for_login_fn(page) -> None
        upload_single_fn(page, png_path, metadata) -> None
    """
    folder = args.folder
    limit = args.limit
    delay = args.delay
    dry_run = args.dry_run
    retry_failed = args.retry_failed

    # Discover designs
    shuffle = getattr(args, "shuffle", False)
    source_dir = Path(args.source_dir) if getattr(args, "source_dir", None) else None
    designs = discover_designs(folder, shuffle_niches=shuffle, source_dir=source_dir)
    location = str(source_dir / folder) if source_dir else f"output/{folder}/"
    if not designs:
        print(f"No designs found in {location}")
        return

    print(f"Found {len(designs)} designs in {location}")

    # Load tracker
    tracker = load_tracker(tracker_file)

    # Filter based on tracker
    to_upload = []
    for png_path, meta in designs:
        key = tracker_key(folder, png_path, source_dir=source_dir)
        entry = tracker.get(key, {})
        status = entry.get("status")

        if retry_failed and status == "failed":
            to_upload.append((png_path, meta))
        elif status == "success":
            continue
        elif not retry_failed:
            to_upload.append((png_path, meta))

    if not to_upload:
        print("No designs to upload (all already uploaded or no failures to retry).")
        return

    if limit and limit > 0:
        to_upload = to_upload[:limit]

    print(f"Will {'preview' if dry_run else 'upload'} {len(to_upload)} designs")
    print()

    if dry_run:
        for i, (png_path, meta) in enumerate(to_upload, 1):
            key = tracker_key(folder, png_path, source_dir=source_dir)
            print(f"  [{i}] {key}")
            print(f"       Title: {meta['title']}")
            print(f"       Tags:  {', '.join(meta.get('tags', []))}")
            print()
        print("Dry run complete — no uploads performed.")
        return

    # Launch browser
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        context, page = launch_browser(p, session_dir)

        # Check if session is valid
        if not check_session_fn(page):
            wait_for_login_fn(page)
            if not check_session_fn(page):
                print("Error: still not logged in. Exiting.")
                context.close()
                return

        print("Session valid — starting uploads\n")

        consecutive_failures = 0
        uploaded_count = 0
        session_start = time.time()

        for i, (png_path, meta) in enumerate(to_upload, 1):
            key = tracker_key(folder, png_path, source_dir=source_dir)
            print(f"[{i}/{len(to_upload)}] Uploading: {key}")
            print(f"  Title: {meta['title']}")

            try:
                upload_single_fn(page, png_path, meta)
                record_upload(tracker, tracker_file, key, "success")
                consecutive_failures = 0
                uploaded_count += 1
                print(f"  -> Success")

            except CaptchaError:
                print("\n=== CAPTCHA detected ===")
                print("  Solve the CAPTCHA in the browser window.")
                print("  Auto-detecting when cleared (up to 120s)...")
                captcha_cleared = False
                captcha_start = time.time()
                while time.time() - captcha_start < 120:
                    time.sleep(3)
                    if not page_has_captcha(page):
                        print("  CAPTCHA cleared!")
                        captcha_cleared = True
                        time.sleep(2)
                        break
                if captcha_cleared:
                    try:
                        upload_single_fn(page, png_path, meta)
                        record_upload(tracker, tracker_file, key, "success")
                        consecutive_failures = 0
                        uploaded_count += 1
                        print(f"  -> Success (after CAPTCHA)")
                    except Exception as e2:
                        record_upload(tracker, tracker_file, key, "failed", str(e2))
                        consecutive_failures += 1
                        print(f"  -> Failed: {e2}")
                else:
                    print("  CAPTCHA not cleared after 120s — skipping this design.")
                    record_upload(tracker, tracker_file, key, "failed", "CAPTCHA timeout")
                    consecutive_failures += 1

            except SessionExpiredError:
                print("\n=== Session expired ===")
                wait_for_login_fn(page)
                if not check_session_fn(page):
                    print("Error: still not logged in. Stopping.")
                    break
                try:
                    upload_single_fn(page, png_path, meta)
                    record_upload(tracker, tracker_file, key, "success")
                    consecutive_failures = 0
                    uploaded_count += 1
                    print(f"  -> Success (after re-login)")
                except Exception as e2:
                    record_upload(tracker, tracker_file, key, "failed", str(e2))
                    consecutive_failures += 1
                    print(f"  -> Failed: {e2}")

            except Exception as e:
                record_upload(tracker, tracker_file, key, "failed", str(e))
                consecutive_failures += 1
                print(f"  -> Failed: {e}")

            # Circuit breaker
            if consecutive_failures >= CONSECUTIVE_FAILURE_LIMIT:
                print(f"\n=== {CONSECUTIVE_FAILURE_LIMIT} consecutive failures ===")
                print("  Something may be wrong. Pausing 60s before retrying...")
                time.sleep(60)
                # Check if session is still valid
                try:
                    if not check_session_fn(page):
                        print("  Session expired during failures. Attempting re-login...")
                        wait_for_login_fn(page)
                        if not check_session_fn(page):
                            print("  Could not recover session. Stopping.")
                            break
                except Exception:
                    pass
                consecutive_failures = 0

            # Progress stats
            if uploaded_count > 0 and uploaded_count % 10 == 0:
                elapsed = time.time() - session_start
                rate = uploaded_count / (elapsed / 3600)
                remaining_count = len(to_upload) - i
                if rate > 0:
                    eta_hours = remaining_count / rate
                    if eta_hours < 1:
                        print(f"\n  --- Progress: {uploaded_count}/{len(to_upload)} done | {rate:.1f}/hr | ~{eta_hours * 60:.0f} min remaining ---\n")
                    else:
                        print(f"\n  --- Progress: {uploaded_count}/{len(to_upload)} done | {rate:.1f}/hr | ~{eta_hours:.1f} hr remaining ---\n")

            # Delay between uploads (skip after last)
            if i < len(to_upload):
                maybe_take_break(uploaded_count)
                wait_time = jittered_delay(delay)
                print(f"  Waiting {wait_time:.0f}s before next upload...")
                time.sleep(wait_time)

        # Summary
        elapsed = time.time() - session_start
        print(f"\n=== Upload session complete ===")
        print(f"  Uploaded: {uploaded_count}/{len(to_upload)}")
        if elapsed > 0 and uploaded_count > 0:
            rate = uploaded_count / (elapsed / 3600)
            print(f"  Rate:     {rate:.1f} uploads/hour")
            print(f"  Duration: {elapsed / 60:.1f} minutes")
        failed = sum(
            1 for png_path, _ in to_upload
            if tracker.get(tracker_key(folder, png_path, source_dir=source_dir), {}).get("status") == "failed"
        )
        if failed:
            print(f"  Failed:   {failed}")
            print(f"  Re-run with --retry-failed to retry")

        context.close()
