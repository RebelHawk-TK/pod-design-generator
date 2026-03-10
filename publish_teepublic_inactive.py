#!/usr/bin/env python3
"""Bulk-publish inactive TeePublic designs.

Uses design IDs extracted from upload logs to visit each edit page and publish.

Usage:
    python3 publish_teepublic_inactive.py              # Publish all known inactive
    python3 publish_teepublic_inactive.py --limit 5    # Publish up to 5
    python3 publish_teepublic_inactive.py --dry-run    # Preview only
    python3 publish_teepublic_inactive.py --ids 123 456  # Publish specific IDs
"""

from __future__ import annotations

import argparse
import re
import time
from pathlib import Path

from upload_common import launch_browser, wait_for_cloudflare
from upload_teepublic import _set_product_colors

SESSION_DIR = Path(__file__).parent / ".teepublic_session"
LOG_FILE = Path(__file__).parent / "logs" / "com.moderndesignconcept.pod-upload-teepublic.log"


def extract_design_ids_from_logs() -> list[str]:
    """Extract unique design IDs from TeePublic upload logs."""
    ids = set()
    if LOG_FILE.exists():
        text = LOG_FILE.read_text()
        for m in re.finditer(r'/designs/(\d+)/edit', text):
            ids.add(m.group(1))
    return sorted(ids)


def check_design_status(page, design_id: str) -> str:
    """Visit a design's edit page and return its status: 'inactive', 'active', or 'unknown'."""
    url = f"https://www.teepublic.com/designs/{design_id}/edit"
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)
    wait_for_cloudflare(page)

    # Check if page loaded correctly
    if "/edit" not in page.url:
        return "not_found"

    status = page.evaluate("""() => {
        const buttons = document.querySelectorAll('button, input[type="submit"]');
        for (const b of buttons) {
            const text = b.textContent?.trim()?.toLowerCase() || b.value?.toLowerCase() || '';
            const cls = b.className?.toLowerCase() || '';
            // Check class-based status
            if (cls.includes('design-published'))
                return 'active';
            if (cls.includes('publish-and-promote'))
                return 'inactive';
            // Check text-based status
            if (text.includes('unpublish') || text.includes('deactivate'))
                return 'active';
            if (text === 'publish' || (text.includes('publish') && !text.includes('unpublish') && !text.includes('save')))
                return 'inactive';
        }
        // Fallback: check if the save button says "Save All Changes" (published)
        // vs "Save as Draft" or has publish-and-promote button (inactive)
        const saveBtn = document.querySelector('.save-publish-later-button');
        if (saveBtn) {
            const cls = saveBtn.className?.toLowerCase() || '';
            if (cls.includes('design-published'))
                return 'active';
        }
        const publishBtn = document.querySelector('.publish-and-promote-button');
        if (publishBtn)
            return 'inactive';
        return 'unknown';
    }""")
    return status


def _find_metadata_for_design(page, design_id: str) -> dict:
    """Try to find metadata JSON for a design by matching its artwork filename."""
    import json
    import glob

    # Check tracker for the design key
    tracker_file = Path(__file__).parent / "uploaded_teepublic.json"
    if tracker_file.exists():
        tracker = json.loads(tracker_file.read_text())
        for key, entry in tracker.items():
            # The key looks like "ext:output/tshirt/amsterdam_canals_cafe_terrace"
            # The design ID is not stored, but we can use the key to find metadata
            base = key.replace("ext:", "")
            # Try both phase directories
            for phase_dir in [
                Path("/Users/rebelhawk/Documents/Claude/landmark-style-transfer/"),
                Path("/Users/rebelhawk/Documents/Claude/landmark-style-transfer-phase2/"),
            ]:
                json_path = phase_dir / f"{base}.json"
                if json_path.exists():
                    meta = json.loads(json_path.read_text())
                    return meta
    return {}


