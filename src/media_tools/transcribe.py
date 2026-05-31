
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class TranscriptionResult:
    input_path: Path
    txt_path: Path
    vtt_path: Path
    language: str | None
    segment_count: int


def format_timestamp(value: float) -> str:
    milliseconds = int(round(value * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1_000)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


def transcribe_media(
    input_path: str | Path,
    *,
    model_name: str = "base",
    device: str = "cpu",
    compute_type: str = "int8",
    language: str | None = None,
    output_dir: str | Path | None = None,
) -> TranscriptionResult:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("faster-whisper is not installed") from exc

    source = Path(input_path).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {source}")

    destination_dir = Path(output_dir).expanduser().resolve() if output_dir else source.parent
    destination_dir.mkdir(parents=True, exist_ok=True)
    stem = source.stem

    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    segments_iter, info = model.transcribe(str(source), language=language)
    segments = list(segments_iter)

    txt_path = destination_dir / f"{stem}.txt"
    vtt_path = destination_dir / f"{stem}.vtt"

    transcript = " ".join(segment.text.strip() for segment in segments).strip()
    txt_path.write_text(f"{transcript}\n", encoding="utf-8")

    vtt_lines = ["WEBVTT", ""]
    for segment in segments:
        vtt_lines.append(f"{format_timestamp(segment.start)} --> {format_timestamp(segment.end)}")
        vtt_lines.append(segment.text.strip())
        vtt_lines.append("")
    vtt_path.write_text("\n".join(vtt_lines), encoding="utf-8")

    return TranscriptionResult(
        input_path=source,
        txt_path=txt_path,
        vtt_path=vtt_path,
        language=getattr(info, "language", None),
        segment_count=len(segments),
    )
