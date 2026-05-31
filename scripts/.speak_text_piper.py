#!/usr/bin/env python3
from pathlib import Path
import sys

from media_tools.tts import speak_text_file


SCRIPT_DIR = Path(__file__).resolve().parent


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: speak_text_piper.py <path_to_text_file>")
        return 1
    result = speak_text_file(sys.argv[1], voice_dir=SCRIPT_DIR / ".piper")
    print(f"Saved {result.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
