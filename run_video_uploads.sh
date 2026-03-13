#!/bin/bash
# Upload next videos to TikTok, Instagram, and YouTube
# Schedule: Daily at 3:00 AM
# Volume: 9 videos (TikTok/IG) + 9 YouTube Shorts per run
cd "$(dirname "$0")"
echo "=== Video Upload $(date) ==="

caffeinate -s /usr/bin/python3 upload_queue.py --limit 9

echo "--- YouTube Shorts ---"
/usr/bin/python3 upload_youtube.py --upload --limit 9

echo "=== Done $(date) ==="
