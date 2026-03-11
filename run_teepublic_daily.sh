#!/bin/bash
# Daily automated uploads: TeePublic landmark tshirts
# Schedule: Daily at 1:00 AM
# Volume: 3x previous (15 Phase 1 + 15 Phase 2 + 15 Phase 3 = 45/day)
cd "/Users/rebelhawk/Documents/Claude/pod-design-generator"

PHASE1="/Users/rebelhawk/Documents/Claude/landmark-style-transfer/output"
PHASE2="/Users/rebelhawk/Documents/Claude/landmark-style-transfer-phase2/output"
PHASE3="/Users/rebelhawk/Documents/Claude/landmark-style-transfer-phase3/output"

echo "=== TeePublic Daily Upload $(date) ==="

# --- Retry any failed uploads first ---
echo ""
echo "--- Retrying Failed Uploads ---"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder poster --retry-failed --source-dir "$PHASE1"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder poster --retry-failed --source-dir "$PHASE2"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder poster --retry-failed --source-dir "$PHASE3"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder tshirt --retry-failed --source-dir "$PHASE1"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder tshirt --retry-failed --source-dir "$PHASE2"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder tshirt --retry-failed --source-dir "$PHASE3"

# --- Landmark tshirts (tripled: 15 per phase) ---
echo ""
echo "--- Tshirt Uploads (Phase 1 landmarks) ---"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder tshirt --limit 15 --source-dir "$PHASE1" --shuffle

echo ""
echo "--- Tshirt Uploads (Phase 2 landmarks) ---"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder tshirt --limit 15 --source-dir "$PHASE2" --shuffle

echo ""
echo "--- Tshirt Uploads (Phase 3 landmarks) ---"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder tshirt --limit 15 --source-dir "$PHASE3" --shuffle

echo ""
echo "=== Done $(date) ==="
