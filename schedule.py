#!/usr/bin/env python3
"""Manage launchd scheduling for automated POD uploads.

Installs, removes, and monitors launchd jobs that run batch_upload.py
on a daily schedule. API platforms (Pinterest, Etsy) run fully unattended.
Browser platforms (Redbubble, TeePublic, Society6) require the screen to
be unlocked.

Usage:
    python3 schedule.py install                     # Install default schedule
    python3 schedule.py install --time 09:30        # Custom time
    python3 schedule.py install --platforms pinterest,etsy --time 06:00
    python3 schedule.py remove                      # Remove all schedules
    python3 schedule.py status                      # Show schedule status
    python3 schedule.py logs                        # Tail recent log output
    python3 schedule.py run-now                     # Trigger immediately
"""

from __future__ import annotations

import argparse
import plistlib
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_DIR = Path(__file__).parent
LOGS_DIR = PROJECT_DIR / "logs"
PYTHON = "/usr/bin/python3"

LANDMARK_SOURCE = Path.home() / "Documents" / "Claude" / "landmark-style-transfer-unified" / "output"

LAUNCH_AGENTS_DIR = Path.home() / "Library" / "LaunchAgents"
PLIST_PREFIX = "com.moderndesignconcept.pod-upload"

# Schedule profiles
PROFILES = {
    "api": {
        "label": f"{PLIST_PREFIX}-api",
        "platforms": "pinterest",
        "description": "API platforms (Pinterest) — fully unattended",
        "default_time": "06:00",
        "daily_limit": None,  # use per-platform defaults
    },
    "browser": {
        "label": f"{PLIST_PREFIX}-browser",
        "platforms": "redbubble,teepublic,society6",
        "description": "Browser platforms (Redbubble, TeePublic, Society6) — needs screen unlocked",
        "default_time": "10:00",
        "daily_limit": 30,
    },
    "all": {
        "label": f"{PLIST_PREFIX}-all",
        "platforms": "redbubble,teepublic,society6,pinterest",
        "description": "All platforms",
        "default_time": "09:00",
        "daily_limit": None,
    },
    "landmark-pinterest": {
        "label": f"{PLIST_PREFIX}-landmark-pinterest",
        "description": "Landmark style-transfer posters + tshirts to Pinterest — fully unattended",
        "default_time": "06:00",
        "daily_limit": 10,
        "direct_cmd": True,  # uses upload_pinterest.py directly, not batch_upload.py
    },
    "video-social": {
        "label": f"{PLIST_PREFIX}-video-social",
        "description": "Landmark videos to TikTok + Instagram — Tue & Fri at 10:00 AM",
        "default_time": "10:00",
        "daily_limit": 1,
        "direct_cmd": True,  # uses run_video_uploads.sh wrapper
        "weekdays": [2, 5],  # Tuesday=2, Friday=5 (launchd Weekday format)
    },
}


# ---------------------------------------------------------------------------
# Plist generation
# ---------------------------------------------------------------------------

def build_landmark_cmd(daily_limit: int) -> list[str]:
    """Build the command to upload landmark designs to Pinterest.

    Runs poster upload first, then tshirt, each respecting the daily limit.
    Uses a wrapper shell command so both folders run sequentially.
    """
    base = [
        PYTHON,
        str(PROJECT_DIR / "upload_pinterest.py"),
        "--source-dir", str(LANDMARK_SOURCE),
        "--board-name", "World Landmarks in Classic Art Styles",
        "--daily-limit", str(daily_limit),
    ]
    return base + ["--folder", "poster"]


def build_landmark_wrapper_script(daily_limit: int) -> str:
    """Generate a shell script that uploads posters then tshirts."""
    script = PROJECT_DIR / "run_landmark_pinterest.sh"
    base_args = (
        f'"{PYTHON}" "{PROJECT_DIR / "upload_pinterest.py"}"'
        f' --source-dir "{LANDMARK_SOURCE}"'
        f' --board-name "World Landmarks in Classic Art Styles"'
        f" --daily-limit {daily_limit}"
    )
    content = f"""#!/bin/bash
# Auto-generated — uploads landmark posters then tshirts to Pinterest daily
echo "=== Landmark Pinterest Upload $(date) ==="
{base_args} --folder poster
{base_args} --folder tshirt
echo "=== Done $(date) ==="
"""
    script.write_text(content)
    script.chmod(0o755)
    return str(script)


