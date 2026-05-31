# Publishing Checklist

Use this before making the GitHub repository public.

## Repository Basics

- Rename the repository to `media-tools`.
- Confirm the package metadata in `pyproject.toml` matches the public repo name and description.
- Keep `LICENSE` in the repo root.
- Keep `assets/media-tools-hero.png` referenced from `README.md`.

## Pre-Publish Checks

Run the unit tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Check the installer help text:

```bash
scripts/setup.sh --help
```

```powershell
.\scripts\setup.ps1 -Help
```

## Suggested GitHub Description

Cross-platform media helpers for transcription, GIF-to-MP4 conversion, and Piper text-to-speech.

## Suggested Topics

```text
python
media-tools
ffmpeg
whisper
faster-whisper
piper-tts
transcription
text-to-speech
cli
cross-platform
```

## Hero Image Prompt

The current hero image was generated with this direction:

```text
Create a polished marketing hero image for an open-source cross-platform command-line app called Media Tools. The image should communicate audio transcription, GIF/video conversion, and text-to-speech in a clean developer-tool style. Use a wide 16:9 composition with a central terminal-style tool surface, abstract waveform audio, video frames, and typed text converging into clean output artifacts. Avoid readable text, logos, OS branding, watermarks, and mascots.
```

## Release Notes Starter

```markdown
## Media Tools 0.1.0

Initial public release with:

- `media-tools transcribe` for TXT and VTT output via faster-whisper
- `media-tools gif-to-mp4` for ffmpeg-powered GIF conversion
- `media-tools speak` for Piper WAV generation
- Cross-platform setup helpers for Linux, macOS, and Windows
- Optional ffmpeg installation and Piper voice download support
```
