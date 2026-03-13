#!/usr/bin/env python3
"""Update TikTok profile picture and bio via Playwright.

Uses the existing persistent Chrome session from the upload scripts.

Usage:
    python3 update_tiktok_profile.py              # Update both logo and bio
    python3 update_tiktok_profile.py --logo-only   # Just update profile picture
    python3 update_tiktok_profile.py --bio-only    # Just update bio
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from upload_common import wait_for_cloudflare

PROJECT_DIR = Path(__file__).parent
CHROME_PROFILE_DIR = PROJECT_DIR / ".chrome_profile"
LOGO_PATH = PROJECT_DIR / "app_icon.png"

BIO_TEXT = (
    "AI-powered art meets world landmarks 🎨🌍\n"
    "Prints, posters & tees for art lovers\n"
    "moderndesignconcept.com"
)

def check_session(page) -> bool:
    """Check if logged into TikTok."""
    try:
        page.goto("https://www.tiktok.com", wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)
        wait_for_cloudflare(page)
        return "/login" not in page.url
    except Exception:
        return False


def wait_for_login(page) -> None:
    """Prompt user to log in manually."""
    print("\n=== TikTok Login Required ===")
    print("  Log into your TikTok account in the browser window.")
    print("  Waiting up to 5 minutes...\n")
    page.goto("https://www.tiktok.com/login", wait_until="domcontentloaded", timeout=30000)
    deadline = time.time() + 300
    while time.time() < deadline:
        time.sleep(5)
        if "/login" not in page.url and "tiktok.com" in page.url:
            print("  Login detected!")
            time.sleep(3)
            return
    print("  Login timeout — please try again.")


def navigate_to_edit_profile(page) -> bool:
    """Navigate to the Edit Profile modal/page from the user's profile."""
    # First go to the user's own profile page
    page.goto("https://www.tiktok.com/profile", wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)
    wait_for_cloudflare(page)

    # Look for "Edit profile" button on the profile page
    edit_selectors = [
        '[data-e2e="edit-profile-button"]',
        'button:has-text("Edit profile")',
        'a:has-text("Edit profile")',
        'span:has-text("Edit profile")',
        '[class*="edit-profile"]',
        'div[role="button"]:has-text("Edit profile")',
    ]

    for sel in edit_selectors:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                page.evaluate("el => el.click()", el)
                print(f"  Opened edit profile via: {sel}")
                time.sleep(3)
                return True
        except Exception:
            continue

    # Fallback: try JS search for any element containing "Edit profile"
    try:
        clicked = page.evaluate("""() => {
            const els = document.querySelectorAll('button, a, div[role="button"], span');
            for (const el of els) {
                if (el.textContent.trim() === 'Edit profile') {
                    el.click();
                    return true;
                }
            }
            return false;
        }""")
        if clicked:
            print(f"  Opened edit profile via JS fallback")
            time.sleep(3)
            return True
    except Exception:
        pass

    print(f"  Could not find Edit profile button")
    page.screenshot(path=str(PROJECT_DIR / "debug_tiktok_profile_page.png"))
    return False


def update_profile_picture(page, logo_path: Path) -> bool:
    """Upload a new profile picture from the Edit Profile modal."""
    print(f"\n=== Updating profile picture ===")
    print(f"  Logo: {logo_path}")

    if not logo_path.exists():
        print(f"  Error: logo file not found: {logo_path}")
        return False

    # We should already be on the edit profile modal/page
    # Look for the avatar/photo edit area within the modal
    photo_selectors = [
        '[data-e2e="change-photo"]',
        '[data-e2e="edit-avatar"]',
        'span:has-text("Change photo")',
        'div:has-text("Change photo")',
        'button:has-text("Change photo")',
        'img[class*="avatar"]',
        '[class*="avatar-wrapper"]',
        '[class*="edit-photo"]',
        '[class*="profile-photo"]',
    ]

    # Click the avatar area to trigger file upload
    photo_clicked = False
    for sel in photo_selectors:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                page.evaluate("el => el.click()", el)
                photo_clicked = True
                print(f"  Clicked photo area via: {sel}")
                time.sleep(3)
                break
        except Exception:
            continue

    if not photo_clicked:
        # Try clicking on any image that looks like an avatar (circular, small)
        try:
            clicked = page.evaluate("""() => {
                const imgs = document.querySelectorAll('img');
                for (const img of imgs) {
                    const rect = img.getBoundingClientRect();
                    if (rect.width > 50 && rect.width < 200 && rect.height > 50 && rect.height < 200) {
                        const style = window.getComputedStyle(img);
                        if (style.borderRadius.includes('50%') || style.borderRadius.includes('9999')) {
                            img.click();
                            return true;
                        }
                    }
                }
                // Also try any element with "avatar" in class
                const avatars = document.querySelectorAll('[class*="avatar"], [class*="Avatar"]');
                for (const av of avatars) {
                    if (av.offsetWidth > 50) {
                        av.click();
                        return true;
                    }
                }
                return false;
            }""")
            if clicked:
                photo_clicked = True
                print(f"  Clicked avatar via JS heuristic")
                time.sleep(3)
        except Exception:
            pass

    # Look for file input (may be present already or appear after click)
    time.sleep(2)
    file_input = page.locator('input[type="file"][accept*="image"]')
    if file_input.count() == 0:
        file_input = page.locator('input[type="file"]')

    if file_input.count() > 0:
        file_input.first.set_input_files(str(logo_path))
        print(f"  Logo file selected, waiting for upload...")
        time.sleep(5)

        # Look for Apply/Save button on crop dialog
        apply_selectors = [
            'button:has-text("Apply")',
            'button:has-text("Save")',
            'button:has-text("Confirm")',
            'button:has-text("Done")',
        ]
        for sel in apply_selectors:
            try:
                el = page.query_selector(sel)
                if el and el.is_visible():
                    page.evaluate("el => el.click()", el)
                    print(f"  Confirmed crop via: {sel}")
                    time.sleep(3)
                    break
            except Exception:
                continue

        print(f"  Profile picture updated!")
        return True
    else:
        print(f"  Could not find file input for profile picture.")
        page.screenshot(path=str(PROJECT_DIR / "debug_tiktok_profile.png"))
        return False


