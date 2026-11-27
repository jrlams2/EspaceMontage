#!/usr/bin/env bash
# Convertit en 9:16 (1080x1920) avec fond flouté. Usage: vertical.sh video.mp4
set -euo pipefail
v="$1"; o="${v%.*}_9x16.mp4"
ffmpeg -y -i "$v" -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 192k "$o"
echo "$o"
