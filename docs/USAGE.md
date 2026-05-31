# Usage

Media Tools exposes one CLI:

```bash
media-tools --help
```

You can also run it as a Python module:

```bash
python -m media_tools --help
```

## Transcribe Audio or Video

```bash
media-tools transcribe meeting.mp4
```

This creates:

- `meeting.txt`
- `meeting.vtt`

Options:

```bash
media-tools transcribe meeting.mp4 --model small --device cpu --compute-type int8
media-tools transcribe meeting.mp4 --language en
media-tools transcribe meeting.mp4 --output-dir transcripts
```

Multiple files can be processed in one command:

```bash
media-tools transcribe intro.mp4 outro.mp4 --output-dir transcripts
```

## Convert GIF to MP4

```bash
media-tools gif-to-mp4 animation.gif
```

This creates `animation.mp4` beside the source file.

Options:

```bash
media-tools gif-to-mp4 animation.gif --output-dir converted
media-tools gif-to-mp4 animation.gif --ffmpeg /path/to/ffmpeg
```

The conversion uses `-movflags +faststart` and `-pix_fmt yuv420p` so the output is broadly compatible with browsers and social platforms.

## Speak Text with Piper

```bash
media-tools speak script.txt
```

This creates `script.wav` beside the source file.

Options:

```bash
media-tools speak script.txt --voice en_US-lessac-high
media-tools speak script.txt --voice-dir /path/to/piper/voices
media-tools speak script.txt --model-path /path/to/en_US-lessac-high.onnx
media-tools speak script.txt --output-dir audio
```

When `--model-path` is provided, Media Tools expects the matching config at the same path plus `.json`, for example:

```text
en_US-lessac-high.onnx
en_US-lessac-high.onnx.json
```

## File-Manager Helpers

The scripts with human-readable names in `scripts/` are optional wrappers around the CLI:

- `Convert GIF to MP4`
- `Speak Text with Piper`
- `Transcribe to TXT+VTT`

They assume `.venv` exists in the repo root. Set `MEDIA_TOOLS_PYTHON` if you want them to use a different Python interpreter:

```bash
MEDIA_TOOLS_PYTHON=/path/to/python "scripts/Convert GIF to MP4" clip.gif
```