def build_plist(
    label: str,
    hour: int,
    minute: int,
    cmd: list[str],
    weekdays: list[int] | None = None,
) -> dict:
    """Build a launchd plist dict.

    Args:
        weekdays: If provided, run only on these days (0=Sun, 1=Mon, ..., 6=Sat).
                  Creates multiple StartCalendarInterval entries.
    """
    stdout_log = str(LOGS_DIR / f"{label}.log")
    stderr_log = str(LOGS_DIR / f"{label}.err.log")

    if weekdays:
        # Multiple calendar intervals for specific weekdays
        calendar = [{"Hour": hour, "Minute": minute, "Weekday": d} for d in weekdays]
    else:
        calendar = {"Hour": hour, "Minute": minute}

    return {
        "Label": label,
        "ProgramArguments": cmd,
        "WorkingDirectory": str(PROJECT_DIR),
        "StartCalendarInterval": calendar,
        "StandardOutPath": stdout_log,
        "StandardErrorPath": stderr_log,
        "EnvironmentVariables": {
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "HOME": str(Path.home()),
        },
    }


def plist_path(label: str) -> Path:
    return LAUNCH_AGENTS_DIR / f"{label}.plist"


# ---------------------------------------------------------------------------
# Install / Remove
# ---------------------------------------------------------------------------

