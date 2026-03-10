#!/bin/bash
# Daily automated uploads: landmark designs to Pinterest + Printify
# Covers Phase 1 and Phase 2 landmark collections
cd "/Users/rebelhawk/Documents/Claude/pod-design-generator"

PHASE1="/Users/rebelhawk/Documents/Claude/landmark-style-transfer/output"
PHASE2="/Users/rebelhawk/Documents/Claude/landmark-style-transfer-phase2/output"

echo "=== Landmark Daily Upload $(date) ==="

# --- Pinterest (sandbox: 10 pins/day limit) ---
echo ""
echo "--- Pinterest Uploads (Phase 1) ---"
"/usr/bin/python3" "upload_pinterest.py" --source-dir "$PHASE1" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder poster
"/usr/bin/python3" "upload_pinterest.py" --source-dir "$PHASE1" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder tshirt

echo ""
echo "--- Pinterest Uploads (Phase 2) ---"
"/usr/bin/python3" "upload_pinterest.py" --source-dir "$PHASE2" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder poster
"/usr/bin/python3" "upload_pinterest.py" --source-dir "$PHASE2" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder tshirt

# --- Printify (no daily limit, 50 per folder per run to be safe) ---
echo ""
echo "--- Printify Uploads (Phase 1) ---"
"/usr/bin/python3" "upload_printify.py" --source-dir "$PHASE1" --folder poster --limit 50 --publish --delay 3
"/usr/bin/python3" "upload_printify.py" --source-dir "$PHASE1" --folder tshirt --limit 50 --publish --delay 3

echo ""
echo "--- Printify Uploads (Phase 2) ---"
"/usr/bin/python3" "upload_printify.py" --source-dir "$PHASE2" --folder poster --limit 50 --publish --delay 3
"/usr/bin/python3" "upload_printify.py" --source-dir "$PHASE2" --folder tshirt --limit 50 --publish --delay 3

echo ""
echo "=== Done $(date) ==="
