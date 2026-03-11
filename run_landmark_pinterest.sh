#!/bin/bash
# Auto-generated — uploads landmark posters then tshirts to Pinterest daily
echo "=== Landmark Pinterest Upload $(date) ==="
"/usr/bin/python3" "/Users/rebelhawk/Documents/Claude/pod-design-generator/upload_pinterest.py" --source-dir "/Users/rebelhawk/Documents/Claude/landmark-style-transfer-unified/output" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder poster
"/usr/bin/python3" "/Users/rebelhawk/Documents/Claude/pod-design-generator/upload_pinterest.py" --source-dir "/Users/rebelhawk/Documents/Claude/landmark-style-transfer-unified/output" --board-name "World Landmarks in Classic Art Styles" --daily-limit 10 --folder tshirt
echo "=== Done $(date) ==="
