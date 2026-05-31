from __future__ import annotations

import os
import sys
from pathlib import Path


APP_NAME = "media-tools"
APP_AUTHOR = "media-tools"
DEFAULT_PIPER_VOICE = "en_US-lessac-high"


def _expand(path: str | os.PathLike[str] | None) -> Path | None:
    if path is None:
        return None
    return Path(path).expanduser()


def cache_dir() -> Path:
    override = os.environ.get("MEDIA_TOOLS_CACHE_DIR")
    if override:
        return Path(override).expanduser()

    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / APP_NAME / "Cache"

    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / APP_NAME

    base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / APP_NAME


def default_voice_dir() -> Path:
    override = os.environ.get("MEDIA_TOOLS_PIPER_VOICE_DIR")
    if override:
        return Path(override).expanduser()
    return cache_dir() / "voices" / "piper"


def resolve_piper_model(
    *,
    voice: str = DEFAULT_PIPER_VOICE,
    voice_dir: str | os.PathLike[str] | None = None,
    model_path: str | os.PathLike[str] | None = None,
) -> tuple[Path, Path]:
    explicit_model = _expand(model_path)
    if explicit_model is not None:
        model = explicit_model
        config = Path(f"{model}.json")
    else:
        base_dir = _expand(voice_dir) or default_voice_dir()
        voice_stem = Path(voice).stem if voice.endswith(".onnx") else voice
        model = base_dir / f"{voice_stem}.onnx"
        config = base_dir / f"{voice_stem}.onnx.json"

    if not model.exists():
        raise FileNotFoundError(f"Piper model not found: {model}")
    if not config.exists():
        raise FileNotFoundError(f"Piper config not found: {config}")
    return model, config