def update_bio(page, bio_text: str) -> bool:
    """Update the TikTok profile bio from the Edit Profile modal."""
    print(f"\n=== Updating bio ===")

    # We should already be on the edit profile modal/page
    # Find the bio textarea/input
    bio_selectors = [
        'textarea[placeholder*="Bio"]',
        'textarea[placeholder*="bio"]',
        '[data-e2e="bio-input"]',
        'textarea[name="bio"]',
        'textarea[class*="bio"]',
        'div[class*="bio"] textarea',
        'textarea',
    ]

    bio_el = None
    for sel in bio_selectors:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                bio_el = el
                print(f"  Found bio field via: {sel}")
                break
        except Exception:
            continue

    if not bio_el:
        # Fallback: find textarea via JS
        try:
            found = page.evaluate("""() => {
                const textareas = document.querySelectorAll('textarea');
                for (const ta of textareas) {
                    if (ta.offsetHeight > 0) return true;
                }
                return false;
            }""")
            if found:
                bio_el = page.query_selector('textarea')
                print(f"  Found bio field via JS fallback")
        except Exception:
            pass

    if bio_el:
        # Clear existing bio and type new one
        page.evaluate("el => el.click()", bio_el)
        time.sleep(0.5)
        page.keyboard.press("Meta+A")
        page.keyboard.press("Backspace")
        time.sleep(0.3)

        # Type bio line by line (use Shift+Enter for newlines within the field)
        lines = bio_text.split("\n")
        for i, line in enumerate(lines):
            page.keyboard.type(line, delay=20)
            if i < len(lines) - 1:
                page.keyboard.press("Shift+Enter")
        time.sleep(1)

        # Click Save
        save_selectors = [
            'button:has-text("Save")',
            'button:has-text("Submit")',
            'button:has-text("Confirm")',
            '[data-e2e="save-btn"]',
        ]
        for sel in save_selectors:
            try:
                el = page.query_selector(sel)
                if el and el.is_visible():
                    page.evaluate("el => el.click()", el)
                    print(f"  Saved via: {sel}")
                    time.sleep(3)
                    break
            except Exception:
                continue

        print(f"  Bio updated!")
        return True
    else:
        print(f"  Could not find bio field.")
        page.screenshot(path=str(PROJECT_DIR / "debug_tiktok_bio.png"))
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Update TikTok profile picture and bio.")
    parser.add_argument("--logo-only", action="store_true", help="Only update profile picture")
    parser.add_argument("--bio-only", action="store_true", help="Only update bio")
    parser.add_argument("--logo", type=str, default=str(LOGO_PATH), help="Path to logo image")
    parser.add_argument("--bio", type=str, default=BIO_TEXT, help="Bio text")
    args = parser.parse_args()

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(CHROME_PROFILE_DIR),
            channel="chrome",
            headless=False,
            slow_mo=100,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
        )
        page = context.pages[0] if context.pages else context.new_page()

        if not check_session(page):
            wait_for_login(page)
            if not check_session(page):
                print("Error: still not logged in. Exiting.")
                context.close()
                return

        print("Session valid — updating profile\n")

        do_logo = not args.bio_only
        do_bio = not args.logo_only

        if not navigate_to_edit_profile(page):
            print("Error: could not open Edit Profile. Check debug screenshot.")
            context.close()
            return

        if do_logo:
            update_profile_picture(page, Path(args.logo))

        if do_bio:
            # Re-open edit profile in case photo upload closed the modal
            if do_logo:
                time.sleep(2)
                navigate_to_edit_profile(page)
            update_bio(page, args.bio)

        print("\n=== Done ===")
        context.close()


if __name__ == "__main__":
    main()
