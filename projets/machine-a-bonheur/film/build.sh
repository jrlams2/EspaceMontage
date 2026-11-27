#!/bin/sh
set -e
H=$(cd "$(dirname "$0")" && pwd); LIB=${LIB:-$HOME/lemo-opuscar}; export LIB PATH="$H/../../../.outils/ffmpeg7:$PATH"
cd "$LIB"; node core/render/events.mjs "$H"
node core/render/video.mjs "$H" --fps 30 --workers 2 --size 1080x1920 --out "$H/out/video.mp4"
.venv/bin/python "$H/mix.py"
LEMO_COLOR=bt709 sh core/render/mux.sh "$H/out/video.mp4" "$H/out/mix.wav" "$H/../../../exports/machine-a-bonheur.mp4" 30 0
