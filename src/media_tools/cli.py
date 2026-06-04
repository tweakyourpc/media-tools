from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__
from .convert import convert_gif_to_mp4
from .transcribe import transcribe_media
from .tts import speak_text_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="media-tools")
    parser.add_argument("--version", action="version", version=__version__)

    subparsers = parser.add_subparsers(dest="command", required=True)

    transcribe = subparsers.add_parser("transcribe", help="Transcribe audio or video to TXT and VTT")
    transcribe.add_argument("files", nargs="+", help="Input media files")
    transcribe.add_argument("--model", default="base", help="Whisper model name")
    transcribe.add_argument("--device", default="cpu", help="Whisper device")
    transcribe.add_argument("--compute-type", default="int8", help="Whisper compute type")
    transcribe.add_argument("--language", default=None, help="Force a language code")
    transcribe.add_argument("--output-dir", default=None, help="Write outputs to this directory")

    speak = subparsers.add_parser("speak", help="Render text files to WAV with Piper")
    speak.add_argument("files", nargs="+", help="Input text files")
    speak.add_argument("--voice", default="en_US-lessac-high", help="Piper voice name")
    speak.add_argument("--voice-dir", default=None, help="Directory containing Piper model files")
    speak.add_argument("--model-path", default=None, help="Explicit Piper .onnx model path")
    speak.add_argument("--output-dir", default=None, help="Write outputs to this directory")

    convert = subparsers.add_parser("gif-to-mp4", help="Convert GIF files to MP4")
    convert.add_argument("files", nargs="+", help="Input GIF files")
    convert.add_argument("--ffmpeg", default="ffmpeg", help="ffmpeg command name on PATH; paths are rejected")
    convert.add_argument("--output-dir", default=None, help="Write outputs to this directory")

    return parser


def _output_path(output_dir: str | None, source: str | Path, suffix: str) -> Path | None:
    if output_dir is None:
        return None
    source_path = Path(source)
    return Path(output_dir).expanduser().resolve() / f"{source_path.stem}{suffix}"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "transcribe":
        for file_path in args.files:
            result = transcribe_media(
                file_path,
                model_name=args.model,
                device=args.device,
                compute_type=args.compute_type,
                language=args.language,
                output_dir=args.output_dir,
            )
            print(f"{result.input_path}: saved {result.txt_path.name} and {result.vtt_path.name}")
            if result.language:
                print(f"Detected language: {result.language}")
        return 0

    if args.command == "speak":
        for file_path in args.files:
            output_path = _output_path(args.output_dir, file_path, ".wav")
            result = speak_text_file(
                file_path,
                output_path=output_path,
                voice=args.voice,
                voice_dir=args.voice_dir,
                model_path=args.model_path,
            )
            print(f"{result.input_path}: saved {result.output_path}")
        return 0

    if args.command == "gif-to-mp4":
        for file_path in args.files:
            output_path = _output_path(args.output_dir, file_path, ".mp4")
            result = convert_gif_to_mp4(file_path, output_path=output_path, ffmpeg=args.ffmpeg)
            print(f"{result.input_path}: saved {result.output_path}")
        return 0

    parser.error("Unknown command")
    return 2
