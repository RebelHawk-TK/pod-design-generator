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

STUDIO_URL = "https://studio.society6.com/"
UPLOAD_URL = "https://studio.society6.com/upload"
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
    """Remove platform-specific tags, return up to 10 clean tags (Society6 limit)."""
    result = []
    for tag in tags:
        cleaned = tag.strip()
        if cleaned.lower() in _PLATFORM_TAGS:
            continue
        # Society6: 20 char max per tag
        if len(cleaned) > 20:
            cleaned = cleaned[:20].strip()
        result.append(cleaned)
        if len(result) >= 10:
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
    """Wait for the user to log in manually (auto-detects when done)."""
    print("\n=== Manual login required ===")
    print("  Log in to your Society6 account in the browser window.")
    print("  Waiting for login to complete (auto-detecting)...")
    timeout = 300  # 5 minutes
    start = time.time()
    while time.time() - start < timeout:
        time.sleep(3)
        try:
            url = page.url.lower()
            if "login" not in url and "sign_in" not in url and "sign-in" not in url and "signin" not in url and "auth" not in url:
                print("  Login detected! Continuing...")
                time.sleep(2)
                return
        except Exception:
            pass
    print("  Login timeout (5 min). Continuing anyway...")
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


def _cleanup_existing_uploads(page) -> None:
    """Delete any files already on the upload page from previous attempts."""
    try:
        delete_buttons = page.get_by_text("Delete", exact=True)
        count = delete_buttons.count()
        if count > 0:
            print(f"    Cleaning up {count} existing upload(s)...")
            for _ in range(count):
                try:
                    btn = page.get_by_text("Delete", exact=True).first
                    if btn.is_visible():
                        btn.click(timeout=3000)
                        time.sleep(1)
                except Exception:
                    break
            time.sleep(1)
    except Exception:
        pass


def _upload_via_filechooser_event(page, png_path: Path) -> bool:
    """Try click-to-upload using page.on('filechooser') event listener."""
    file_chooser_ref = [None]

    def on_filechooser(fc):
        file_chooser_ref[0] = fc

    page.on("filechooser", on_filechooser)

    # Try clicking various upload trigger elements
    upload_triggers = [
        ("text 'Upload a File'", lambda: page.get_by_text("Upload a File", exact=False)),
        ("heading 'Upload a File'", lambda: page.locator("h1, h2, h3").filter(has_text="Upload")),
        ("button 'Upload'", lambda: page.get_by_role("button", name="Upload")),
    ]

    for desc, get_trigger in upload_triggers:
        try:
            trigger = get_trigger()
            if trigger.count() > 0 and trigger.first.is_visible():
                print(f"    Clicking {desc}...")
                trigger.first.click(timeout=5000)
                time.sleep(3)  # Let event loop process the filechooser event
                if file_chooser_ref[0]:
                    file_chooser_ref[0].set_files(str(png_path))
                    print("    Image uploaded via file chooser event")
                    page.remove_listener("filechooser", on_filechooser)
                    return True
        except Exception as e:
            print(f"    {desc} failed: {str(e)[:60]}")
            continue

    page.remove_listener("filechooser", on_filechooser)
    return False


def _upload_via_input_intercept(page, png_path: Path) -> bool:
    """Intercept file input creation, prevent native dialog, set files directly."""
    try:
        # Monkey-patch HTMLInputElement.click to capture file inputs without opening dialog
        page.evaluate("""() => {
            window.__capturedFileInput = null;
            const origClick = HTMLInputElement.prototype.click;
            HTMLInputElement.prototype.click = function() {
                if (this.type === 'file') {
                    window.__capturedFileInput = this;
                    // Add a marker so we can find it via Playwright
                    this.setAttribute('data-pw-captured', 'true');
                    // Don't open the native dialog
                    return;
                }
                return origClick.call(this);
            };
        }""")

        # Now click the upload area — this should create a file input and try to .click() it
        upload_triggers = [
            page.get_by_text("Upload a File", exact=False),
            page.get_by_role("button", name="Upload"),
        ]

        clicked = False
        for trigger in upload_triggers:
            try:
                if trigger.count() > 0 and trigger.first.is_visible():
                    trigger.first.click(timeout=5000)
                    clicked = True
                    break
            except Exception:
                continue

        if not clicked:
            return False

        time.sleep(1)

        # Check if we captured a file input
        captured = page.query_selector('input[data-pw-captured="true"]')
        if captured:
            captured.set_input_files(str(png_path))
            print("    Image uploaded via intercepted file input")
            # Restore original click
            page.evaluate("""() => {
                delete window.__capturedFileInput;
            }""")
            return True

        # Also check if a file input was created (even without our marker)
        file_input = page.query_selector('input[type="file"]')
        if file_input:
            file_input.set_input_files(str(png_path))
            print("    Image uploaded via dynamically created file input")
            return True

        print("    No file input captured after clicking upload area")
        return False
    except Exception as e:
        print(f"    Input intercept failed: {str(e)[:80]}")
        return False


