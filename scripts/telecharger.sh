#!/usr/bin/env bash
# Télécharge une vidéo (YouTube, TikTok, X...) dans Videos/. Usage: telecharger.sh URL
set -euo pipefail
yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b" -o "$(dirname "$0")/../Videos/%(title).80s.%(ext)s" "$1"
