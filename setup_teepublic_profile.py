#!/usr/bin/env python3
"""Upload profile image and banner to TeePublic store."""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from upload_common import launch_browser, wait_for_cloudflare

SESSION_DIR = Path(__file__).parent / ".teepublic_session"
LOGO_PATH = Path(__file__).parent / "shopify_logo.png"
BANNER_PATH = Path(__file__).parent / "shopify_banner.png"

with sync_playwright() as p:
    context, page = launch_browser(p, SESSION_DIR)

    page.goto("https://www.teepublic.com/user/modern-design-concept",
              wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)
    wait_for_cloudflare(page)

    # Find file inputs and identify them by parent context
    input_info = page.evaluate("""() => {
        const inputs = document.querySelectorAll('input[type="file"]');
        return Array.from(inputs).map((inp, idx) => {
            // Walk up to find context
            let el = inp;
            let context = '';
            for (let i = 0; i < 10 && el; i++) {
                el = el.parentElement;
                if (!el) break;
                const cls = typeof el.className === 'string' ? el.className.toLowerCase() : '';
                if (cls.includes('banner') || cls.includes('cover')) { context = 'banner'; break; }
                if (cls.includes('avatar') || cls.includes('logo') || cls.includes('profile')) { context = 'avatar'; break; }
            }
            return {idx, context};
        });
    }""")
    print("File inputs:")
    for info in input_info:
        print(f"  [{info['idx']}] context={info['context']}")

    file_inputs = page.locator('input[type="file"]')
    total = file_inputs.count()
    print(f"Total: {total}")

    # Upload based on context, or fallback to order
    banner_done = False
    avatar_done = False

    for info in input_info:
        idx = info['idx']
        ctx = info['context']
        if ctx == 'banner' and not banner_done:
            print(f"\nUploading banner to input [{idx}]...")
            file_inputs.nth(idx).set_input_files(str(BANNER_PATH))
            banner_done = True
            time.sleep(5)
        elif ctx == 'avatar' and not avatar_done:
            print(f"\nUploading avatar to input [{idx}]...")
            file_inputs.nth(idx).set_input_files(str(LOGO_PATH))
            avatar_done = True
            time.sleep(5)

    # Fallback if context detection didn't work
    if not banner_done and total >= 1:
        print(f"\nUploading banner to input [0] (fallback)...")
        file_inputs.nth(0).set_input_files(str(BANNER_PATH))
        banner_done = True
        time.sleep(5)

    if not avatar_done and total >= 2:
        print(f"\nUploading avatar to input [1] (fallback)...")
        file_inputs.nth(1).set_input_files(str(LOGO_PATH))
        avatar_done = True
        time.sleep(5)

    page.screenshot(path="/tmp/teepublic_after_uploads.png")
    print(f"\nBanner: {'done' if banner_done else 'failed'}")
    print(f"Avatar: {'done' if avatar_done else 'failed'}")

    # Look for any save/apply/confirm buttons that appeared
    time.sleep(2)
    for text in ["Save", "Apply", "Confirm", "Upload", "Done"]:
        btn = page.locator(f'button:has-text("{text}"):visible')
        if btn.count() > 0:
            btn.first.click(timeout=5000)
            print(f"Clicked '{text}' button")
            time.sleep(3)

    time.sleep(3)
    page.screenshot(path="/tmp/teepublic_profile_final.png")
    print("Done!")
    context.close()
