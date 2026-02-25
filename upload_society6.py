#!/usr/bin/env python3
"""Society6 auto-upload script using Playwright browser automation.

Uploads PNG designs with metadata from paired JSON files.
Uses a persistent browser session so you only log in once.
Optimized for wall art / poster uploads but works with any design folder.

Usage:
    python3 upload_society6.py --folder poster --limit 1       # First run: log in
    python3 upload_society6.py --folder poster --dry-run        # Preview
    python3 upload_society6.py --folder poster --limit 50       # Upload batch
    python3 upload_society6.py --folder tshirt                  # Upload all
    python3 upload_society6.py --folder poster --retry-failed   # Retry failures
"""

from __future__ import annotations

import time
from pathlib import Path

from upload_common import (
    SessionExpiredError,
    CaptchaError,
    UploadError,
    find_element,
    wait_for_cloudflare,
    page_has_captcha,
    build_arg_parser,
    run_upload_loop,
)

# ---------------------------------------------------------------------------
# Society6-specific constants
# ---------------------------------------------------------------------------

UPLOAD_URL = "https://society6.com/studio/upload"
SESSION_DIR = Path(__file__).parent / ".society6_session"
TRACKER_FILE = Path(__file__).parent / "uploaded_society6.json"

# Tags to strip from metadata before uploading to Society6
_PLATFORM_TAGS = frozenset({
    "redbubble", "teepublic", "print-on-demand", "pod",
})


# ---------------------------------------------------------------------------
# Tag helpers
# ---------------------------------------------------------------------------

def _clean_tags(tags: list[str]) -> list[str]:
    """Remove platform-specific tags, return up to 15 clean tags."""
    result = []
    for tag in tags:
        cleaned = tag.strip()
        if cleaned.lower() in _PLATFORM_TAGS:
            continue
        result.append(cleaned)
        if len(result) >= 15:
            break
    return result


# ---------------------------------------------------------------------------
# Society6-specific callbacks
# ---------------------------------------------------------------------------

