#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="${PYTHON:-python3}"
VENV_DIR="${MEDIA_TOOLS_VENV:-$REPO_ROOT/.venv}"
INSTALL_SYSTEM_DEPS=0
DOWNLOAD_PIPER_VOICE=0
PIPER_VOICE="en_US-lessac-high"
ASSUME_YES=0

usage() {
  cat <<'USAGE'
Usage: scripts/setup.sh [options]

Creates a virtual environment and installs Media Tools plus its Python dependencies.

Options:
  --install-system-deps       Also install required system tools such as ffmpeg.
  --download-piper-voice      Download the default Piper voice model and config.
  --piper-voice <name>        Piper voice to download. Default: en_US-lessac-high
  --yes                       Do not prompt package managers that support noninteractive installs.
  --help                      Show this help.

Environment:
  PYTHON                      Python executable to use. Default: python3
  MEDIA_TOOLS_VENV            Virtualenv path. Default: .venv in the repo root
USAGE
}

while [ $# -gt 0 ]; do
  case "$1" in
    --install-system-deps)
      INSTALL_SYSTEM_DEPS=1
      ;;
    --download-piper-voice)
      DOWNLOAD_PIPER_VOICE=1
      ;;
    --piper-voice)
      if [ $# -lt 2 ]; then
        echo "--piper-voice requires a value" >&2
        exit 2
      fi
      PIPER_VOICE="$2"
      shift
      ;;
    --yes|-y)
      ASSUME_YES=1
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

have() {
  command -v "$1" >/dev/null 2>&1
}

run_with_sudo() {
  if [ "$(id -u)" -eq 0 ]; then
    "$@"
  elif have sudo; then
    sudo "$@"
  else
    echo "This install needs root privileges. Re-run as root or install sudo." >&2
    return 1
  fi
}

install_ffmpeg() {
  if have ffmpeg; then
    echo "ffmpeg already installed: $(command -v ffmpeg)"
    return 0
  fi

  case "$(uname -s)" in
    Darwin)
      if ! have brew; then
        echo "Homebrew is required to install ffmpeg automatically on macOS: https://brew.sh" >&2
        return 1
      fi
      brew install ffmpeg
      ;;
    Linux)
      if have apt-get; then
        run_with_sudo apt-get update
        if [ "$ASSUME_YES" -eq 1 ]; then
          run_with_sudo apt-get install -y ffmpeg
        else
          run_with_sudo apt-get install ffmpeg
        fi
      elif have dnf; then
        if [ "$ASSUME_YES" -eq 1 ]; then
          run_with_sudo dnf install -y ffmpeg
        else
          run_with_sudo dnf install ffmpeg
        fi
      elif have yum; then
        if [ "$ASSUME_YES" -eq 1 ]; then
          run_with_sudo yum install -y ffmpeg
        else
          run_with_sudo yum install ffmpeg
        fi
      elif have pacman; then
        if [ "$ASSUME_YES" -eq 1 ]; then
          run_with_sudo pacman -S --needed --noconfirm ffmpeg
        else
          run_with_sudo pacman -S --needed ffmpeg
        fi
      elif have zypper; then
        if [ "$ASSUME_YES" -eq 1 ]; then
          run_with_sudo zypper --non-interactive install ffmpeg
        else
          run_with_sudo zypper install ffmpeg
        fi
      elif have apk; then
        run_with_sudo apk add ffmpeg
      else
        echo "No supported Linux package manager found. Install ffmpeg manually and re-run setup." >&2
        return 1
      fi
      ;;
    *)
      echo "Unsupported OS for automatic ffmpeg install: $(uname -s)" >&2
      return 1
      ;;
  esac
}

download_piper_voice() {
  "$VENV_DIR/bin/python" - "$PIPER_VOICE" <<'PY'
from __future__ import annotations

import re
import sys
import urllib.request

from media_tools.paths import default_voice_dir

voice = sys.argv[1]
match = re.fullmatch(r"([a-z]{2}_[A-Z]{2})-(.+)-(low|medium|high)", voice)
if not match:
    raise SystemExit(f"Unsupported Piper voice name format: {voice}")

language, speaker, quality = match.groups()
family = language.split("_", 1)[0]
base_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/{family}/{language}/{speaker}/{quality}"
destination = default_voice_dir()
destination.mkdir(parents=True, exist_ok=True)

for suffix in (".onnx", ".onnx.json"):
    filename = f"{voice}{suffix}"
    target = destination / filename
    if target.exists():
        print(f"Piper voice file already exists: {target}")
        continue
    url = f"{base_url}/{filename}"
    print(f"Downloading {url}")
    urllib.request.urlretrieve(url, target)
    print(f"Saved {target}")
PY
}

if [ "$INSTALL_SYSTEM_DEPS" -eq 1 ]; then
  install_ffmpeg
fi

"$PYTHON_BIN" -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --upgrade pip setuptools wheel
"$VENV_DIR/bin/python" -m pip install -e "$REPO_ROOT"

if [ "$DOWNLOAD_PIPER_VOICE" -eq 1 ]; then
  download_piper_voice
fi

cat <<EOF2
Setup complete.

Run:
  $VENV_DIR/bin/media-tools --help

Optional checks:
  ffmpeg -version
  $VENV_DIR/bin/python -m media_tools --help
EOF2
