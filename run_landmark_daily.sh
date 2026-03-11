#!/bin/bash
# Daily automated uploads: landmark designs to Pinterest + Printify
# Covers Phase 1, Phase 2, and Phase 3 landmark collections
# Schedule: Daily at Midnight (12:00 AM)
# Volume: 3x previous (150/folder Printify, 30 pins Pinterest)
cd "/Users/rebelhawk/Documents/Claude/pod-design-generator"

PHASE1="/Users/rebelhawk/Documents/Claude/landmark-style-transfer/output"
PHASE2="/Users/rebelhawk/Documents/Claude/landmark-style-transfer-phase2/output"
PHASE3="/Users/rebelhawk/Documents/Claude/landmark-style-transfer-phase3/output"

echo "=== Landmark Daily Upload $(date) ==="

# --- Pinterest (sandbox: 10 pins/day limit per call, 30 total) ---
echo ""
echo "--- Pinterest Uploads (Phase 1) ---"
"/usr/bin/python3" "upload_pinterest.py" --source-dir "$PHASE1" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder poster
"/usr/bin/python3" "upload_pinterest.py" --source-dir "$PHASE1" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder tshirt

echo ""
echo "--- Pinterest Uploads (Phase 2) ---"
"/usr/bin/python3" "upload_pinterest.py" --source-dir "$PHASE2" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder poster
"/usr/bin/python3" "upload_pinterest.py" --source-dir "$PHASE2" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder tshirt

echo ""
echo "--- Pinterest Uploads (Phase 3) ---"
"/usr/bin/python3" "upload_pinterest.py" --source-dir "$PHASE3" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder poster
"/usr/bin/python3" "upload_pinterest.py" --source-dir "$PHASE3" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder tshirt

# --- Printify (tripled: 150 per folder per run) ---
echo ""
echo "--- Printify Uploads (Phase 1) ---"
"/usr/bin/python3" "upload_printify.py" --source-dir "$PHASE1" --folder poster --limit 150 --publish --delay 3
"/usr/bin/python3" "upload_printify.py" --source-dir "$PHASE1" --folder tshirt --limit 150 --publish --delay 3

echo ""
echo "--- Printify Uploads (Phase 2) ---"
"/usr/bin/python3" "upload_printify.py" --source-dir "$PHASE2" --folder poster --limit 150 --publish --delay 3
"/usr/bin/python3" "upload_printify.py" --source-dir "$PHASE2" --folder tshirt --limit 150 --publish --delay 3

echo ""
echo "--- Printify Uploads (Phase 3) ---"
"/usr/bin/python3" "upload_printify.py" --source-dir "$PHASE3" --folder poster --limit 150 --publish --delay 3
"/usr/bin/python3" "upload_printify.py" --source-dir "$PHASE3" --folder tshirt --limit 150 --publish --delay 3

echo ""
echo "=== Done $(date) ==="
