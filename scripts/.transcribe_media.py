#!/usr/bin/env python3
import sys

from media_tools.transcribe import transcribe_media


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: transcribe_media.py <path>")
        return 1
    result = transcribe_media(sys.argv[1])
    print(f"Detected language: {result.language}")
    print(f"Saved {result.txt_path} and {result.vtt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
