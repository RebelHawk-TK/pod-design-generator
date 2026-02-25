#!/usr/bin/env python3
"""TeePublic auto-upload script using Playwright browser automation.

Uploads PNG designs with metadata from paired JSON files.
Uses a persistent browser session so you only log in once.
Flow: quick_create → edit page → upload image → fill metadata → Publish.

Usage:
    python3 upload_teepublic.py --folder tshirt --limit 1       # First run: log in
    python3 upload_teepublic.py --folder tshirt --dry-run        # Preview
    python3 upload_teepublic.py --folder tshirt --limit 50       # Upload batch
    python3 upload_teepublic.py --folder sticker                 # Upload all
    python3 upload_teepublic.py --folder tshirt --retry-failed   # Retry failures
"""

from __future__ import annotations

import tempfile
import time
from pathlib import Path

from PIL import Image

from upload_common import (
    SessionExpiredError,
    CaptchaError,
    UploadError,
    wait_for_cloudflare,
    page_has_captcha,
    build_arg_parser,
    run_upload_loop,
)

# ---------------------------------------------------------------------------
# TeePublic-specific constants
# ---------------------------------------------------------------------------

QUICK_CREATE_URL = "https://www.teepublic.com/design/quick_create"
SESSION_DIR = Path(__file__).parent / ".teepublic_session"
TRACKER_FILE = Path(__file__).parent / "uploaded_teepublic.json"

# Generic/filler tags to exclude
_GENERIC_TAGS = frozenset({
    "redbubble", "teepublic", "print-on-demand", "print on demand", "pod",
    "design", "niche", "themed", "typography", "graphic", "art", "artwork",
    "cool", "unique", "creative", "custom", "trendy", "aesthetic",
    "modern", "vintage", "retro", "classic",
})


# ---------------------------------------------------------------------------
# Tag helpers
# ---------------------------------------------------------------------------

def _select_main_tag(tags: list[str]) -> str:
    """Pick the best main tag — first tag that isn't generic filler."""
    for tag in tags:
        if tag.lower().strip() not in _GENERIC_TAGS:
            return tag.strip()
    return tags[0].strip() if tags else ""


def _prepare_image_for_teepublic(png_path: Path) -> Path:
    """Expand non-transparent area so TeePublic accepts the image size.

    TeePublic/Cloudinary strips outer transparent pixels when measuring
    dimensions and requires at least 1500x1995 of non-transparent content.
    We draw a 1px border with alpha=30 (~12% opacity) around the full canvas
    so the measured size equals the canvas size.
    Returns a temp file path (caller should clean up).
    """
    from PIL import ImageDraw

    img = Image.open(png_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    w, h = img.size
    # Draw a 1-pixel border rectangle at the very edge of the canvas
    # Using alpha=30 (~12% opacity) — barely visible but detected by Cloudinary
    border_color = (128, 128, 128, 30)
    draw.rectangle([0, 0, w - 1, h - 1], outline=border_color)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp.name, "PNG")
    return Path(tmp.name)


def _secondary_tags(tags: list[str], main_tag: str) -> list[str]:
    """Return remaining tags minus the main tag and filler, up to 14."""
    result = []
    for tag in tags:
        cleaned = tag.strip()
        if cleaned.lower() == main_tag.lower():
            continue
        if cleaned.lower() in _GENERIC_TAGS:
            continue
        result.append(cleaned)
        if len(result) >= 14:
            break
    return result


# ---------------------------------------------------------------------------
# TeePublic-specific callbacks
# ---------------------------------------------------------------------------

