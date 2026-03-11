#!/bin/bash
# Daily automated uploads: TeePublic landmark tshirts
# All phases unified in a single source directory
# Schedule: Daily at 1:00 AM
cd "/Users/rebelhawk/Documents/Claude/pod-design-generator"

SOURCE="/Users/rebelhawk/Documents/Claude/landmark-style-transfer-unified/output"

echo "=== TeePublic Daily Upload $(date) ==="

# --- Retry any failed uploads first ---
echo ""
echo "--- Retrying Failed Uploads ---"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder poster --retry-failed --source-dir "$SOURCE"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder tshirt --retry-failed --source-dir "$SOURCE"

# --- Landmark tshirts (45/day from unified source) ---
echo ""
echo "--- Tshirt Uploads ---"
caffeinate -s "/usr/bin/python3" "upload_teepublic.py" --folder tshirt --limit 45 --source-dir "$SOURCE" --shuffle

echo ""
echo "=== Done $(date) ==="