def install_schedule(
    profile: str,
    time_str: str,
    platforms: str | None,
    daily_limit: int | None,
    notify: bool,
) -> None:
    """Install a launchd schedule."""
    LOGS_DIR.mkdir(exist_ok=True)
    LAUNCH_AGENTS_DIR.mkdir(exist_ok=True)

    prof = PROFILES.get(profile)
    if not prof and not platforms:
        print(f"Unknown profile: {profile}")
        print(f"Available: {', '.join(PROFILES)}")
        sys.exit(1)

    # Parse time
    try:
        t = datetime.strptime(time_str, "%H:%M")
        hour, minute = t.hour, t.minute
    except ValueError:
        print(f"Invalid time format: {time_str} (use HH:MM)")
        sys.exit(1)

    if platforms:
        label = f"{PLIST_PREFIX}-custom"
        description = f"Custom: {platforms}"
    else:
        label = prof["label"]
        platforms = prof.get("platforms")
        description = prof["description"]
        if daily_limit is None:
            daily_limit = prof.get("daily_limit")

    # Build the command based on profile type
    if prof and prof.get("direct_cmd") and profile == "video-social":
        # Video-social: runs wrapper script for TikTok + Instagram
        wrapper = str(PROJECT_DIR / "run_video_uploads.sh")
        cmd = ["/bin/bash", wrapper]
        platforms = "tiktok, instagram (video)"
    elif prof and prof.get("direct_cmd"):
        # Landmark-pinterest: runs a wrapper script for poster + tshirt
        limit = daily_limit or 10
        wrapper = build_landmark_wrapper_script(limit)
        cmd = ["/bin/bash", wrapper]
        platforms = "pinterest (landmark)"
    else:
        # Standard batch_upload.py
        cmd = [
            PYTHON,
            str(PROJECT_DIR / "batch_upload.py"),
            "--platforms", platforms,
            "--yes",
        ]
        if daily_limit:
            cmd.extend(["--daily-limit", str(daily_limit)])
        if notify:
            cmd.append("--notify")

    weekdays = prof.get("weekdays") if prof else None
    plist_data = build_plist(label, hour, minute, cmd, weekdays=weekdays)
    path = plist_path(label)

    # Unload existing if present
    if path.exists():
        subprocess.run(["launchctl", "unload", str(path)], capture_output=True)

    # Write plist
    with open(path, "wb") as f:
        plistlib.dump(plist_data, f)

    # Load into launchd
    result = subprocess.run(["launchctl", "load", str(path)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  Error loading plist: {result.stderr}")
        sys.exit(1)

    print(f"\nSchedule installed:")
    print(f"  Profile:   {profile}")
    print(f"  Job:       {description}")
    print(f"  Platforms: {platforms}")
    print(f"  Time:      {time_str} daily")
    if daily_limit:
        print(f"  Limit:     {daily_limit} per platform per folder")
    print(f"  Notify:    {'yes' if notify else 'no'}")
    print(f"  Plist:     {path}")
    print(f"  Logs:      {LOGS_DIR}/{label}.log")
    print(f"\n  The job will run daily at {time_str}.")
    print(f"  Use 'python3 schedule.py status' to verify.")
    print(f"  Use 'python3 schedule.py run-now' to test immediately.")


def remove_schedule(profile: str | None) -> None:
    """Remove launchd schedule(s)."""
    if profile and profile != "all":
        prof = PROFILES.get(profile)
        labels = [prof["label"]] if prof else [f"{PLIST_PREFIX}-{profile}"]
    else:
        # Remove all POD schedules
        labels = [p["label"] for p in PROFILES.values()]
        labels.append(f"{PLIST_PREFIX}-custom")

    removed = 0
    for label in labels:
        path = plist_path(label)
        if path.exists():
            subprocess.run(["launchctl", "unload", str(path)], capture_output=True)
            path.unlink()
            print(f"  Removed: {label}")
            removed += 1

    if removed:
        print(f"\n  {removed} schedule(s) removed.")
    else:
        print("  No schedules found to remove.")


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def show_status() -> None:
    """Show current schedule status."""
    print("\n  POD Upload Schedule Status")
    print("  " + "=" * 50)

    found = False
    all_labels = [p["label"] for p in PROFILES.values()] + [f"{PLIST_PREFIX}-custom"]

    for label in all_labels:
        path = plist_path(label)
        if not path.exists():
            continue
        found = True

        with open(path, "rb") as f:
            plist = plistlib.load(f)

        cal = plist.get("StartCalendarInterval", {})
        hour = cal.get("Hour", 0)
        minute = cal.get("Minute", 0)
        args = plist.get("ProgramArguments", [])

        # Extract platforms from args
        platforms = "unknown"
        for i, arg in enumerate(args):
            if arg == "--platforms" and i + 1 < len(args):
                platforms = args[i + 1]

        # Check if loaded in launchd
        check = subprocess.run(
            ["launchctl", "list", label],
            capture_output=True, text=True,
        )
        loaded = check.returncode == 0

        status = "LOADED" if loaded else "NOT LOADED"
        print(f"\n  [{status}] {label}")
        print(f"    Platforms: {platforms}")
        print(f"    Schedule:  {hour:02d}:{minute:02d} daily")
        print(f"    Plist:     {path}")

        # Check log for last run
        log_path = LOGS_DIR / f"{label}.log"
        if log_path.exists():
            lines = log_path.read_text().strip().split("\n")
            if lines:
                print(f"    Last log:  {lines[-1][:80]}")
            size = log_path.stat().st_size
            print(f"    Log size:  {size:,} bytes")

    if not found:
        print("\n  No schedules installed.")
        print("  Use 'python3 schedule.py install' to create one.")

    # Also show report files
    reports_dir = PROJECT_DIR / "reports"
    if reports_dir.is_dir():
        reports = sorted(reports_dir.glob("batch_report_*.txt"), reverse=True)
        if reports:
            print(f"\n  Recent reports:")
            for r in reports[:3]:
                print(f"    {r.name}")

    print()


# ---------------------------------------------------------------------------
# Logs / Run now
# ---------------------------------------------------------------------------

def show_logs(lines: int = 50) -> None:
    """Show recent log output."""
    log_files = sorted(LOGS_DIR.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True) if LOGS_DIR.is_dir() else []
    if not log_files:
        print("No log files found. Run a scheduled upload first.")
        return

    for log_file in log_files[:2]:
        print(f"\n--- {log_file.name} ---")
        content = log_file.read_text()
        log_lines = content.strip().split("\n")
        for line in log_lines[-lines:]:
            print(line)


def run_now(profile: str) -> None:
    """Trigger an immediate run of a schedule profile."""
    prof = PROFILES.get(profile)
    if not prof:
        # Check for custom
        label = f"{PLIST_PREFIX}-custom"
        path = plist_path(label)
        if not path.exists():
            print(f"Unknown profile: {profile}")
            sys.exit(1)
        with open(path, "rb") as f:
            plist = plistlib.load(f)
        cmd = plist["ProgramArguments"]
    else:
        label = prof["label"]
        path = plist_path(label)
        if path.exists():
            with open(path, "rb") as f:
                plist = plistlib.load(f)
            cmd = plist["ProgramArguments"]
        elif prof.get("direct_cmd"):
            # Landmark profile: generate wrapper and run it
            limit = prof.get("daily_limit", 10)
            wrapper = build_landmark_wrapper_script(limit)
            cmd = ["/bin/bash", wrapper]
        else:
            # Run with profile defaults even if not installed
            cmd = [
                PYTHON,
                str(PROJECT_DIR / "batch_upload.py"),
                "--platforms", prof["platforms"],
                "--notify",
            ]

    print(f"Running: {' '.join(cmd)}\n")
    subprocess.run(cmd, cwd=str(PROJECT_DIR))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Manage launchd scheduling for POD uploads.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python3 schedule.py install                              # Default API schedule
  python3 schedule.py install --profile browser --time 10:30
  python3 schedule.py install --platforms pinterest --time 06:00
  python3 schedule.py remove                               # Remove all
  python3 schedule.py status                               # Check schedules
  python3 schedule.py logs                                 # Recent log output
  python3 schedule.py run-now                              # Test run now

Profiles:
  api                 Pinterest POD designs (fully unattended, default 06:00)
  browser             Redbubble + TeePublic + Society6 (needs screen, default 10:00)
  all                 All platforms (default 09:00)
  landmark-pinterest  Landmark style-transfer to Pinterest (unattended, default 06:00)
  video-social        TikTok + Instagram videos (Tue & Fri at 10:00, needs screen)
""",
    )
    sub = parser.add_subparsers(dest="command")

    # install
    install_p = sub.add_parser("install", help="Install a daily upload schedule")
    install_p.add_argument(
        "--profile", default="api",
        help="Schedule profile: api, browser, all (default: api)",
    )
    install_p.add_argument(
        "--platforms",
        help="Override platforms (comma-separated)",
    )
    install_p.add_argument(
        "--time", default=None,
        help="Daily run time in HH:MM format (default: profile default)",
    )
    install_p.add_argument(
        "--daily-limit", type=int, default=None,
        help="Override daily upload limit per platform per folder",
    )
    install_p.add_argument(
        "--notify", action="store_true", default=True,
        help="Send macOS notification on completion (default: yes)",
    )
    install_p.add_argument(
        "--no-notify", action="store_true",
        help="Disable macOS notification",
    )

    # remove
    remove_p = sub.add_parser("remove", help="Remove upload schedule(s)")
    remove_p.add_argument(
        "--profile",
        help="Specific profile to remove (default: all)",
    )

    # status
    sub.add_parser("status", help="Show schedule status")

    # logs
    logs_p = sub.add_parser("logs", help="Show recent log output")
    logs_p.add_argument(
        "--lines", type=int, default=50,
        help="Number of lines to show (default: 50)",
    )

    # run-now
    run_p = sub.add_parser("run-now", help="Trigger an immediate run")
    run_p.add_argument(
        "--profile", default="api",
        help="Profile to run (default: api)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "install":
        notify = args.notify and not args.no_notify
        time_str = args.time or PROFILES.get(args.profile, {}).get("default_time", "09:00")
        install_schedule(args.profile, time_str, args.platforms, args.daily_limit, notify)

    elif args.command == "remove":
        remove_schedule(args.profile)

    elif args.command == "status":
        show_status()

    elif args.command == "logs":
        show_logs(args.lines)

    elif args.command == "run-now":
        run_now(args.profile)


if __name__ == "__main__":
    main()
