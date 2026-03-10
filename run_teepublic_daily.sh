#!/bin/bash
# Daily automated uploads: TeePublic designs (tshirts, posters, stickers)
# Retries any previously failed uploads, then uploads new tshirts
# TeePublic has a daily creation limit (~10-15), so we keep limits conservative
cd "/Users/rebelhawk/Documents/Claude/pod-design-generator"

PHASE1="/Users/rebelhawk/Documents/Claude/landmark-style-transfer/output"
PHASE2="/Users/rebelhawk/Documents/Claude/landmark-style-transfer-phase2/output"

echo "=== TeePublic Daily Upload $(date) ==="

# --- Retry any failed landmark uploads first ---
echo ""
echo "--- Retrying Failed Uploads ---"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder poster --retry-failed --source-dir "$PHASE1"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder poster --retry-failed --source-dir "$PHASE2"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder tshirt --retry-failed --source-dir "$PHASE1"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder tshirt --retry-failed --source-dir "$PHASE2"

# --- Landmark tshirts ---
echo ""
echo "--- Tshirt Uploads (Phase 1 landmarks) ---"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder tshirt --limit 5 --source-dir "$PHASE1" --shuffle

echo ""
echo "--- Tshirt Uploads (Phase 2 landmarks) ---"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder tshirt --limit 5 --source-dir "$PHASE2" --shuffle

echo ""
echo "=== Done $(date) ==="
