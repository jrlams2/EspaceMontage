#!/usr/bin/env bash
# Incruste un .srt dans la vidéo. Usage: incruster-sous-titres.sh video.mp4 [subs.srt]
set -euo pipefail
v="$1"; s="${2:-${v%.*}.srt}"; o="${v%.*}_st.mp4"
ffmpeg -y -i "$v" -vf "subtitles='$s':force_style='FontName=Montserrat,Fontsize=14,Bold=1,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Alignment=2,MarginV=60'" -c:a copy "$o"
echo "$o"