def upload_single(page, png_path: Path, metadata: dict) -> None:
    """Upload one design to Society6."""
    page.goto(UPLOAD_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)
    wait_for_cloudflare(page)

    # Check for login redirect
    url = page.url.lower()
    if "login" in url or "sign_in" in url or "sign-in" in url or "signin" in url:
        raise SessionExpiredError("Redirected to login — session expired")

    # --- 1. Upload the PNG ---
    time.sleep(3)
    print(f"    Upload page: {page.url[:80]}")

    # First, clean up any existing uploads from previous attempts
    _cleanup_existing_uploads(page)

    # Society6 uses drag-and-drop / click-to-upload with no standard file input.
    # Try multiple approaches to get the file onto the page.
    uploaded = False

    # Approach A: Standard file input (may appear after page interaction)
    file_input = page.query_selector('input[type="file"]')
    if file_input:
        try:
            file_input.set_input_files(str(png_path))
            uploaded = True
            print("    Image uploaded via file input")
        except Exception as e:
            print(f"    File input found but failed: {e}")

    # Approach B: Use event listener + click (more reliable than expect_file_chooser)
    if not uploaded:
        uploaded = _upload_via_filechooser_event(page, png_path)

    # Approach C: Intercept file input creation and set files directly
    if not uploaded:
        uploaded = _upload_via_input_intercept(page, png_path)

    # Approach D: Check if file appeared (from a previous click that opened dialog)
    if not uploaded:
        has_file = page.evaluate("""() => {
            const text = document.body.innerText;
            return text.includes('.PNG') || text.includes('.png') ||
                   text.includes('.JPG') || text.includes('.jpg');
        }""")
        if has_file:
            print("    File already present on page from previous interaction")
            uploaded = True

    if not uploaded:
        try:
            ss_path = Path(__file__).parent / "debug_society6.png"
            page.screenshot(path=str(ss_path))
            print(f"    DEBUG: Screenshot saved to {ss_path}")
        except Exception:
            pass
        raise UploadError("Could not find upload mechanism on Society6 page")

    print("    Waiting for image processing...")
    time.sleep(15)

    debug_dir = Path(__file__).parent
    tags = _clean_tags(metadata.get("tags", []))

    # --- 2. Fill metadata (scroll to each section, use specific selectors) ---
    # Note: page has duplicate IDs — <div id="title"> in header and <input id="title"> in form
    # Use tag-qualified selectors: input#title, textarea#description, select#medium

    # Title — scroll to it and fill
    title_field = page.locator('input#title, input[name="title"]').first
    try:
        title_field.scroll_into_view_if_needed()
        time.sleep(0.3)
        title_field.click(timeout=3000)
        title_field.fill(metadata["title"][:200])
        print(f"    Title filled")
    except Exception as e:
        print(f"    Warning: title fill failed ({e})")

    # Medium dropdown
    try:
        medium = page.locator('select#medium, select[name="medium"]').first
        medium.scroll_into_view_if_needed()
        time.sleep(0.3)
        for label in ["Digital", "Design", "Illustration", "Other"]:
            try:
                medium.select_option(label=label)
                print(f"    Medium: {label}")
                break
            except Exception:
                continue
    except Exception as e:
        print(f"    Warning: could not set medium ({e})")

    # Tags (keyboard entry — unnamed text input)
    if tags:
        try:
            tag_input = page.locator('input.w-auto').first
            tag_input.scroll_into_view_if_needed()
            time.sleep(0.3)
            tag_input.click(timeout=3000)
            time.sleep(0.3)
            for tag in tags[:15]:
                page.keyboard.type(tag, delay=20)
                page.keyboard.press("Enter")
                time.sleep(0.2)
            print(f"    Tags: {len(tags)} entered")
            page.keyboard.press("Escape")
            time.sleep(0.3)
        except Exception as e:
            print(f"    Warning: could not fill tags ({e})")

    # Subject (required — Headless UI chip-select, pick up to 2)
    try:
        subject_btn = page.get_by_text("Select subject(s)", exact=False).first
        subject_btn.scroll_into_view_if_needed()
        time.sleep(0.3)
        subject_btn.click(timeout=3000)
        time.sleep(1)
        # Click chip-style subject options (visible after dropdown opens)
        selected = 0
        for subject in ["Architecture", "Landscape", "Nature", "Travel"]:
            if selected >= 2:
                break
            try:
                chip = page.get_by_text(subject, exact=True)
                if chip.count() > 0 and chip.first.is_visible():
                    chip.first.click(timeout=2000)
                    time.sleep(0.3)
                    selected += 1
                    print(f"    Subject: {subject}")
            except Exception:
                continue
        # Close dropdown
        page.keyboard.press("Escape")
        time.sleep(0.3)
    except Exception as e:
        print(f"    Warning: subject selection failed ({e})")

    # Description
    desc_field = page.locator('textarea#description, textarea[name="description"]').first
    try:
        desc_field.scroll_into_view_if_needed()
        time.sleep(0.3)
        desc_field.click(timeout=3000)
        desc_field.fill(metadata.get("description", ""))
        print(f"    Description filled")
    except Exception as e:
        print(f"    Warning: description fill failed ({e})")

    # Agreement checkbox — the input is invisible, must interact carefully
    try:
        agree_cb = page.locator('input#agreementCheckbox')
        agree_cb.scroll_into_view_if_needed(timeout=5000)
        time.sleep(0.3)
        if not agree_cb.is_checked():
            # Try clicking the label wrapper (the visible custom checkbox UI)
            page.evaluate("""() => {
                const cb = document.querySelector('#agreementCheckbox');
                if (cb) {
                    // Find the visible label/wrapper that users click
                    const label = cb.closest('label') || cb.parentElement?.querySelector('label')
                        || document.querySelector('label[for="agreementCheckbox"]');
                    if (label) {
                        label.click();
                        return 'label';
                    }
                    // Direct click + React compat
                    cb.click();
                    return 'direct';
                }
                return 'not found';
            }""")
            time.sleep(0.5)
            # Verify
            if not agree_cb.is_checked():
                # Force via JS
                page.evaluate("""() => {
                    const cb = document.querySelector('#agreementCheckbox');
                    if (cb) {
                        const nativeSetter = Object.getOwnPropertyDescriptor(
                            HTMLInputElement.prototype, 'checked'
                        ).set;
                        nativeSetter.call(cb, true);
                        cb.dispatchEvent(new Event('click', {bubbles: true}));
                        cb.dispatchEvent(new Event('change', {bubbles: true}));
                        cb.dispatchEvent(new Event('input', {bubbles: true}));
                    }
                }""")
                time.sleep(0.3)
            is_checked = agree_cb.is_checked()
            print(f"    Agreement: {'checked' if is_checked else 'STILL UNCHECKED'}")
    except Exception as e:
        print(f"    Warning: agreement failed ({e})")

    # Mature content — click the visible "No" label text
    try:
        # Scroll to mature content section first
        mature_section = page.get_by_text("Does this artwork contain mature content?")
        if mature_section.count() > 0:
            mature_section.first.scroll_into_view_if_needed()
            time.sleep(0.3)
        # Click the visible "No" text label (not the hidden radio)
        no_label = page.locator('label[for="matureContentNo"]')
        if no_label.count() > 0:
            no_label.first.scroll_into_view_if_needed()
            time.sleep(0.2)
            no_label.first.click(timeout=3000)
            print(f"    Mature content: No (via label)")
        else:
            # Fallback: click "No" text near mature content
            no_text = page.get_by_text("No", exact=True)
            for i in range(no_text.count()):
                el = no_text.nth(i)
                if el.is_visible():
                    parent_text = el.evaluate("el => el.parentElement?.textContent?.slice(0, 50) || ''")
                    if "mature" not in parent_text.lower():
                        continue
                    el.click(timeout=2000)
                    print(f"    Mature content: No (via text)")
                    break
    except Exception as e:
        print(f"    Warning: mature content failed ({e})")

    time.sleep(2)

    # Full-page screenshot for debugging
    try:
        page.screenshot(path=str(debug_dir / "debug_s6_form_filled.png"), full_page=True)
    except Exception:
        pass

    # --- 3. Click "Save And Add Products" ---
    pre_url = page.url
    try:
        save_btn = page.get_by_role("button", name="Save And Add Products")
        if save_btn.count() > 0:
            save_btn.first.scroll_into_view_if_needed()
            time.sleep(0.5)

            # Check if button is enabled
            is_disabled = save_btn.first.is_disabled()
            if is_disabled:
                # Dump field values for debugging
                field_state = page.evaluate("""() => {
                    const title = document.querySelector('input[name="title"]');
                    const desc = document.querySelector('textarea[name="description"]');
                    const medium = document.querySelector('select[name="medium"]');
                    const agreement = document.querySelector('#agreementCheckbox');
                    const matureNo = document.querySelector('#matureContentNo');
                    // Check for subject selections
                    const subjectChips = document.querySelectorAll('[data-headlessui-state] [class*="bg-black"]');
                    // Check for any red error messages
                    const redTexts = Array.from(document.querySelectorAll('.text-red-500, .text-red-600, [class*="error"], [class*="red"]'))
                        .map(el => el.textContent?.trim().slice(0, 60))
                        .filter(t => t && t.length > 0);
                    return {
                        title: title?.value || '',
                        desc: (desc?.value || '').slice(0, 50),
                        medium: medium?.value || '',
                        agreement: agreement?.checked || false,
                        matureNo: matureNo?.checked || false,
                        subjects: subjectChips.length,
                        redErrors: redTexts.slice(0, 5),
                    };
                }""")
                print(f"    WARNING: Save button disabled. Fields: {field_state}")
                # Try force-clicking anyway to see server-side errors
                print(f"    Attempting force-click on disabled Save button...")
                save_btn.first.click(force=True, timeout=5000)
                time.sleep(5)

            save_btn.first.click(timeout=10000)
            print(f"    Clicked 'Save And Add Products'")
            time.sleep(10)
        else:
            raise UploadError("'Save And Add Products' button not found")
    except UploadError:
        raise
    except Exception as e:
        raise UploadError(f"Could not click Save button: {e}")

    # --- 4. Post-submit verification ---
    try:
        page.screenshot(path=str(debug_dir / "debug_s6_after_submit.png"))
    except Exception:
        pass

    if page_has_captcha(page):
        raise CaptchaError("CAPTCHA detected")

    current_url = page.url.lower()
    print(f"    Post-submit URL: {page.url[:80]}")

    # Check for error messages
    errors = page.evaluate("""() => {
        const errorEls = document.querySelectorAll(
            '.alert-error, .error-message, [role="alert"], .flash-error, .text-red-500, .text-red-600, [class*="error"]'
        );
        return Array.from(errorEls).map(el => el.innerText.trim()).filter(t => t.length > 0).slice(0, 5);
    }""")
    if errors:
        print(f"    Page errors: {errors}")

    # Success: URL changed away from upload page
    if current_url != pre_url.lower() and "upload" not in current_url:
        print(f"    Navigated to: {page.url[:80]}")
        return

    # Success: page shows enable products / product added
    page_text = page.evaluate("() => document.body.innerText.slice(0, 2000)").lower()
    if any(word in page_text for word in ["product added", "artwork saved", "enable products", "select products"]):
        return

    # If still on upload page, this is a failure
    if "upload" in current_url:
        raise UploadError(f"Still on upload page after submit. Errors: {errors or 'none detected'}")


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
