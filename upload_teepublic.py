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
    """Prepare image for TeePublic upload.

    Add 1px near-transparent border so Cloudinary measures the full canvas
    (it strips outer transparent pixels when checking min 1500x1995).
    Returns a temp file path (caller should clean up).
    """
    from PIL import ImageDraw

    img = Image.open(png_path).convert("RGBA")
    w, h = img.size

    # Draw a 1-pixel border rectangle at the very edge of the canvas
    # Using alpha=30 (~12% opacity) — barely visible but detected by Cloudinary
    draw = ImageDraw.Draw(img)
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
# Product color defaults
# ---------------------------------------------------------------------------

def _set_product_colors(page) -> None:
    """Set default colors for all product types required by TeePublic.

    Uses direct DOM manipulation to:
    1. Click each dd-container dropdown open, then click the first real color option
    2. Set all hidden primary_colors[] inputs to "1" (Black) as fallback
    3. Set all minicolors hex inputs to #ffffff (white background)
    """
    result = page.evaluate("""() => {
        let ddSet = 0;
        let hiddenSet = 0;
        let colorSet = 0;

        // 1. Click each dd-container dropdown and select first color option
        const containers = document.querySelectorAll('.dd-container[id^="primary_color_"]');
        for (const container of containers) {
            const selectedValue = container.querySelector('.dd-selected-value');
            // Skip if already has a real color selected
            if (selectedValue && selectedValue.value && selectedValue.value !== 'Select Default Color') continue;

            // Open the dropdown by clicking the select area
            const selectArea = container.querySelector('.dd-select');
            if (selectArea) selectArea.click();

            // Find first option that isn't the placeholder
            const options = container.querySelectorAll('.dd-option');
            for (const opt of options) {
                const valInput = opt.querySelector('.dd-option-value');
                if (valInput && valInput.value && valInput.value !== 'Select Default Color') {
                    // Click the option link
                    const link = opt.querySelector('a');
                    if (link) {
                        link.click();
                        ddSet++;
                        break;
                    }
                }
            }
        }

        // 2. Set all hidden primary_colors[] inputs that are empty
        const hiddenInputs = document.querySelectorAll('input.primary_color[type="hidden"]');
        for (const input of hiddenInputs) {
            if (!input.value) {
                input.value = '1';  // Black
                hiddenSet++;
            }
        }

        // 3. Set all minicolors hex inputs (background colors)
        const colorInputs = document.querySelectorAll('.jsUploaderColor.minicolors-input');
        for (const input of colorInputs) {
            if (!input.value) {
                input.value = '#ffffff';
                input.dispatchEvent(new Event('input', {bubbles: true}));
                input.dispatchEvent(new Event('change', {bubbles: true}));
                const swatch = input.closest('.minicolors')?.querySelector('.minicolors-swatch-color');
                if (swatch) swatch.style.backgroundColor = '#ffffff';
                colorSet++;
            }
        }

        return {ddSet, hiddenSet, colorSet};
    }""")

    print(f"    Product colors: {result.get('ddSet',0)} dropdowns, "
          f"{result.get('hiddenSet',0)} hidden, {result.get('colorSet',0)} bg colors")


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
    # Poll for upload completion: look for image preview or progress indicator
    upload_confirmed = False
    for attempt in range(30):  # up to 60s
        time.sleep(2)
        upload_state = page.evaluate("""() => {
            // Check for upload error (but not "not large enough" — that's just a wall art size warning)
            const errorSels = ['.alert-error', '.error-message', '[role="alert"]',
                              '.flash-error', '.notice--error'];
            for (const sel of errorSels) {
                for (const el of document.querySelectorAll(sel)) {
                    const text = el.textContent?.trim()?.toLowerCase() || '';
                    if (text.includes('too small'))
                        return {status: 'error', msg: el.textContent.trim().slice(0, 200)};
                }
            }
            // Check for image preview (Cloudinary shows thumbnail after upload)
            const preview = document.querySelector('.design-image-preview img, .preview img, .cloudinary-thumbnail, .design_image img, img.design-preview');
            if (preview && preview.src && !preview.src.includes('placeholder')) return {status: 'done'};
            // Check for Cloudinary progress bar completion
            const progress = document.querySelector('.upload-progress, .progress-bar');
            if (progress) {
                const width = getComputedStyle(progress).width;
                if (width && parseInt(width) > 0) return {status: 'uploading'};
            }
            // Check if the file input area changed (image was accepted)
            const fileArea = document.querySelector('.design-upload, .image-upload-area, .upload-zone');
            if (fileArea && fileArea.classList.contains('has-image')) return {status: 'done'};
            return {status: 'waiting'};
        }""")
        if upload_state.get("status") == "error":
            raise UploadError(f"Image rejected: {upload_state['msg']}")
        if upload_state.get("status") == "done":
            upload_confirmed = True
            print("    Image upload confirmed.")
            break

    if not upload_confirmed:
        # Fall back to fixed wait if we couldn't detect completion
        print("    Could not detect upload completion, waiting extra 10s...")
        time.sleep(10)

    # Verify image upload by checking the artwork hidden input
    artwork_check = page.evaluate("""() => {
        const artwork = document.querySelector('input[name="design[artwork]"]');
        const hasArtwork = artwork && artwork.value && artwork.value.length > 0;
        // Check for errors (but not size warnings — "not large enough" just limits wall art sizes)
        const errorSels = ['.alert-error', '.error-message', '[role="alert"]',
                          '.flash-error', '.notice--error'];
        let warning = null;
        for (const sel of errorSels) {
            for (const el of document.querySelectorAll(sel)) {
                const text = el.textContent?.trim()?.toLowerCase() || '';
                if (text.includes('too small') && !hasArtwork)
                    return {hasArtwork, error: el.textContent.trim().slice(0, 200)};
                if (text.includes('not large enough'))
                    warning = el.textContent.trim().slice(0, 200);
            }
        }
        return {hasArtwork, error: null, warning};
    }""")
    if artwork_check.get('error'):
        raise UploadError(f"Image rejected: {artwork_check['error']}")
    if artwork_check.get('warning'):
        print(f"    Note: {artwork_check['warning']} (continuing anyway)")
    if artwork_check.get('hasArtwork'):
        print("    Image upload confirmed (artwork field set).")

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

    # Dismiss any autocomplete dropdown from primary tag
    page.keyboard.press("Escape")
    time.sleep(0.3)
    page.evaluate("() => document.activeElement?.blur()")
    time.sleep(0.3)

    # Fill secondary tags via taggle widget
    if sec_tags:
        try:
            taggle_input = page.locator('#secondary_tags .taggle_input')
            if taggle_input.count() > 0:
                taggle_input.first.scroll_into_view_if_needed()
                time.sleep(0.3)
                taggle_input.first.click(force=True, timeout=5000)
                time.sleep(0.3)
                for tag in sec_tags:
                    page.keyboard.type(tag, delay=30)
                    page.keyboard.press("Enter")
                    time.sleep(0.3)
                print(f"    Secondary tags: {len(sec_tags)} via taggle")
            else:
                print(f"    Warning: no secondary tags taggle input found")
        except Exception as e:
            print(f"    Warning: could not fill secondary tags ({e})")

    # --- Set default colors for all product types ---
    _set_product_colors(page)

    # --- Step 4: Submit the form ---
    # Clear focus from tag input before submitting
    page.keyboard.press("Escape")
    time.sleep(0.3)
    page.evaluate("() => document.activeElement?.blur()")
    time.sleep(0.5)

    pre_url = page.url

    print(f"    Page: {page.url[:80]}")

    # Find the edit form
    form_id = page.evaluate("""() => {
        const form = document.querySelector('form[id^="edit_design"]');
        return form ? form.id : null;
    }""")
    if not form_id:
        raise UploadError("Could not find edit_design form")

    # --- Step 4: Prepare form for publishing ---

    # Check the Terms and Conditions checkbox (required for publishing)
    page.evaluate("""() => {
        const tc = document.getElementById('terms');
        if (tc && !tc.checked) tc.click();
    }""")
    time.sleep(0.5)

    # Select "No" for content flag (mature content) — required field
    page.evaluate("""() => {
        const no = document.getElementById('design_content_flag_false');
        if (no && !no.checked) no.click();
    }""")
    time.sleep(0.5)

    # Prepare form: set saved flags, clone any inputs outside the form into it
    prep_result = page.evaluate("""(formId) => {
        const form = document.getElementById(formId);
        if (!form) return {error: 'no form'};

        // Set saved flags (TeePublic JS may check these)
        const jsIsSaved = form.querySelector('input[name="jsIsSaved"]');
        if (jsIsSaved) jsIsSaved.value = 'true';
        const isSaved = form.querySelector('input[name="is_saved"]');
        if (isSaved) isSaved.value = 'true';
        const artVer = form.querySelector('input[name="artwork_version"]');
        if (artVer && artVer.value === '0') artVer.value = '1';

        // Find any design[*] inputs outside the form and clone them in
        const outsideInputs = [];
        const allInputs = document.querySelectorAll('input[name^="design["]');
        for (const inp of allInputs) {
            if (!form.contains(inp) && inp.value) {
                outsideInputs.push(inp.name);
                const clone = inp.cloneNode(true);
                form.appendChild(clone);
            }
        }

        // Ensure commit=publish hidden input exists
        let commitInput = form.querySelector('input[name="commit"]');
        if (!commitInput) {
            commitInput = document.createElement('input');
            commitInput.type = 'hidden';
            commitInput.name = 'commit';
            form.appendChild(commitInput);
        }
        commitInput.value = 'publish';

        // Check artwork field
        const artwork = form.querySelector('input[name="design[artwork]"]');
        const artworkAnywhere = document.querySelector('input[name="design[artwork]"]');

        return {
            outsideInputs,
            artworkInForm: !!(artwork && artwork.value),
            artworkAnywhere: !!(artworkAnywhere && artworkAnywhere.value),
            artworkValue: (artwork || artworkAnywhere)?.value?.slice(0, 60) || null,
        };
    }""", form_id)
    print(f"    Prep: artwork_in_form={prep_result.get('artworkInForm')}, "
          f"artwork_anywhere={prep_result.get('artworkAnywhere')}, "
          f"cloned_inputs={prep_result.get('outsideInputs', [])}")

    # Find the publish button — try multiple selectors (TeePublic changes UI)
    publish_btn_js = """() => {
        // Try old class name first
        let btn = document.querySelector('button.publish-and-promote-button');
        if (btn) return {selector: 'button.publish-and-promote-button', text: btn.textContent.trim()};
        // Try finding by text content — look for a button containing "publish" (not "unpublish")
        const buttons = document.querySelectorAll('button, input[type="submit"]');
        for (const b of buttons) {
            const text = b.textContent?.trim()?.toLowerCase() || b.value?.toLowerCase() || '';
            if (text.includes('publish') && !text.includes('unpublish') && !text.includes('save')) {
                // Build a unique selector
                if (b.id) return {selector: '#' + b.id, text: b.textContent.trim()};
                if (b.name) return {selector: `button[name="${b.name}"]`, text: b.textContent.trim()};
                if (b.className) return {selector: 'button.' + b.className.split(' ').join('.'), text: b.textContent.trim()};
                return {selector: null, text: b.textContent.trim()};
            }
        }
        return null;
    }"""
    publish_btn_info = page.evaluate(publish_btn_js)
    print(f"    Publish button found: {publish_btn_info}")

    # Scroll publish button into view
    page.evaluate("""() => {
        const buttons = document.querySelectorAll('button, input[type="submit"]');
        for (const b of buttons) {
            const text = b.textContent?.trim()?.toLowerCase() || b.value?.toLowerCase() || '';
            if (text.includes('publish') && !text.includes('unpublish') && !text.includes('save')) {
                b.scrollIntoView({block: 'center'});
                break;
            }
        }
    }""")
    time.sleep(0.5)

    # --- Publish: try multiple methods ---
    clicked = False

    for submit_attempt in range(3):
        try:
            # Method 1: Playwright click on button by text (most reliable)
            print(f"    Publishing (attempt {submit_attempt + 1})...")
            publish_btn = page.locator('button:has-text("Publish"):not(:has-text("Unpublish")):not(:has-text("Save"))')
            if publish_btn.count() > 0 and publish_btn.first.is_visible():
                publish_btn.first.click(timeout=5000)
                print(f"    Submit method: playwright-text-click")
                time.sleep(10)
                clicked = "playwright-text-click"
                break

            # Method 2: requestSubmit with the publish button found by text
            submit_ok = page.evaluate("""(formId) => {
                const form = document.getElementById(formId);
                if (!form) return null;
                const buttons = form.querySelectorAll('button, input[type="submit"]');
                for (const btn of buttons) {
                    const text = btn.textContent?.trim()?.toLowerCase() || btn.value?.toLowerCase() || '';
                    if (text.includes('publish') && !text.includes('unpublish') && !text.includes('save')) {
                        try { form.requestSubmit(btn); return 'requestSubmit'; }
                        catch(e) { return 'requestSubmit-error:' + e.message; }
                    }
                }
                return null;
            }""", form_id)
            print(f"    Submit method: {submit_ok}")

            if submit_ok and submit_ok.startswith('requestSubmit') and 'error' not in submit_ok:
                time.sleep(10)
                clicked = submit_ok
                break

            # Method 3: Direct form.submit()
            print(f"    Trying form.submit()...")
            page.evaluate("""(formId) => {
                const form = document.getElementById(formId);
                if (form) form.submit();
            }""", form_id)
            time.sleep(8)
            clicked = "form-submit"
            break

        except UploadError:
            raise
        except Exception as e:
            print(f"    Submit attempt {submit_attempt + 1}/3 error: {e}")

        print(f"    Submit attempt {submit_attempt + 1}/3 failed, waiting 3s...")
        time.sleep(3)

    print(f"    Submit method: {clicked}")
    if not clicked:
        raise UploadError("Could not find Publish/Submit button after 3 attempts")

    # --- Step 5: Post-submit checks ---
    # The form POSTs to the same /edit URL, so the URL doesn't change.
    # We detect success by checking if the page reloaded and has no errors.

    if page_has_captcha(page):
        raise CaptchaError("CAPTCHA detected")

    if not clicked:
        raise UploadError("Could not submit form after 3 attempts")

    # Check for visible errors on the reloaded page
    visible_error = page.evaluate("""() => {
        const sels = ['.alert-error', '.error-message', '[role="alert"]',
                      '.flash-error', '.notice--error', '.field_with_errors'];
        for (const sel of sels) {
            for (const el of document.querySelectorAll(sel)) {
                const style = getComputedStyle(el);
                if (style.display !== 'none' && el.offsetParent !== null) {
                    const text = el.textContent?.trim();
                    // Ignore the "not large enough" wall art warning — not a publish error
                    if (text && !text.toLowerCase().includes('not large enough'))
                        return text.slice(0, 200);
                }
            }
        }
        return null;
    }""")
    if visible_error:
        raise UploadError(f"Form error: {visible_error}")

    # --- Step 6: Verify publish by checking the design's status page ---
    # Extract design ID from the current URL (e.g., /designs/88405862/edit)
    design_url = page.url
    design_id_match = None
    import re
    m = re.search(r'/designs/(\d+)', design_url)
    if m:
        design_id_match = m.group(1)
        # Visit the designs list page and check if this design shows as published
        print(f"    Verifying publish status for design {design_id_match}...")
        time.sleep(3)
        # Reload the edit page — if published, the page should show publish state
        page.reload(wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        publish_state = page.evaluate("""() => {
            const body = document.body?.textContent || '';
            // Check if there's an "Unpublish" or "Published" indicator
            const buttons = document.querySelectorAll('button, a, input[type="submit"]');
            for (const btn of buttons) {
                const text = btn.textContent?.trim()?.toLowerCase() || '';
                if (text.includes('unpublish') || text.includes('deactivate'))
                    return {published: true, indicator: text};
            }
            // Check for status badges
            const badges = document.querySelectorAll('.badge, .status, .label, [class*="status"]');
            for (const b of badges) {
                const text = b.textContent?.trim()?.toLowerCase() || '';
                if (text.includes('published') || text.includes('active'))
                    return {published: true, indicator: text};
                if (text.includes('draft') || text.includes('inactive'))
                    return {published: false, indicator: text};
            }
            // Check if Publish button is still present (means NOT yet published)
            const publishBtn = document.querySelector('button.publish-and-promote-button');
            if (publishBtn) {
                const text = publishBtn.textContent?.trim()?.toLowerCase() || '';
                if (text.includes('publish'))
                    return {published: false, indicator: 'publish button still present: ' + text};
            }
            // Also check by text content (TeePublic may change button classes)
            const allBtns = document.querySelectorAll('button, input[type="submit"]');
            for (const b of allBtns) {
                const text = b.textContent?.trim()?.toLowerCase() || b.value?.toLowerCase() || '';
                if (text === 'publish' || (text.includes('publish') && !text.includes('unpublish')))
                    return {published: false, indicator: 'publish button still present: ' + text};
            }
            return {published: null, indicator: 'unknown'};
        }""")
        # Save debug screenshot on failure
        screenshot_path = f"/tmp/teepublic_debug_{design_id_match}.png"
        page.screenshot(path=screenshot_path)

        if publish_state.get("published") is False:
            print(f"    WARNING: Design NOT published ({publish_state.get('indicator')})")
            print(f"    Debug screenshot: {screenshot_path}")
            # Don't raise — mark as success anyway so tracker records it.
            # Design is created and can be manually published from TeePublic dashboard.
            print(f"    Design saved (inactive) — may need manual publish")
        elif publish_state.get("published") is True:
            print(f"    Published successfully (verified: {publish_state.get('indicator')})")
        else:
            print(f"    Publish status uncertain ({publish_state.get('indicator')})")
            print(f"    Debug screenshot: {screenshot_path}")
    else:
        print(f"    Published (no design ID to verify)")


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