def check_session_valid(page) -> bool:
    """Navigate to upload page and check if we're logged in."""
    try:
        page.goto(UPLOAD_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        wait_for_cloudflare(page)
        url = page.url.lower()
        if "login" in url or "sign_in" in url or "sign-in" in url or "signin" in url or "auth" in url:
            return False
        return True
    except Exception:
        return False


def wait_for_login(page) -> None:
    """Wait for the user to log in manually."""
    print("\n=== Manual login required ===")
    print("  1. Log in to your Society6 account in the browser window.")
    print("  2. Once logged in, press ENTER here to continue.")
    input("  Press ENTER when logged in... ")
    time.sleep(2)


def _fill_tags_one_by_one(page, el, tags: list[str]) -> None:
    """Fill tags by typing each one and pressing Enter (tag-widget pattern)."""
    for tag in tags:
        el.type(tag, delay=30)
        time.sleep(0.3)
        page.keyboard.press("Enter")
        time.sleep(0.3)


def _select_category(page) -> None:
    """Try to select an art/design category if a dropdown is present."""
    category_selectors = [
        'select[name*="category"]',
        'select[id*="category"]',
        '[data-testid="category-select"]',
        'select[name*="art_type"]',
    ]
    for sel in category_selectors:
        try:
            dropdown = page.query_selector(sel)
            if dropdown:
                # Prefer "Digital" or "Design" or "Illustration"; fall back to first option
                for value in ["digital", "design", "illustration", "graphic-design", "other"]:
                    try:
                        dropdown.select_option(value=value)
                        time.sleep(0.3)
                        return
                    except Exception:
                        continue
                # Try by label text
                for label in ["Digital", "Design", "Illustration", "Graphic Design", "Other"]:
                    try:
                        dropdown.select_option(label=label)
                        time.sleep(0.3)
                        return
                    except Exception:
                        continue
        except Exception:
            continue


def _handle_checkboxes(page) -> None:
    """Check any agreement/rights checkboxes on the form."""
    checkbox_selectors = [
        'input[type="checkbox"][name*="agree"]',
        'input[type="checkbox"][name*="right"]',
        'input[type="checkbox"][name*="certif"]',
        'input[type="checkbox"][name*="terms"]',
        'input[type="checkbox"][name*="original"]',
        'input[type="checkbox"][name*="own"]',
        '[data-testid="agreement-checkbox"]',
        '[data-testid="rights-checkbox"]',
    ]
    for sel in checkbox_selectors:
        try:
            cb = page.query_selector(sel)
            if cb and not cb.is_checked():
                cb.check()
                time.sleep(0.3)
        except Exception:
            continue


def upload_single(page, png_path: Path, metadata: dict) -> None:
    """Upload one design to Society6."""
    page.goto(UPLOAD_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)
    wait_for_cloudflare(page)

    # Check for login redirect
    url = page.url.lower()
    if "login" in url or "sign_in" in url or "sign-in" in url or "signin" in url:
        raise SessionExpiredError("Redirected to login — session expired")

    # --- 1. Upload the PNG via file input ---
    file_input = find_element(page, [
        'input[type="file"]',
        'input[accept*="image"]',
        '#upload-input',
        '[data-testid="upload-input"]',
        'input[name="image"]',
        'input[name="artwork"]',
        '.upload-area input[type="file"]',
        'input[name="file"]',
    ], "file upload input", timeout=15000)
    file_input.set_input_files(str(png_path))

    print("    Waiting for image processing...")
    time.sleep(10)

    # --- 2. Fill title ---
    title_el = find_element(page, [
        '#title',
        'input[name="title"]',
        'input[name="artwork[title]"]',
        '[data-testid="title-input"]',
        'input[placeholder*="title" i]',
        'input[id*="title" i]',
        'input.artwork-title',
        '#artwork_title',
    ], "title input", timeout=60000)
    title_el.click()
    title_el.fill("")
    title_el.fill(metadata["title"][:200])
    time.sleep(0.5)

    # --- 3. Fill tags/keywords ---
    tags = _clean_tags(metadata.get("tags", []))
    if tags:
        try:
            tags_el = find_element(page, [
                '#tags',
                'input[name="tags"]',
                'textarea[name="tags"]',
                'input[name="artwork[tags]"]',
                'textarea[name="artwork[tags]"]',
                '[data-testid="tags-input"]',
                'input[placeholder*="tag" i]',
                'input[id*="tag" i]',
            ], "tags input", timeout=10000)
            tags_el.click()
            tags_el.fill("")

            # Try comma-separated fill first
            tags_str = ", ".join(tags)
            tags_el.fill(tags_str)
            time.sleep(0.5)

            # Check if the field accepted it
            try:
                val = tags_el.input_value()
            except Exception:
                val = tags_str

            if len(val.strip()) < len(tags[0]):
                # Comma fill didn't stick — fall back to one-by-one
                print("    Trying tag-widget entry mode...")
                tags_el.fill("")
                _fill_tags_one_by_one(page, tags_el, tags)
        except RuntimeError:
            print("    Warning: could not find tags input, skipping tags")

    # --- 4. Fill description ---
    try:
        desc_el = find_element(page, [
            '#description',
            'textarea[name="description"]',
            'textarea[name="artwork[description]"]',
            '[data-testid="description-input"]',
            'textarea[placeholder*="description" i]',
            'textarea[id*="description" i]',
            'textarea.artwork-description',
        ], "description input", timeout=10000)
        desc_el.click()
        desc_el.fill("")
        desc_el.fill(metadata.get("description", ""))
        time.sleep(0.5)
    except RuntimeError:
        print("    Warning: could not find description input, skipping description")

    # --- 5. Select category if available ---
    _select_category(page)

    # --- 6. Check agreement/rights checkboxes ---
    _handle_checkboxes(page)

    # --- 7. Click submit ---
    save_btn = find_element(page, [
        'button[type="submit"]',
        'button[name="submit"]',
        '#submit-artwork',
        '[data-testid="submit-artwork"]',
        'button:has-text("Publish")',
        'button:has-text("Submit")',
        'button:has-text("Save")',
        'button:has-text("Upload")',
        'input[type="submit"]',
    ], "submit button", timeout=10000)
    save_btn.click()

    # Wait for navigation / confirmation
    time.sleep(5)

    # --- 8. Post-submit checks ---
    if page_has_captcha(page):
        raise CaptchaError("CAPTCHA detected")

    # Verify we moved away from /upload (success indicator)
    current_url = page.url.lower()
    if "/upload" in current_url:
        error_el = page.query_selector('.alert-error, .error-message, [role="alert"], .flash-error, .notice, .error')
        if error_el:
            raise UploadError(f"Form error: {error_el.inner_text()[:200]}")
        # Give it more time
        time.sleep(5)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_arg_parser("Society6")
    args = parser.parse_args()

    if args.limit == 0:
        args.limit = None

    run_upload_loop(
        args=args,
        tracker_file=TRACKER_FILE,
        session_dir=SESSION_DIR,
        check_session_fn=check_session_valid,
        wait_for_login_fn=wait_for_login,
        upload_single_fn=upload_single,
    )


if __name__ == "__main__":
    main()
