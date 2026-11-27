# Espace montage

Espace de travail pour créer des vidéos (TikTok, Shorts, YouTube) avec Claude Code : scripts de montage, skills, agents, et films faits en code (Lemo-Opuscar, HyperFrames).

## Installer
Prérequis : Linux ou WSL2, `git`, `ffmpeg`, Node 20+, [uv](https://docs.astral.sh/uv/), `curl`.

```bash
git clone https://github.com/jrlams2/EspaceMontage.git && cd EspaceMontage
./installer.sh                 # tout
./installer.sh --violoncelles  # + échantillons de violoncelle (414 Mo) pour les musiques Lemo-Opuscar
./installer.sh --sans-plugins  # sans les plugins Claude Code
```

Le script installe : les paquets Python (`requirements.txt`, dans `.venv`), ffmpeg 7 et les sons UI SFX (dans `.outils/`), Earshot, Chromium pour Playwright, les plugins et skills Claude Code, et la bibliothèque Lemo-Opuscar (`~/lemo-opuscar`).

## Pas dans le dépôt
Les rushs (`Videos/`), les exports, et les médias des projets (voix, musiques, captures) : refaire un projet existant demande de les remettre à leur place.

Organisation, conventions et outils : voir `CLAUDE.md`.
