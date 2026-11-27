#!/usr/bin/env bash
# Installe tout ce qu'il faut pour l'espace montage. Usage : ./installer.sh [--sans-plugins] [--violoncelles]
set -euo pipefail
cd "$(dirname "$0")"; ICI=$PWD
PLUGINS=1; VSCO=0
for a in "$@"; do case $a in --sans-plugins) PLUGINS=0;; --violoncelles) VSCO=1;; *) echo "option inconnue : $a"; exit 1;; esac; done
ok(){ echo "✓ $*"; }; manque(){ echo "✗ $*"; MANQUE=1; }; MANQUE=0

echo "== 1. Outils système"
command -v git >/dev/null && ok git || manque "git (sudo apt install git)"
command -v ffmpeg >/dev/null && ok "ffmpeg $(ffmpeg -version | head -1 | cut -d' ' -f3)" || manque "ffmpeg (sudo apt install ffmpeg)"
command -v node >/dev/null && [ "$(node -p 'process.versions.node.split(".")[0]')" -ge 20 ] && ok "node $(node -v)" || manque "Node 20+ (https://github.com/nvm-sh/nvm)"
command -v uv >/dev/null && ok uv || manque "uv (curl -LsSf https://astral.sh/uv/install.sh | sh)"
command -v curl >/dev/null && ok curl || manque curl
[ $MANQUE = 0 ] || { echo "Installe d'abord ce qui manque, puis relance."; exit 1; }

echo "== 2. Python (.venv)"
[ -d .venv ] || uv venv -q --python 3.12 .venv
uv pip install -q --python .venv/bin/python -r requirements.txt && ok "paquets Python"

echo "== 3. ffmpeg 7 (pour Lemo-Opuscar), dans .outils/ffmpeg7"
if [ ! -x .outils/ffmpeg7/ffmpeg ]; then
  mkdir -p .outils/ffmpeg7 && cd .outils/ffmpeg7
  U=https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
  curl -fsSLO "$U" && curl -fsSLO "$U.md5" && md5sum -c ffmpeg-release-amd64-static.tar.xz.md5
  tar xJf ffmpeg-release-amd64-static.tar.xz --strip-components=1 && rm -f ffmpeg-release-amd64-static.tar.xz*
  cd "$ICI"
fi; ok "$(.outils/ffmpeg7/ffmpeg -version | head -1 | cut -d' ' -f1-3)"

echo "== 4. Sons d'interface UI SFX (CC0), dans .outils/uisfx"
mkdir -p .outils/uisfx && (cd .outils/uisfx && [ -f package.json ] || npm init -y >/dev/null; npm install -s --ignore-scripts --no-audit --no-fund uisfx@0.4.0) && ok "UI SFX"

echo "== 5. Earshot (bruitages et écoute)"
uv tool install -q --python 3.12 "earshot[listen,mcp] @ git+https://github.com/Leonxlnx/earshot@7a7f7c5" 2>/dev/null || uv tool upgrade earshot -q || true
command -v earshot >/dev/null && ok earshot || echo "! ajoute ~/.local/bin à ton PATH pour earshot"

echo "== 6. Navigateur de rendu (Playwright Chromium)"
npx -y playwright@1 install chromium >/dev/null && ok chromium

echo "== 7. Plugins et skills Claude Code"
CL=$(command -v claude || ls ~/.vscode-server/extensions/anthropic.claude-code-*/resources/native-binary/claude 2>/dev/null | tail -1 || true)
if [ $PLUGINS = 1 ] && [ -n "$CL" ]; then
  for m in anthropics/skills remotion-dev/claude-code-plugin lemomo-ai/lemo-opuscar Leonxlnx/earshot; do "$CL" plugin marketplace add "$m" >/dev/null 2>&1 || true; done
  for p in hyperframes playwright superpowers context7 claude-code-setup commit-commands hookify frontend-design github figma notion; do "$CL" plugin install "$p@claude-plugins-official" -y >/dev/null 2>&1 && ok "plugin $p" || echo "! plugin $p"; done
  for p in example-skills@anthropic-agent-skills document-skills@anthropic-agent-skills remotion@remotion lemo-opuscar@lemolab earshot@earshot; do "$CL" plugin install "$p" -y >/dev/null 2>&1 && ok "plugin $p" || echo "! plugin $p"; done
  npx -y hyperframes@latest skills update >/dev/null 2>&1 && ok "skills HyperFrames" || echo "! skills HyperFrames"
  S=$(ls ~/.claude/plugins/cache/lemolab/lemo-opuscar/*/skills/lemo-opuscar/scripts/setup.sh 2>/dev/null | tail -1 || true)
  if [ -n "$S" ]; then PATH="$ICI/.outils/ffmpeg7:$PATH" sh "$S" deps >/dev/null && ok "bibliothèque Lemo-Opuscar (~/lemo-opuscar)"
    [ $VSCO = 1 ] && (cd ~/lemo-opuscar && sh tools/fetch.sh instruments vsco2ce) && ok "violoncelles VSCO 2 CE"; fi
else echo "- plugins ignorés (Claude Code absent ou --sans-plugins)"; fi

echo; echo "Terminé. Active Python avec : source .venv/bin/activate"
echo "Pour Lemo-Opuscar : export PATH=\"$ICI/.outils/ffmpeg7:\$PATH\""
