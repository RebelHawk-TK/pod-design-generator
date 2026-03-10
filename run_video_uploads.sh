#!/bin/bash
# Upload next videos from randomized queue to TikTok and Instagram
# Schedule: Tuesday + Friday at 5:00 AM
# Uploads 3 videos per run from the shuffled queue (promo/travel/stock mix)
cd "$(dirname "$0")"
echo "=== Video Upload $(date) ==="

caffeinate -s /usr/bin/python3 upload_queue.py --limit 3

echo "=== Done $(date) ==="
