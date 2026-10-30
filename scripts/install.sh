#!/usr/bin/env bash
set -euo pipefail
# Install creator-style-bible locally.
# This script only copies the skill folder. It sends nothing anywhere and asks for no token.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC="$REPO_DIR/plugins/creator-style-bible/skills/creator-style-bible"
DEST="$HOME/.claude/skills/creator-style-bible"
mkdir -p "$HOME/.claude/skills"
cp -r "$SRC" "$DEST"
echo "Installed to $DEST"
echo "Restart Claude Code, then ask it to use creator-style-bible."
