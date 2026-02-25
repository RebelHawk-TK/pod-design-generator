#!/usr/bin/env python3
"""Redbubble auto-upload script using Playwright browser automation.

Uploads PNG designs with metadata from paired JSON files.
Uses a persistent browser session so you only log in once.

Usage:
    python3 upload.py --folder tshirt --limit 1       # First run: log in manually
    python3 upload.py --folder tshirt --dry-run        # Preview without uploading
    python3 upload.py --folder tshirt --limit 50       # Upload batch
    python3 upload.py --folder sticker                 # Upload all
    python3 upload.py --folder tshirt --retry-failed   # Retry failures
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
# Redbubble-specific constants
# ---------------------------------------------------------------------------

UPLOAD_URL = "https://www.redbubble.com/portfolio/images/new"
SESSION_DIR = Path(__file__).parent / ".redbubble_session"
TRACKER_FILE = Path(__file__).parent / "uploaded.json"


# ---------------------------------------------------------------------------
# Redbubble-specific callbacks
# ---------------------------------------------------------------------------

def check_session_valid(page) -> bool:
    """Navigate to upload page and check if we're logged in."""
    try:
        page.goto(UPLOAD_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        wait_for_cloudflare(page)
        url = page.url.lower()
        if "login" in url or "sign_in" in url or "auth" in url:
            return False
        return True
    except Exception:
        return False


def wait_for_login(page) -> None:
    """Wait for the user to log in manually."""
    print("\n=== Manual login required ===")
    print("  1. Log in to your Redbubble account in the browser window.")
    print("  2. Once logged in, press ENTER here to continue.")
    input("  Press ENTER when logged in... ")
    time.sleep(2)


def upload_single(page, png_path: Path, metadata: dict) -> None:
    """Upload one design to Redbubble."""
    page.goto(UPLOAD_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)
    wait_for_cloudflare(page)

    # Check for login redirect
    if "login" in page.url.lower() or "sign_in" in page.url.lower():
        raise SessionExpiredError("Redirected to login — session expired")

    # Upload the PNG via file input
    file_input = find_element(page, [
        'input[type="file"]',
        'input[accept*="image"]',
        '#upload-input',
        '[data-testid="upload-input"]',
    ], "file upload input", timeout=15000)
    file_input.set_input_files(str(png_path))

    # Wait for image processing / form to appear
    print("    Waiting for image processing...")
    time.sleep(8)

    # Wait for the title field to become available (indicates form is ready)
    title_el = find_element(page, [
        '#work_title_en',
        'input[name="work[title]"]',
        'input[name="title"]',
        '[data-testid="title-input"]',
        'input[placeholder*="title" i]',
        '#work_title',
    ], "title input", timeout=60000)

    # Fill title
    title_el.click()
    title_el.fill("")
    title_el.fill(metadata["title"][:200])
    time.sleep(0.5)

    # Filter and prepare tags
    FILLER_TAGS = {
        "and", "the", "but", "first", "led", "for", "with", "design",
        "niche", "print-on-demand", "pod", "redbubble", "typography",
    }
    raw_tags = metadata.get("tags", [])
    clean_tags = [t for t in raw_tags if t.lower() not in FILLER_TAGS]
    if not clean_tags:
        clean_tags = raw_tags  # fallback to originals if all filtered

    # Pick main tag: first tag that's a meaningful keyword
    main_tag = clean_tags[0] if clean_tags else ""

    # Fill Main Tag (contenteditable span with pill UI)
    main_tag_filled = False
    try:
        main_tag_el = find_element(page, [
            '#main-tag-en',
            'span#main-tag-en[contenteditable="true"]',
        ], "main tag input", timeout=10000)
        main_tag_el.click()
        time.sleep(0.3)
        page.keyboard.type(main_tag, delay=30)
        page.keyboard.press("Enter")
        time.sleep(0.5)
        main_tag_filled = True
        print(f"    Main tag: {main_tag}")
    except RuntimeError:
        print("    Warning: could not find main tag input")

    # Fill Supporting Tags (contenteditable span with pill UI)
    secondary_tags = clean_tags[1:14] if main_tag_filled else clean_tags[:14]  # max 14 supporting
    try:
        tags_el = find_element(page, [
            '#supporting-tags-en',
            'span#supporting-tags-en[contenteditable="true"]',
        ], "supporting tags input", timeout=10000)
        tags_el.click()
        time.sleep(0.3)
        for tag in secondary_tags:
            page.keyboard.type(tag, delay=30)
            page.keyboard.press("Enter")
            time.sleep(0.3)
        print(f"    Supporting tags: {len(secondary_tags)} entered")
    except RuntimeError:
        print("    Warning: could not find supporting tags input, skipping tags")

    # Fill description and submit via JS to avoid tag suggestion dropdown blocking clicks
    description = metadata.get("description", "")
    page.evaluate("""(desc) => {
        // Dismiss tag suggestions
        document.activeElement?.blur();
        document.querySelectorAll('*').forEach(el => {
            if (el.className && typeof el.className === 'string' && el.className.includes('suggestion')) {
                el.style.display = 'none';
            }
        });

        // Fill description
        const descEl = document.querySelector('#work_description_en')
            || document.querySelector('textarea[name="work[description_en]"]')
            || document.querySelector('textarea[name="work[description]"]');
        if (descEl) {
            descEl.value = desc;
            descEl.dispatchEvent(new Event('input', {bubbles: true}));
            descEl.dispatchEvent(new Event('change', {bubbles: true}));
        }

        // Check rights checkbox if present (id='rightsDeclaration')
        const checkbox = document.querySelector('#rightsDeclaration');
        if (checkbox && !checkbox.checked) {
            checkbox.checked = true;
            checkbox.dispatchEvent(new Event('change', {bubbles: true}));
        }
    }""", description)
    time.sleep(0.5)

    # Select "Not Mature" (safe for work = true)
    page.keyboard.press("Escape")
    time.sleep(0.3)

    # Click the radio for mature content
    page.evaluate("""() => {
        const radio = document.querySelector('#work_safe_for_work_true');
        if (radio) radio.scrollIntoView({block: 'center'});
    }""")
    time.sleep(0.5)
    page.locator('#work_safe_for_work_true').click(force=True, timeout=5000)
    time.sleep(0.5)
    print("    Mature content: No (safe for work)")

    # Check agreement checkbox (id='rightsDeclaration')
    page.locator('#rightsDeclaration').scroll_into_view_if_needed()
    time.sleep(0.3)
    page.locator('#rightsDeclaration').check(force=True, timeout=5000)
    time.sleep(0.3)
    print("    Agreement: checked")

    # Click the "Save work" submit button
    page.locator('#submit-work').scroll_into_view_if_needed()
    time.sleep(0.5)
    page.locator('#submit-work').click(timeout=10000)

    # Wait for navigation / confirmation
    time.sleep(8)

    # Check for CAPTCHA
    if page_has_captcha(page):
        raise CaptchaError("CAPTCHA detected")

    # Detect server errors (500, 502, 503, etc.)
    page_title = page.title().lower()
    page_text = page.inner_text("body")[:1000].lower() if page.query_selector("body") else ""

    server_error_signals = [
        "500" in page_title and "error" in page_title,
        "server error" in page_title,
        "computer says 'no'" in page_text,
        "500 server error" in page_text,
        "502 bad gateway" in page_text,
        "503 service" in page_text,
        "sorry" in page_title and "error" in page_title,
    ]
    if any(server_error_signals):
        raise UploadError(f"Server error page detected (title: {page.title()[:100]})")

    # Detect "work could not be saved" errors
    if "could not be saved" in page_text or "must have at least one image" in page_text:
        raise UploadError(f"Redbubble rejected upload: {page_text[:200]}")

    # Verify we moved away from the upload page (success indicator)
    current_url = page.url.lower()
    if "/images/new" in current_url:
        # Only detect VISIBLE error elements (hidden ones are pre-existing placeholders)
        visible_error = page.evaluate("""() => {
            const selectors = ['.alert-error', '.error-message', '[role="alert"]'];
            for (const sel of selectors) {
                for (const el of document.querySelectorAll(sel)) {
                    const style = getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    if (style.display !== 'none' && style.visibility !== 'hidden'
                        && rect.width > 0 && rect.height > 0) {
                        const text = el.textContent?.trim();
                        if (text) return text.slice(0, 200);
                    }
                }
            }
            return null;
        }""")
        if visible_error:
            raise UploadError(f"Form error: {visible_error}")
        # Still on upload page with no visible error — likely didn't save
        time.sleep(5)
        if "/images/new" in page.url.lower():
            raise UploadError("Upload may have failed — still on upload page after submission")

    # Positive confirmation: check we landed on an edit/success page
    final_url = page.url.lower()
    if "/works/" not in final_url and "/images/" not in final_url and "/images/new" not in final_url:
        # Could be a redirect to an unexpected page
        if "error" in final_url or "sorry" in final_url:
            raise UploadError(f"Redirected to error page: {page.url[:200]}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_arg_parser("Redbubble")
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
