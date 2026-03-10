#!/bin/bash
# Telegram bot — persistent service, forwards messages to Claude Code CLI
cd /Users/rebelhawk/Documents/Claude/pod-design-generator
export PATH="/Users/rebelhawk/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
/usr/bin/python3 telegram_bot.py
