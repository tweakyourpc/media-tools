# Installation

Media Tools installs as a local Python package. The setup helpers create a `.venv`, install the package, and can optionally install the system tools needed by the media commands.

## Recommended Install

Linux and macOS:

```bash
scripts/setup.sh --install-system-deps --download-piper-voice
```

Windows PowerShell:

```powershell
.\scripts\setup.ps1 -InstallSystemDeps -DownloadPiperVoice
```

## Noninteractive Install

Linux and macOS:

```bash
scripts/setup.sh --install-system-deps --download-piper-voice --yes
```

Windows PowerShell:

```powershell
.\scripts\setup.ps1 -InstallSystemDeps -DownloadPiperVoice -Yes
```

## Python-Only Install

Use this if Python is already installed and `ffmpeg` is already on `PATH`.

Linux and macOS:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
```

## Requirements File

The project also includes `requirements.txt` for dependency review or pre-installing packages:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

`pyproject.toml` is still the package source of truth.

## System Dependencies

`gif-to-mp4` requires `ffmpeg`. The setup helpers can install it automatically through these package managers:

- Linux: `apt-get`, `dnf`, `yum`, `pacman`, `zypper`, or `apk`
- macOS: Homebrew
- Windows: `winget`, Chocolatey, or Scoop

If none of those package managers are available, install `ffmpeg` manually and confirm it works:

```bash
ffmpeg -version
```

## Piper Voice Files

`speak` requires a Piper `.onnx` model and matching `.onnx.json` config. The setup helpers can download the default `en_US-lessac-high` voice:

```bash
scripts/setup.sh --download-piper-voice
```

```powershell
.\scripts\setup.ps1 -DownloadPiperVoice
```

To use a different voice name supported by the Piper voice repository:

```bash
scripts/setup.sh --download-piper-voice --piper-voice en_US-lessac-medium
```

```powershell
.\scripts\setup.ps1 -DownloadPiperVoice -PiperVoice en_US-lessac-medium
```

## Verify Install

Linux and macOS:

```bash
.venv/bin/media-tools --help
.venv/bin/python -m media_tools --help
ffmpeg -version
```

Windows PowerShell:

```powershell
.\.venv\Scripts\media-tools.exe --help
.\.venv\Scripts\python.exe -m media_tools --help
ffmpeg -version
```
