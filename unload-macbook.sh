#!/usr/bin/env bash
PLIST_DEST="$HOME/Library/LaunchAgents/com.me.random-wsg-bg.plist"

echo "Unloading com.me.random-wsg-bg..."
launchctl unload -w "$PLIST_DEST"

echo "✅ com.me.random-wsg-bg is now unloaded."
