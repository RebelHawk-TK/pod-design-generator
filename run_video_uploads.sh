#!/bin/bash
# Auto-generated — uploads landmark videos to TikTok and Instagram
# Schedule: Tuesday + Friday at 10:00 AM
# Uploads 1 promo + 1 travel per platform per run (4 videos total)
cd "$(dirname "$0")"
echo "=== Video Upload $(date) ==="

echo "--- TikTok (promo) ---"
/usr/bin/python3 upload_tiktok.py --source-dir output/videos --limit 1

echo "--- TikTok (travel) ---"
/usr/bin/python3 upload_tiktok.py --source-dir output/videos_travel --limit 1

echo "--- Instagram (promo) ---"
/usr/bin/python3 upload_instagram.py --source-dir output/videos --limit 1

echo "--- Instagram (travel) ---"
/usr/bin/python3 upload_instagram.py --source-dir output/videos_travel --limit 1

echo "=== Done $(date) ==="
