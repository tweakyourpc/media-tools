# Troubleshooting

## `ffmpeg not found on PATH`

Install `ffmpeg` and confirm your shell can find it:

```bash
ffmpeg -version
```

You can ask the setup helper to install it:

```bash
scripts/setup.sh --install-system-deps
```

```powershell
.\scripts\setup.ps1 -InstallSystemDeps
```

Media Tools rejects direct executable paths for `--ffmpeg` to avoid executing untrusted path input. Install `ffmpeg` on `PATH`, then use the default or pass the command name:

```bash
media-tools gif-to-mp4 clip.gif --ffmpeg ffmpeg
```

## Piper model not found

Download the default voice:

```bash
scripts/setup.sh --download-piper-voice
```

```powershell
.\scripts\setup.ps1 -DownloadPiperVoice
```

Or point the command at a voice directory:

```bash
media-tools speak script.txt --voice-dir /path/to/voices
```

The directory must contain both files:

```text
en_US-lessac-high.onnx
en_US-lessac-high.onnx.json
```

## `faster-whisper` install is slow

`faster-whisper` and its runtime dependencies can take time to download. This is expected on a fresh machine. Re-run the install if a network interruption stops `pip` halfway through.

## Whisper model download is slow

The first transcription can download the selected Whisper model. Smaller models start faster:

```bash
media-tools transcribe sample.mp4 --model tiny
```

## Windows PowerShell blocks script execution

If PowerShell refuses to run local scripts, run from the repo root with a temporary process policy:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1 -InstallSystemDeps -DownloadPiperVoice
```

## Outputs are not where expected

By default, output files are written beside the input file. Use `--output-dir` to choose a destination:

```bash
media-tools transcribe file.mp4 --output-dir output
media-tools gif-to-mp4 clip.gif --output-dir output
media-tools speak script.txt --output-dir output
```
