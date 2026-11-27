# Espace montage & automatisation

Espace de travail pour le montage vidéo (surtout format vertical 9:16 : TikTok, Reels, Shorts), la création de contenu et les automatisations.

## Arborescence
- `Videos/` : rushes bruts et vidéos téléchargées (sources, jamais modifiées)
- `projets/<nom-projet>/` : un dossier par vidéo (script, montage, fichiers de travail)
- `assets/` : musique, sfx, polices, overlays, logos réutilisables
- `exports/` : rendus finaux
- `scripts/` : outils réutilisables (voir ci-dessous)
- `automatisations/` : workflows automatisés (pipelines, tâches planifiées, publication)
- `templates/` : modèles de scripts, compositions, presets

## Environnement
- Python : `.venv` (géré avec `uv`). Activer : `source .venv/bin/activate`.
  Paquets : yt-dlp, faster-whisper, moviepy, pydub, ffmpeg-python, auto-editor, scenedetect.
- ffmpeg 6.1, Node 22, GPU NVIDIA RTX 5060 (CUDA) : à utiliser pour Whisper.
- WSL2, ~11 Go de RAM : éviter de lancer plusieurs gros modèles en même temps.

## Scripts
- `scripts/telecharger.sh URL` : télécharge dans `Videos/`
- `scripts/sous-titres.py video.mp4 [--mots 3]` : transcription → .srt (`--mots` pour le style TikTok mot à mot)
- `scripts/incruster-sous-titres.sh video.mp4` : incruste le .srt
- `scripts/couper-silences.sh video.mp4` : jump cuts automatiques
- `scripts/vertical.sh video.mp4` : conversion en 9:16 avec fond flouté

## Conventions
- Ne jamais écraser une source : toujours écrire un nouveau fichier (suffixes `_cut`, `_st`, `_9x16`).
- Export par défaut : H.264, CRF 18-20, AAC 192k, 1080x1920 à 30 fps.
- Langue par défaut : français.

## Agents (`.claude/agents/`)
Chaîne vidéo type : `research-analyst` → `video-director` (storyboard) → `video-editor` et `motion-designer` → `qa-engineer`.
Autres agents : `ui-ux-designer`, `fullstack-developer`, `automation-engineer`, `data-analyst`, `devops-engineer`.

## Plugins (installés pour l'utilisateur)
hyperframes, remotion, playwright, superpowers, context7, claude-code-setup, commit-commands, hookify, frontend-design,
example-skills et document-skills (Anthropic), github, figma, notion, lemo-opuscar, earshot.

## Lemo-Opuscar
Courts films entièrement en code, dans un style de bibliothèque (pas pour monter des rushs). Bibliothèque : `~/lemo-opuscar` (ne rien y modifier, elle est réinitialisée à chaque mise à jour).
- Exige ffmpeg 7+ : avant toute commande Lemo-Opuscar (à chaque appel Bash), faire `export PATH="$PWD/.outils/ffmpeg7:$PATH"` (depuis la racine du projet) (7.0.2 statique). Le reste du projet utilise le ffmpeg 6.1 du système.
- Films créés dans `projets/<slug>/` ; préciser 1080x1920 à 30 fps si vertical (défaut 1920x1080 à 24 fps).
- Voix et musique à installer au besoin : `setup.sh deps voice music` (script du plugin).

## Chaîne YouTube / TikTok
Toute vidéo de la chaîne suit le skill `video-chaine`. Idées : `chaine/idees.md` ; historique et statistiques : `chaine/journal.md`.

## Son
- Earshot (commande `earshot`, MCP) : crée des bruitages depuis une phrase et « écoute » un fichier (`earshot make "..." -o f.wav`, `earshot describe f.wav`).
- UI SFX : 936 sons d'interface CC0 dans `.outils/uisfx/node_modules/uisfx/sounds/<pack>/<nom>.ogg`.
- Openverse : `scripts/openverse.py "whoosh" [--prendre N] [--musique] [--cc-by]` ; crédits dans `assets/CREDITS.md`.
- Whisper : installation annulée par l'utilisateur le 2026-11-24 ; ne pas télécharger de modèle sans sa demande. Caler le montage par un autre moyen (minutage ElevenLabs, silences ffmpeg).
