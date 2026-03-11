#!/usr/bin/env python3
"""Debug Redbubble upload — take screenshots at each step."""

from pathlib import Path
from upload_common import launch_browser, wait_for_cloudflare, find_element
import time

SESSION_DIR = Path(__file__).parent / ".redbubble_session"
UPLOAD_URL = "https://www.redbubble.com/portfolio/images/new"
SOURCE = Path.home() / "Documents/Claude/landmark-style-transfer-unified/output/poster"

# Pick first image
png = sorted(SOURCE.glob("*.png"))[0]
import json
meta = json.loads(png.with_suffix(".json").read_text())

print(f"Image: {png.name} ({png.stat().st_size / 1024 / 1024:.1f}MB)")
print(f"Title: {meta['title']}")

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    context, page = launch_browser(p, SESSION_DIR)

    page.goto(UPLOAD_URL, wait_until="domcontentloaded", timeout=30000)
    try:
        page.wait_for_load_state("networkidle", timeout=20000)
    except Exception:
        pass
    time.sleep(2)
    wait_for_cloudflare(page)

    url = page.url.lower()
    if "login" in url or "sign_in" in url:
        print("Login required — log in and press ENTER")
        input("Press ENTER...")
        page.goto(UPLOAD_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

    page.screenshot(path="debug_01_upload_page.png")
    print("1. Upload page loaded")

    # Upload file
    file_input = find_element(page, ['input[type="file"]', 'input[accept*="image"]'], "file input", timeout=30000)
    file_input.set_input_files(str(png))
    print("2. File selected, waiting for processing...")

    # Wait longer for large file
    time.sleep(10)
    try:
        page.wait_for_load_state("networkidle", timeout=60000)
    except Exception:
        pass
    time.sleep(5)

    page.screenshot(path="debug_02_after_file.png")
    print("3. After file processing")

    # Check if title field appeared
    title_el = find_element(page, [
        '#work_title_en', 'input[name="work[title]"]', 'input[name="title"]',
    ], "title input", timeout=60000)

    title_el.click()
    title_el.fill("")
    title_el.fill(meta["title"][:200])
    time.sleep(0.5)

    page.screenshot(path="debug_03_after_title.png")
    print("4. Title filled")

    # Fill main tag
    try:
        main_tag_el = find_element(page, ['#main-tag-en'], "main tag", timeout=10000)
        main_tag_el.click()
        time.sleep(0.3)
        page.keyboard.type(meta["tags"][0], delay=30)
        page.keyboard.press("Enter")
        time.sleep(0.5)
        print(f"5. Main tag: {meta['tags'][0]}")
    except Exception as e:
        print(f"5. Main tag failed: {e}")

    # Fill supporting tags
    try:
        tags_el = find_element(page, ['#supporting-tags-en'], "tags", timeout=10000)
        tags_el.click()
        time.sleep(0.3)
        for tag in meta["tags"][1:14]:
            page.keyboard.type(tag, delay=30)
            page.keyboard.press("Enter")
            time.sleep(0.3)
        print(f"6. Supporting tags entered: {len(meta['tags'][1:14])}")
    except Exception as e:
        print(f"6. Tags failed: {e}")

    # Fill description + check rights
    page.evaluate("""(desc) => {
        document.activeElement?.blur();
        const descEl = document.querySelector('#work_description_en')
            || document.querySelector('textarea[name="work[description_en]"]');
        if (descEl) {
            descEl.value = desc;
            descEl.dispatchEvent(new Event('input', {bubbles: true}));
            descEl.dispatchEvent(new Event('change', {bubbles: true}));
        }
    }""", meta.get("description", ""))
    time.sleep(0.5)
    print("7. Description filled")

    # SFW radio
    page.keyboard.press("Escape")
    time.sleep(0.3)
    page.evaluate("() => { const r = document.querySelector('#work_safe_for_work_true'); if (r) r.scrollIntoView({block: 'center'}); }")
    time.sleep(0.5)
    page.locator('#work_safe_for_work_true').click(force=True, timeout=5000)
    time.sleep(0.5)
    print("8. SFW checked")

    # Rights checkbox
    page.locator('#rightsDeclaration').scroll_into_view_if_needed()
    time.sleep(0.3)
    page.locator('#rightsDeclaration').check(force=True, timeout=5000)
    time.sleep(0.3)
    print("9. Rights checked")

    page.screenshot(path="debug_04_before_submit.png")
    print("10. Screenshot before submit")

    # Check form validity
    form_state = page.evaluate("""() => {
        const form = document.querySelector('form');
        if (!form) return {error: 'no form found'};

        // Check for visible errors
        const errors = [];
        document.querySelectorAll('.error, .field_with_errors, .alert-error, [role="alert"]').forEach(el => {
            const style = getComputedStyle(el);
            if (style.display !== 'none' && style.visibility !== 'hidden') {
                errors.push(el.textContent?.trim().slice(0, 100));
            }
        });

        // Check submit button state
        const submitBtn = document.querySelector('#submit-work');
        const disabled = submitBtn?.disabled;
        const btnText = (submitBtn?.value || submitBtn?.textContent || '').trim();

        // Check if image was uploaded successfully
        const uploadProgress = document.querySelector('.upload-progress, .progress-bar, [class*="progress"]');
        const progressText = uploadProgress?.textContent?.trim().slice(0, 100);

        return {
            errors,
            submitDisabled: disabled,
            submitText: btnText,
            progressText,
            formAction: form.action,
        };
    }""")
    print(f"11. Form state: {json.dumps(form_state, indent=2)}")

    # Click submit
    page.locator('#submit-work').scroll_into_view_if_needed()
    time.sleep(0.5)
    page.locator('#submit-work').click(timeout=10000)
    print("12. Submit clicked")

    # Wait and take screenshots at intervals
    for i, wait in enumerate([3, 5, 10], 1):
        time.sleep(wait)
        page.screenshot(path=f"debug_05_after_submit_{i}.png")
        print(f"13.{i}. URL after {sum([3,5,10][:i])}s: {page.url}")
        if "/images/new" not in page.url.lower():
            print("  -> Navigated away! Upload likely succeeded.")
            break

    # Final state
    page.screenshot(path="debug_06_final.png")
    print(f"\n14. Final URL: {page.url}")
    print(f"    Final title: {page.title()}")

    # Check page content for errors
    body_text = page.inner_text("body")[:500] if page.query_selector("body") else ""
    print(f"    Body preview: {body_text[:200]}")

    context.close()
    print("\nDone — check debug_*.png screenshots")
