<p align="center">
  <img src="https://raw.githubusercontent.com/tweakyourpc/media-tools/main/assets/media-tools-hero.png" alt="Media Tools hero image showing audio, video, and text workflows converging into a command-line media utility" width="100%">
</p>

# Media Tools

Cross-platform command-line helpers for everyday media jobs: transcribe audio and video, convert GIFs to MP4, and render text to speech with Piper.

Media Tools is built as a normal Python package with one CLI, `media-tools`, and small optional file-manager wrappers. It is intended to work on Windows, macOS, and Linux without tying the project to one desktop environment.

## What It Does

- Transcribes audio and video to `.txt` and `.vtt` using `faster-whisper`.
- Converts animated GIFs to browser-friendly `.mp4` files using `ffmpeg`.
- Renders text files to `.wav` audio using Piper TTS voices.
- Installs into a local `.venv` with setup helpers for Linux, macOS, and Windows.
- Keeps the core implementation in reusable Python modules under `src/media_tools/`.

## Quick Install

Linux and macOS:

```bash
scripts/setup.sh --install-system-deps --download-piper-voice
```

Windows PowerShell:

```powershell
.\scripts\setup.ps1 -InstallSystemDeps -DownloadPiperVoice
```

These commands create `.venv`, install the Python package and dependencies, optionally install `ffmpeg`, and optionally download the default Piper voice files.

For more install options, see [docs/INSTALLATION.md](docs/INSTALLATION.md).

## Quick Start

```bash
media-tools transcribe path/to/file.mp4
media-tools gif-to-mp4 path/to/animation.gif
media-tools speak path/to/script.txt
```

Equivalent module form:

```bash
python -m media_tools --help
```

## Commands

### Transcribe Media

```bash
media-tools transcribe interview.mp4
```

Outputs:

- `interview.txt`
- `interview.vtt`

Useful options:

```bash
media-tools transcribe interview.mp4 --model small --language en --output-dir transcripts
```

### Convert GIF to MP4

```bash
media-tools gif-to-mp4 clip.gif
```

Outputs:

- `clip.mp4`

Useful options:

```bash
media-tools gif-to-mp4 clip.gif --output-dir converted
```

### Speak Text with Piper

```bash
media-tools speak narration.txt
```

Outputs:

- `narration.wav`

Useful options:

```bash
media-tools speak narration.txt --voice en_US-lessac-high --output-dir audio
```

More examples are in [docs/USAGE.md](docs/USAGE.md).

## Requirements

- Python 3.10 or newer
- Internet access during first install so `pip` can download Python dependencies
- `ffmpeg` on `PATH` for GIF conversion
- Piper voice model files for text-to-speech

Supported automatic `ffmpeg` installers:

- Linux: `apt-get`, `dnf`, `yum`, `pacman`, `zypper`, or `apk`
- macOS: Homebrew
- Windows: `winget`, Chocolatey, or Scoop

## Piper Voices

By default, `media-tools speak` looks for `en_US-lessac-high.onnx` and `en_US-lessac-high.onnx.json` in the platform cache directory:

- Windows: `%LOCALAPPDATA%\media-tools\Cache\voices\piper`
- macOS: `~/Library/Caches/media-tools/voices/piper`
- Linux: `${XDG_CACHE_HOME:-~/.cache}/media-tools/voices/piper`

You can override this with `MEDIA_TOOLS_PIPER_VOICE_DIR`, `--voice-dir`, or `--model-path`.

## Documentation

- [Installation](docs/INSTALLATION.md)
- [Usage](docs/USAGE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Publishing checklist](docs/PUBLISHING.md)

## Development

Run the pure unit tests without requiring Whisper, Piper, or `ffmpeg` at test time:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Project layout:

- `src/media_tools/` core package and CLI
- `scripts/` optional setup and file-manager helper scripts
- `tests/` unit tests for pure logic
- `assets/` README and marketing assets
- `docs/` public documentation

## License

MIT. See [LICENSE](LICENSE).
