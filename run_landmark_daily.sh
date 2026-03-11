#!/bin/bash
# Daily automated uploads: landmark designs to Pinterest + Printify
# All phases unified in a single source directory
# Schedule: Daily at Midnight (12:00 AM)
cd "/Users/rebelhawk/Documents/Claude/pod-design-generator"

SOURCE="/Users/rebelhawk/Documents/Claude/landmark-style-transfer-unified/output"

echo "=== Landmark Daily Upload $(date) ==="

# --- Pinterest (sandbox: 10 pins/day limit per call) ---
echo ""
echo "--- Pinterest Uploads ---"
"/usr/bin/python3" "upload_pinterest.py" --source-dir "$SOURCE" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder poster
"/usr/bin/python3" "upload_pinterest.py" --source-dir "$SOURCE" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder tshirt

# --- Printify (150 per folder per run) ---
echo ""
echo "--- Printify Uploads ---"
"/usr/bin/python3" "upload_printify.py" --source-dir "$SOURCE" --folder poster --limit 150 --publish --delay 3
"/usr/bin/python3" "upload_printify.py" --source-dir "$SOURCE" --folder tshirt --limit 150 --publish --delay 3

echo ""
echo "=== Done $(date) ==="
