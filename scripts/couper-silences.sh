#!/usr/bin/env bash
# Supprime les silences (jump cuts). Usage: couper-silences.sh video.mp4 [marge=0.15s]
set -euo pipefail
auto-editor "$1" --margin "${2:-0.15}s" --no-open -o "${1%.*}_cut.mp4"
