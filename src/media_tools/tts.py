from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from .paths import DEFAULT_PIPER_VOICE, resolve_piper_model


@dataclass(slots=True)
class SpeechResult:
    input_path: Path
    output_path: Path
    model_path: Path


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", " ").replace("\n", " ")
    text = text.replace("…", ".")
    text = re.sub(r"\.{2,}", ". ", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


def speak_text_file(
    input_path: str | Path,
    *,
    output_path: str | Path | None = None,
    voice: str = DEFAULT_PIPER_VOICE,
    voice_dir: str | Path | None = None,
    model_path: str | Path | None = None,
) -> SpeechResult:
    source = Path(input_path).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {source}")

    text = normalize_text(source.read_text(encoding="utf-8"))
    if not text:
        raise ValueError("Input text file is empty")

    destination = Path(output_path).expanduser().resolve() if output_path else source.with_suffix(".wav")
    destination.parent.mkdir(parents=True, exist_ok=True)

    model, config = resolve_piper_model(voice=voice, voice_dir=voice_dir, model_path=model_path)
    command = [sys.executable, "-m", "piper", "-m", str(model), "-c", str(config), "-f", str(destination)]
    try:
        subprocess.run(command, input=text.encode("utf-8"), check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Piper failed with exit code {exc.returncode}") from exc

    return SpeechResult(input_path=source, output_path=destination, model_path=model)
