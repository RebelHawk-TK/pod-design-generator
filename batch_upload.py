#!/usr/bin/env python3
"""Batch upload orchestrator for multi-platform POD uploads.

Runs uploads across multiple platforms in a single session with
configurable daily limits per platform. Designs are niche-shuffled
for diverse ordering. Generates a summary report after each run.

Usage:
    python3 batch_upload.py                              # Run all platforms
    python3 batch_upload.py --platforms redbubble         # One platform
    python3 batch_upload.py --platforms redbubble,teepublic --daily-limit 25
    python3 batch_upload.py --folder tshirt --daily-limit 50
    python3 batch_upload.py --dry-run                     # Preview plan
    python3 batch_upload.py --status                      # Show dashboard
    python3 batch_upload.py --retry-failed                # Retry all failures
    python3 batch_upload.py --list-reports                # List saved reports
    python3 batch_upload.py --show-report                 # Print latest report
    python3 batch_upload.py --notify                      # macOS notification

The script will:
    1. Show what will be uploaded (plan)
    2. Run each platform's uploader sequentially
    3. Print a summary report
    4. Save report to reports/ directory
    5. Send macOS notification (if --notify)

Reports are saved to reports/ and can be emailed via Claude Code's
MS365 MCP integration: "email my latest batch report"

Note: Browser-based platforms (Redbubble, TeePublic, Society6) require
a visible browser and may pause for CAPTCHAs. API platforms (Pinterest,
Etsy) run fully unattended.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PROJECT_DIR = Path(__file__).parent
REPORTS_DIR = PROJECT_DIR / "reports"

PLATFORM_CONFIGS = {
    "redbubble": {
        "script": "upload.py",
        "type": "browser",
        "default_daily": 30,
        "default_delay": 45,
        "folders": ["tshirt", "sticker", "poster"],
    },
    "teepublic": {
        "script": "upload_teepublic.py",
        "type": "browser",
        "default_daily": 30,
        "default_delay": 45,
        "folders": ["tshirt", "sticker", "poster"],
    },
    "society6": {
        "script": "upload_society6.py",
        "type": "browser",
        "default_daily": 30,
        "default_delay": 45,
        "folders": ["tshirt", "sticker", "poster"],
    },
    "pinterest": {
        "script": "upload_pinterest.py",
        "type": "api",
        "default_daily": 10,
        "default_delay": 240,
        "folders": ["tshirt", "sticker", "poster"],
    },
    "etsy": {
        "script": "upload_etsy.py",
        "type": "api",
        "default_daily": 50,
        "default_delay": 8,
        "folders": ["tshirt", "sticker", "poster"],
    },
    "tiktok": {
        "script": "upload_tiktok.py",
        "type": "browser",
        "default_daily": 1,
        "default_delay": 120,
        "folders": ["video"],
    },
    "instagram": {
        "script": "upload_instagram.py",
        "type": "browser",
        "default_daily": 1,
        "default_delay": 120,
        "folders": ["video"],
    },
}


# ---------------------------------------------------------------------------
# Plan
# ---------------------------------------------------------------------------

def build_plan(
    platforms: list[str],
    folder: str | None,
    daily_limit: int | None,
    retry_failed: bool,
) -> list[dict]:
    """Build the upload plan for this batch run."""
    plan = []
    for platform in platforms:
        config = PLATFORM_CONFIGS[platform]
        folders = [folder] if folder else config["folders"]
        limit = daily_limit or config["default_daily"]

        for f in folders:
            plan.append({
                "platform": platform,
                "folder": f,
                "limit": limit,
                "delay": config["default_delay"],
                "type": config["type"],
                "script": config["script"],
                "retry_failed": retry_failed,
            })

    return plan


def show_plan(plan: list[dict]) -> None:
    """Display the upload plan."""
    print("=" * 55)
    print("  BATCH UPLOAD PLAN")
    print("=" * 55)

    total_uploads = 0
    total_time = 0
    for step in plan:
        est_time = step["limit"] * step["delay"] / 60
        total_uploads += step["limit"]
        total_time += est_time
        auto = "auto" if step["type"] == "api" else "manual"
        retry = " [RETRY FAILED]" if step["retry_failed"] else ""
        print(f"  {step['platform']:<12} {step['folder']:<10} up to {step['limit']:>4} uploads  ~{est_time:.0f} min  [{auto}]{retry}")

    print("-" * 55)
    if total_time < 60:
        print(f"  Total: up to {total_uploads} uploads, ~{total_time:.0f} min")
    else:
        print(f"  Total: up to {total_uploads} uploads, ~{total_time / 60:.1f} hours")
    print("=" * 55)


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

def run_step(step: dict, dry_run: bool = False) -> dict:
    """Run a single upload step. Returns result dict."""
    platform = step["platform"]
    folder = step["folder"]
    script = PROJECT_DIR / step["script"]
    start_time = time.time()

    print(f"\n{'='*50}")
    print(f"  {platform.upper()} / {folder} (limit: {step['limit']})")
    print(f"{'='*50}\n")

    if not script.exists():
        print(f"  Script not found: {script}")
        return {"platform": platform, "folder": folder, "status": "skipped", "reason": "script not found"}

    # Build command — video platforms use --source-dir instead of --folder
    if platform in ("tiktok", "instagram"):
        cmd = [sys.executable, str(script), "--source-dir", str(PROJECT_DIR / "output" / "videos")]
    else:
        cmd = [sys.executable, str(script), "--folder", folder, "--shuffle"]

    if step["limit"]:
        cmd.extend(["--limit", str(step["limit"])])

    if step.get("retry_failed"):
        cmd.append("--retry-failed")

    if dry_run:
        cmd.append("--dry-run")

    # Platform-specific args
    if platform == "pinterest":
        cmd.extend(["--daily-limit", str(step["limit"])])
    elif platform == "etsy":
        cmd.extend(["--daily-limit", str(step["limit"])])

    print(f"  Running: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(
            cmd,
            cwd=str(PROJECT_DIR),
            timeout=7200,  # 2 hour timeout per step
        )
        elapsed = time.time() - start_time
        status = "success" if result.returncode == 0 else "error"
        return {
            "platform": platform,
            "folder": folder,
            "status": status,
            "returncode": result.returncode,
            "elapsed_min": elapsed / 60,
        }
    except subprocess.TimeoutExpired:
        return {
            "platform": platform,
            "folder": folder,
            "status": "timeout",
            "elapsed_min": 120,
        }
    except KeyboardInterrupt:
        print("\n\n  Interrupted by user.")
        return {
            "platform": platform,
            "folder": folder,
            "status": "interrupted",
            "elapsed_min": (time.time() - start_time) / 60,
        }


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report(results: list[dict]) -> None:
    """Print a summary report of the batch run."""
    print("\n" + "=" * 55)
    print("  BATCH UPLOAD REPORT")
    print("=" * 55)
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    total_time = 0
    for r in results:
        elapsed = r.get("elapsed_min", 0)
        total_time += elapsed
        status_icon = {
            "success": "OK",
            "error": "ERR",
            "timeout": "TIMEOUT",
            "interrupted": "STOP",
            "skipped": "SKIP",
        }.get(r["status"], "?")

        print(f"  [{status_icon:>7}] {r['platform']:<12} {r['folder']:<10} {elapsed:.1f} min")

    print("-" * 55)
    print(f"  Total time: {total_time:.1f} min")

    # Run status dashboard
    print()
    subprocess.run([sys.executable, str(PROJECT_DIR / "upload_status.py"), "--compact"])
    print()


def generate_report_text(results: list[dict]) -> str:
    """Generate a plain-text report for email."""
    lines = ["POD Batch Upload Report", f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]

    for r in results:
        elapsed = r.get("elapsed_min", 0)
        lines.append(f"  [{r['status'].upper():>11}] {r['platform']:<12} {r['folder']:<10} {elapsed:.1f} min")

    lines.append("")

    # Add current totals
    from upload_status import platform_stats, count_designs, PLATFORMS
    design_counts = count_designs()
    total_designs = sum(design_counts.values())

    lines.append("Current Status:")
    for platform, info in PLATFORMS.items():
        stats = platform_stats(platform, info)
        pct = (stats["success"] / total_designs * 100) if total_designs else 0
        lines.append(f"  {platform:<12} {stats['success']:>5} done  {stats['failed']:>3} failed  {pct:.1f}%")

    grand_done = sum(platform_stats(p, i)["success"] for p, i in PLATFORMS.items())
    grand_total = total_designs * len(PLATFORMS)
    lines.append(f"\n  GRAND TOTAL: {grand_done}/{grand_total} ({grand_done/grand_total*100 if grand_total else 0:.1f}%)")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Report delivery
# ---------------------------------------------------------------------------

def save_report(results: list[dict]) -> Path:
    """Save the report to a timestamped file. Returns the file path."""
    REPORTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_path = REPORTS_DIR / f"batch_report_{timestamp}.txt"
    report_text = generate_report_text(results)
    report_path.write_text(report_text)
    print(f"  Report saved: {report_path}")
    return report_path


def get_latest_report() -> Path | None:
    """Return the most recent report file, or None."""
    if not REPORTS_DIR.is_dir():
        return None
    reports = sorted(REPORTS_DIR.glob("batch_report_*.txt"), reverse=True)
    return reports[0] if reports else None


def list_reports(limit: int = 10) -> None:
    """List recent report files."""
    if not REPORTS_DIR.is_dir():
        print("No reports directory found. Run a batch upload first.")
        return
    reports = sorted(REPORTS_DIR.glob("batch_report_*.txt"), reverse=True)
    if not reports:
        print("No reports found.")
        return
    print(f"\nRecent reports ({len(reports)} total):\n")
    for r in reports[:limit]:
        size = r.stat().st_size
        print(f"  {r.name}  ({size:,} bytes)")
    if len(reports) > limit:
        print(f"  ... and {len(reports) - limit} more")
    print(f"\nTo email the latest, ask Claude Code: \"email my latest batch report\"")


def send_macos_notification(results: list[dict]) -> None:
    """Send a macOS desktop notification with the batch summary."""
    successes = sum(1 for r in results if r["status"] == "success")
    total = len(results)
    errors = total - successes

    title = "POD Batch Upload Complete"
    if errors:
        message = f"{successes}/{total} steps OK, {errors} had issues. Check reports/ for details."
    else:
        message = f"All {total} steps completed successfully."

    try:
        subprocess.run(
            ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
            timeout=5,
            capture_output=True,
        )
    except Exception:
        pass  # Notification is best-effort


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch upload orchestrator for multi-platform POD uploads.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python3 batch_upload.py                                    # All platforms
  python3 batch_upload.py --platforms redbubble --folder tshirt
  python3 batch_upload.py --platforms redbubble,teepublic --daily-limit 25
  python3 batch_upload.py --dry-run                          # Preview plan
  python3 batch_upload.py --status                           # Dashboard only
  python3 batch_upload.py --retry-failed                     # Retry failures
  python3 batch_upload.py --list-reports                      # List reports
  python3 batch_upload.py --show-report                      # Print latest
  python3 batch_upload.py --notify                           # macOS alert
""",
    )
    parser.add_argument(
        "--platforms",
        help=f"Comma-separated platforms (default: all). Options: {','.join(PLATFORM_CONFIGS)}",
    )
    parser.add_argument(
        "--folder",
        help="Target a specific folder (tshirt, sticker, poster)",
    )
    parser.add_argument(
        "--daily-limit", type=int,
        help="Override daily upload limit per platform per folder",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview plan and run uploaders in dry-run mode",
    )
    parser.add_argument(
        "--retry-failed", action="store_true",
        help="Only retry previously failed uploads",
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Show status dashboard and exit",
    )
    parser.add_argument(
        "--list-reports", action="store_true",
        help="List saved batch reports and exit",
    )
    parser.add_argument(
        "--show-report", action="store_true",
        help="Print the latest report to stdout and exit",
    )
    parser.add_argument(
        "--notify", action="store_true",
        help="Send a macOS desktop notification when the batch finishes",
    )
    parser.add_argument(
        "--yes", "-y", action="store_true",
        help="Skip confirmation prompt (for scheduled/unattended runs)",
    )
    args = parser.parse_args()

    if args.status:
        subprocess.run([sys.executable, str(PROJECT_DIR / "upload_status.py")])
        return

    if args.list_reports:
        list_reports()
        return

    if args.show_report:
        latest = get_latest_report()
        if latest:
            print(latest.read_text())
        else:
            print("No reports found. Run a batch upload first.")
        return

    # Parse platforms
    if args.platforms:
        platforms = [p.strip() for p in args.platforms.split(",")]
        for p in platforms:
            if p not in PLATFORM_CONFIGS:
                print(f"Unknown platform: {p}")
                print(f"Available: {', '.join(PLATFORM_CONFIGS)}")
                sys.exit(1)
    else:
        # Default: only browser platforms (API ones need separate config)
        platforms = ["redbubble", "teepublic", "society6"]

    # Build and show plan
    plan = build_plan(platforms, args.folder, args.daily_limit, args.retry_failed)
    show_plan(plan)

    if args.dry_run:
        print("\n[DRY RUN MODE]\n")

    # Confirm (skip if --yes for unattended runs)
    if not args.dry_run and not args.yes:
        try:
            resp = input("\nProceed? [Y/n] ").strip().lower()
            if resp and resp != "y":
                print("Cancelled.")
                return
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return

    # Execute
    results = []
    for step in plan:
        try:
            result = run_step(step, dry_run=args.dry_run)
            results.append(result)

            # Stop all if interrupted
            if result["status"] == "interrupted":
                break

        except KeyboardInterrupt:
            print("\n\nBatch interrupted.")
            break

    # Report
    if results and not args.dry_run:
        print_report(results)

        # Always save report to file
        report_path = save_report(results)

        # macOS notification
        if args.notify:
            send_macos_notification(results)


if __name__ == "__main__":
    main()
