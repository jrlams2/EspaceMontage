#!/usr/bin/env python3
"""Transcrit une vidéo/audio en .srt avec faster-whisper (GPU si dispo).
Usage: sous-titres.py fichier.mp4 [--modele large-v3] [--langue fr] [--mots 4]"""
import argparse, pathlib
from faster_whisper import WhisperModel

def ts(s):
    h, r = divmod(s, 3600); m, s = divmod(r, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int((s % 1) * 1000):03}"

p = argparse.ArgumentParser()
p.add_argument("fichier"); p.add_argument("--modele", default="large-v3")
p.add_argument("--langue", default="fr"); p.add_argument("--mots", type=int, default=0,
               help="N mots max par sous-titre (style TikTok). 0 = phrases entières")
a = p.parse_args()
try:
    model = WhisperModel(a.modele, device="cuda", compute_type="float16")
except Exception:
    model = WhisperModel(a.modele, device="cpu", compute_type="int8")
segs, _ = model.transcribe(a.fichier, language=a.langue, word_timestamps=bool(a.mots), vad_filter=True)
blocs = []
for s in segs:
    if a.mots:
        w = list(s.words)
        for i in range(0, len(w), a.mots):
            g = w[i:i + a.mots]
            blocs.append((g[0].start, g[-1].end, "".join(x.word for x in g).strip()))
    else:
        blocs.append((s.start, s.end, s.text.strip()))
out = pathlib.Path(a.fichier).with_suffix(".srt")
out.write_text("\n".join(f"{i}\n{ts(d)} --> {ts(f)}\n{t}\n" for i, (d, f, t) in enumerate(blocs, 1)), encoding="utf-8")
print(out)