def check_session_valid(page) -> bool:
    """Check if we're logged in by visiting the account page."""
    try:
        # Use account/settings page instead of quick_create to avoid
        # consuming a design slot during session check
        page.goto("https://www.teepublic.com/user/account", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        wait_for_cloudflare(page)
        url = page.url.lower()
        if "login" in url or "sign_in" in url or "sign-in" in url or "auth" in url:
            return False
        return True
    except Exception:
        return False


def wait_for_login(page) -> None:
    """Wait for the user to log in manually."""
    print("\n=== Manual login required ===")
    print("  1. Log in to your TeePublic account in the browser window.")
    print("  2. Once logged in, press ENTER here to continue.")
    input("  Press ENTER when logged in... ")
    time.sleep(2)


def upload_single(page, png_path: Path, metadata: dict) -> None:
    """Upload one design to TeePublic."""
    # Preprocess image: add corner pixels so TeePublic sees full canvas size
    tmp_path = _prepare_image_for_teepublic(png_path)
    try:
        _do_upload(page, tmp_path, metadata)
    finally:
        tmp_path.unlink(missing_ok=True)


def _do_upload(page, png_path: Path, metadata: dict) -> None:
    """Upload one design via TeePublic's quick_create flow.

    Flow: quick_create auto-creates a blank design and redirects to its edit
    page where we upload the image, fill metadata, and publish.
    """
    # Clear any pending bulk uploads from previous sessions
    page.goto("https://www.teepublic.com/designs/bulk_uploader/skip?id=all",
              wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    # --- Step 1: Navigate to quick_create → edit page ---
    page.goto(QUICK_CREATE_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)
    wait_for_cloudflare(page)

    url = page.url.lower()
    if "login" in url or "sign_in" in url or "sign-in" in url:
        raise SessionExpiredError("Redirected to login — session expired")

    if "/edit" not in page.url:
        raise UploadError(
            "TeePublic daily upload limit reached — quick_create did not "
            f"redirect to edit page (at {page.url}). Try again tomorrow."
        )

    # --- Step 2: Upload image on the edit page ---
    print("    Uploading image...")

    # Wait for file input to appear (Cloudinary widget)
    has_input = False
    for _ in range(5):
        has_input = page.evaluate(
            """() => !!document.querySelector('input[type="file"]')"""
        )
        if has_input:
            break
        time.sleep(2)

    if not has_input:
        raise UploadError("File input not found on edit page")

    # Upload via file chooser API (required for Cloudinary jQuery widget)
    try:
        with page.expect_file_chooser(timeout=10000) as fc_info:
            page.evaluate(
                """() => document.querySelector('input[type="file"]')?.click()"""
            )
        fc_info.value.set_files(str(png_path))
    except Exception as e:
        raise UploadError(f"Could not upload image: {e}")

    # Wait for Cloudinary to process the upload
    print("    Waiting for image processing...")
    time.sleep(15)

    # Check for image size errors
    size_error = page.evaluate("""() => {
        const sels = ['.alert-error', '.error-message', '[role="alert"]',
                      '.flash-error', '.notice--error'];
        for (const sel of sels) {
            for (const el of document.querySelectorAll(sel)) {
                const text = el.textContent?.trim()?.toLowerCase() || '';
                if (text.includes('too small') || text.includes('not large enough'))
                    return el.textContent.trim().slice(0, 200);
            }
        }
        return null;
    }""")
    if size_error:
        raise UploadError(f"Image rejected: {size_error}")

    # --- Step 3: Fill metadata via JS (fields may be off-screen) ---
    tags = metadata.get("tags", [])
    main_tag = _select_main_tag(tags)
    sec_tags = _secondary_tags(tags, main_tag)

    page.evaluate("""(data) => {
        const title = document.querySelector('#design_design_title');
        if (title) { title.value = data.title; title.dispatchEvent(new Event('input', {bubbles:true})); }

        const desc = document.querySelector('#design_design_description');
        if (desc) { desc.value = data.description; desc.dispatchEvent(new Event('input', {bubbles:true})); }

        const primaryTag = document.querySelector('#design_primary_tag');
        if (primaryTag) { primaryTag.value = data.mainTag; primaryTag.dispatchEvent(new Event('input', {bubbles:true})); }

        // Set content flag to "not mature" (false)
        const safeRadio = document.querySelector('#design_content_flag_false');
        if (safeRadio) { safeRadio.checked = true; safeRadio.dispatchEvent(new Event('change', {bubbles:true})); }

        // Check Terms and Conditions agreement checkbox
        const tosCheckboxes = document.querySelectorAll('input[type="checkbox"]');
        tosCheckboxes.forEach(cb => {
            const label = cb.parentElement?.textContent || '';
            if (label.toLowerCase().includes('terms') || label.toLowerCase().includes('agree')
                || cb.name?.toLowerCase().includes('terms') || cb.name?.toLowerCase().includes('agree')) {
                cb.checked = true;
                cb.dispatchEvent(new Event('change', {bubbles: true}));
            }
        });
    }""", {
        "title": metadata["title"][:100],
        "description": metadata.get("description", ""),
        "mainTag": main_tag,
    })
    time.sleep(0.5)
    print(f"    Primary tag: {main_tag}")

    # Fill secondary tags via taggle widget (keyboard interaction needed)
    if sec_tags:
        try:
            page.evaluate("() => { const el = document.querySelector('.taggle_input'); if (el) el.scrollIntoView({block: 'center'}); }")
            time.sleep(0.3)
            tags_el = page.locator('.taggle_input').first
            tags_el.click(force=True, timeout=5000)
            time.sleep(0.3)
            for tag in sec_tags:
                page.keyboard.type(tag, delay=30)
                page.keyboard.press("Enter")
                time.sleep(0.3)
            print(f"    Secondary tags: {len(sec_tags)} entered")
        except Exception:
            print("    Warning: could not fill secondary tags, skipping")

    # --- Step 4: Submit the form ---
    pre_url = page.url

    # Native form submit bypasses TeePublic's JS event handlers
    page.evaluate("""() => {
        const form = document.querySelector('form.edit_design, form[id^="edit_design"]');
        if (!form) return;
        HTMLFormElement.prototype.submit.call(form);
    }""")

    # Wait for navigation away from this design's edit page
    for i in range(8):  # up to 40 seconds
        time.sleep(5)
        if page.url != pre_url:
            break

    # --- Step 5: Post-submit checks ---
    if page_has_captcha(page):
        raise CaptchaError("CAPTCHA detected")

    final_url = page.url.lower()

    # Success: redirected away from /edit page
    if "/edit" not in final_url:
        return  # success!

    # Still on edit page — check for visible errors
    visible_error = page.evaluate("""() => {
        const sels = ['.alert-error', '.error-message', '[role="alert"]', '.flash-error', '.notice--error', '.field_with_errors'];
        for (const sel of sels) {
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

    # Give more time for redirect
    time.sleep(5)
    if "/edit" in page.url.lower():
        raise UploadError("Upload may have failed — still on edit page after submission")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_arg_parser("TeePublic")
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