def publish_design(page, design_id: str, all_metadata: dict = None) -> bool:
    """Publish a design by its ID. Returns True on success."""
    url = f"https://www.teepublic.com/designs/{design_id}/edit"
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)
    wait_for_cloudflare(page)

    if "/edit" not in page.url:
        print(f"    Design {design_id} edit page not found (redirected to {page.url})")
        return False

    # Fill missing metadata (title, description, tags)
    current_title = page.evaluate("() => document.querySelector('#design_design_title')?.value || ''")
    if not current_title.strip():
        # Try to get title from the page itself or use a fallback
        fallback_title = f"Landmark Art Print - Modern Design Concept #{design_id}"
        page.evaluate("""(title) => {
            const el = document.querySelector('#design_design_title');
            if (el) { el.value = title; el.dispatchEvent(new Event('input', {bubbles:true})); }
        }""", fallback_title)
        print(f"    Set fallback title: {fallback_title[:60]}")

    current_desc = page.evaluate("() => document.querySelector('#design_design_description')?.value || ''")
    if not current_desc.strip():
        fallback_desc = "Beautiful landmark art in classic painting style. Perfect for art lovers and travel enthusiasts. Makes a great gift!"
        page.evaluate("""(desc) => {
            const el = document.querySelector('#design_design_description');
            if (el) { el.value = desc; el.dispatchEvent(new Event('input', {bubbles:true})); }
        }""", fallback_desc)
        print(f"    Set fallback description")

    # Primary tag
    current_ptag = page.evaluate("() => document.querySelector('#design_primary_tag')?.value || ''")
    if not current_ptag.strip():
        page.evaluate("""() => {
            const el = document.querySelector('#design_primary_tag');
            if (el) { el.value = 'painted-style'; el.dispatchEvent(new Event('input', {bubbles:true})); }
        }""")
        time.sleep(0.3)
        page.keyboard.press("Escape")
        time.sleep(0.3)
        page.evaluate("() => document.activeElement?.blur()")
        time.sleep(0.3)
        print(f"    Set primary tag: painted-style")

    # Check Terms and Conditions checkbox
    page.evaluate("""() => {
        const tc = document.getElementById('terms');
        if (tc) { tc.checked = true; tc.dispatchEvent(new Event('change', {bubbles:true})); }
    }""")
    time.sleep(0.5)

    # Select "No" for content flag (mature content) — required field
    page.evaluate("""() => {
        const no = document.getElementById('design_content_flag_false');
        if (no) { no.checked = true; no.dispatchEvent(new Event('change', {bubbles:true})); }
    }""")
    time.sleep(0.5)

    # Add secondary tags (required for publish)
    fallback_tags = ["art", "travel", "landmark", "wall art", "gift"]
    try:
        taggle_input = page.locator('#secondary_tags .taggle_input')
        if taggle_input.count() > 0:
            taggle_input.first.scroll_into_view_if_needed()
            time.sleep(0.3)
            taggle_input.first.click(force=True, timeout=5000)
            time.sleep(0.3)
            for tag in fallback_tags:
                page.keyboard.type(tag, delay=30)
                page.keyboard.press("Enter")
                time.sleep(0.3)
            print(f"    Added {len(fallback_tags)} secondary tags")
            page.keyboard.press("Escape")
            time.sleep(0.3)
            page.evaluate("() => document.activeElement?.blur()")
            time.sleep(0.3)
    except Exception as e:
        print(f"    Warning: could not set secondary tags: {e}")

    # Set default product colors (required for publish)
    _set_product_colors(page)

    # Set commit=publish in form
    page.evaluate("""() => {
        const form = document.querySelector('form[id^="edit_design"]');
        if (!form) return;
        let commitInput = form.querySelector('input[name="commit"]');
        if (!commitInput) {
            commitInput = document.createElement('input');
            commitInput.type = 'hidden';
            commitInput.name = 'commit';
            form.appendChild(commitInput);
        }
        commitInput.value = 'publish';
    }""")

    # Find and scroll to publish button
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

    # Listen for validation alert dialogs
    dialog_messages = []
    def handle_dialog(dialog):
        dialog_messages.append(dialog.message)
        try:
            dialog.accept()
        except Exception:
            pass  # Already handled by Playwright auto-dismiss
    page.on("dialog", handle_dialog)

    # Click publish button
    publish_btn = page.locator('button.publish-and-promote-button')
    if publish_btn.count() == 0 or not publish_btn.first.is_visible():
        print(f"    No publish button found — may already be published")
        page.remove_listener("dialog", handle_dialog)
        return False

    publish_btn.first.click(timeout=5000)
    time.sleep(5)

    page.remove_listener("dialog", handle_dialog)

    if dialog_messages:
        print(f"    Validation errors: {dialog_messages[0][:200]}")
        return False

    time.sleep(10)

    # Verify: reload and check if publish button is gone
    page.reload(wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    still_unpublished = page.evaluate("""() => {
        const buttons = document.querySelectorAll('button, input[type="submit"]');
        for (const b of buttons) {
            const text = b.textContent?.trim()?.toLowerCase() || b.value?.toLowerCase() || '';
            if (text === 'publish' || (text.includes('publish') && !text.includes('unpublish')))
                return true;
        }
        return false;
    }""")

    if still_unpublished:
        # Take debug screenshot
        page.screenshot(path=f"/tmp/teepublic_publish_fail_{design_id}.png")

    return not still_unpublished


def main():
    parser = argparse.ArgumentParser(description="Bulk-publish inactive TeePublic designs")
    parser.add_argument("--limit", type=int, default=0, help="Max designs to publish (0=all)")
    parser.add_argument("--dry-run", action="store_true", help="Check status without publishing")
    parser.add_argument("--ids", nargs="+", help="Specific design IDs to publish")
    args = parser.parse_args()

    if args.ids:
        design_ids = args.ids
    else:
        design_ids = extract_design_ids_from_logs()

    if not design_ids:
        print("No design IDs found. Pass --ids or check log file exists.")
        return

    print(f"Found {len(design_ids)} design ID(s) from logs")

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        context, page = launch_browser(p, SESSION_DIR)

        try:
            # Check session
            page.goto("https://www.teepublic.com/user/account", wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
            wait_for_cloudflare(page)

            if "login" in page.url.lower() or "sign_in" in page.url.lower():
                print("\n=== Manual login required ===")
                print("  Log in to TeePublic in the browser window.")
                input("  Press ENTER when logged in... ")
                time.sleep(2)

            # First pass: check which designs are actually inactive
            print("\n=== Checking design status ===")
            inactive = []
            for i, did in enumerate(design_ids):
                status = check_design_status(page, did)
                label = f"  [{i+1}/{len(design_ids)}] Design {did}: {status}"
                print(label)
                if status == "inactive":
                    inactive.append(did)
                time.sleep(1)

            print(f"\n{len(inactive)} inactive design(s) found")

            if not inactive:
                print("Nothing to publish!")
                return

            if args.dry_run:
                print("\n(Dry run — no changes made)")
                return

            limit = args.limit if args.limit > 0 else len(inactive)
            to_publish = inactive[:limit]

            print(f"\n=== Publishing {len(to_publish)} design(s) ===")
            published = 0
            failed = 0

            for i, did in enumerate(to_publish):
                print(f"\n[{i+1}/{len(to_publish)}] Publishing design {did}...")
                try:
                    ok = publish_design(page, did)
                    if ok:
                        print(f"  -> Published!")
                        published += 1
                    else:
                        print(f"  -> Failed to publish")
                        failed += 1
                except Exception as e:
                    print(f"  -> Error: {e}")
                    failed += 1

                if i < len(to_publish) - 1:
                    time.sleep(3)

            print(f"\n=== Done: {published} published, {failed} failed ===")

        finally:
            context.close()


if __name__ == "__main__":
    main()
