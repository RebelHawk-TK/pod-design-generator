#!/bin/bash
# Upload next videos from randomized queue to TikTok and Instagram
# Schedule: Daily at 3:00 AM (was Tue/Fri only)
# Volume: 9 videos per run (tripled from 3)
cd "$(dirname "$0")"
echo "=== Video Upload $(date) ==="

caffeinate -s /usr/bin/python3 upload_queue.py --limit 9

echo "=== Done $(date) ==="
