#!/usr/bin/env bash
PLIST_SRC="$(pwd)/com.me.random-wsg-bg.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/com.me.random-wsg-bg.plist"

# copy if not already there (or you can force-copy)
if [ ! -f "$PLIST_DEST" ]; then
  echo "Installing LaunchAgent plist..."
  cp "$PLIST_SRC" "$PLIST_DEST"
fi

echo "Unloading any existing job (if loaded)..."
launchctl unload "$PLIST_DEST" 2>/dev/null || true

echo "Loading com.me.random-wsg-bg..."
launchctl load -w "$PLIST_DEST"

echo "✅ com.me.random-wsg-bg is now loaded."
