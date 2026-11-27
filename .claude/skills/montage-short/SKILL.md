---
name: montage-short
description: Monte un short vertical 9:16 (TikTok, Reels, Shorts) à partir d'un rush ou d'une URL, avec la chaîne d'outils locale - téléchargement, coupe des silences, recadrage vertical, sous-titres mot à mot, export. Utiliser quand l'utilisateur demande de "monter", "faire un short/TikTok/reel", "sous-titrer", "couper les blancs" ou "passer en vertical" une vidéo.
---

# Montage d'un short vertical

Outils dans `scripts/` (racine du projet). Activer d'abord : `source .venv/bin/activate`.

## Étapes (sauter celles qui ne sont pas demandées)
1. **Source** : si URL → `scripts/telecharger.sh URL` (sortie dans `Videos/`). Sinon prendre le fichier dans `Videos/`.
2. **Projet** : créer `projets/<slug-du-titre>/` et y travailler. Ne jamais modifier la source.
3. **Inspection** : `ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of json <fichier>`.
4. **Coupe des silences** (vidéo face caméra / voix) : `scripts/couper-silences.sh <fichier> 0.15` → `_cut.mp4`.
5. **Vertical** si la source n'est pas déjà en 9:16 : `scripts/vertical.sh <fichier>` → `_9x16.mp4`.
6. **Sous-titres** : `scripts/sous-titres.py <fichier> --mots 3` → `.srt`. Relire le .srt et corriger les noms propres et les fautes évidentes avant de l'incruster.
7. **Incrustation** : `scripts/incruster-sous-titres.sh <fichier> <srt>` → `_st.mp4`.
8. **Export** : copier le rendu final dans `exports/<slug>.mp4`.

## Règles
- Transcrire APRÈS la coupe des silences (sinon le minutage des sous-titres est faux).
- Le premier lancement de Whisper télécharge le modèle large-v3 (~3 Go). Pour un essai rapide, utiliser `--modele small`.
- RAM limitée (~11 Go) : un seul traitement lourd à la fois.
- Pour du motion design, des titres animés ou des sous-titres animés, utiliser plutôt les skills hyperframes (`embedded-captions`, `talking-head-recut`, `motion-graphics`).
- Pour un récit d'enquête, enchaîner avec le skill `video-enquete-storytelling`.
- À la fin, indiquer le chemin du fichier exporté, sa durée et sa résolution.
