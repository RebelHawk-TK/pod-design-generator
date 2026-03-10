#!/bin/bash
# Email monitor — polls inbox via Microsoft Graph API, notifies via Telegram
cd /Users/rebelhawk/Documents/Claude/pod-design-generator
export PATH="/Users/rebelhawk/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
/usr/bin/python3 email_monitor.py
