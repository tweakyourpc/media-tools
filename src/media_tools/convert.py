from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath


@dataclass(slots=True)
class ConversionResult:
    input_path: Path
    output_path: Path


_ALLOWED_FFMPEG_NAMES = {"ffmpeg", "ffmpeg.exe"}


def resolve_ffmpeg_binary(ffmpeg: str = "ffmpeg") -> str:
    if Path(ffmpeg).name != ffmpeg or PureWindowsPath(ffmpeg).name != ffmpeg:
        raise ValueError("ffmpeg must be a command name, not a path; install ffmpeg on PATH and use 'ffmpeg'")
    if ffmpeg.lower() not in _ALLOWED_FFMPEG_NAMES:
        raise ValueError("ffmpeg command must be 'ffmpeg' or 'ffmpeg.exe'")

    binary = shutil.which(ffmpeg)
    if binary is None:
        raise FileNotFoundError(f"ffmpeg not found on PATH: {ffmpeg}")
    return binary


def convert_gif_to_mp4(
    input_path: str | Path,
    *,
    output_path: str | Path | None = None,
    ffmpeg: str = "ffmpeg",
) -> ConversionResult:
    source = Path(input_path).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {source}")

    binary = resolve_ffmpeg_binary(ffmpeg)

    destination = Path(output_path).expanduser().resolve() if output_path else source.with_suffix(".mp4")
    destination.parent.mkdir(parents=True, exist_ok=True)

    command = [
        binary,
        "-y",
        "-loglevel",
        "error",
        "-i",
        str(source),
        "-vf",
        "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        "-movflags",
        "+faststart",
        "-pix_fmt",
        "yuv420p",
        str(destination),
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"ffmpeg failed with exit code {exc.returncode}") from exc

    return ConversionResult(input_path=source, output_path=destination)
