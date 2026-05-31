param(
    [switch]$InstallSystemDeps,
    [switch]$DownloadPiperVoice,
    [switch]$Yes,
    [switch]$Help,
    [string]$PiperVoice = "en_US-lessac-high",
    [string]$Python = $(if ($env:PYTHON) { $env:PYTHON } else { "python" }),
    [string]$VenvDir = $(if ($env:MEDIA_TOOLS_VENV) { $env:MEDIA_TOOLS_VENV } else { "" })
)

$ErrorActionPreference = "Stop"

function Show-Usage {
    Write-Host @"
Usage: .\scripts\setup.ps1 [options]

Creates a virtual environment and installs Media Tools plus its Python dependencies.

Options:
  -InstallSystemDeps      Also install required system tools such as ffmpeg.
  -DownloadPiperVoice     Download the default Piper voice model and config.
  -PiperVoice <name>      Piper voice to download. Default: en_US-lessac-high
  -Yes                    Do not prompt package managers that support noninteractive installs.
  -Python <path>          Python executable to use. Default: python or `$env:PYTHON.
  -VenvDir <path>         Virtualenv path. Default: .venv in the repo root or `$env:MEDIA_TOOLS_VENV.
  -Help                   Show this help.
"@
}

if ($Help) {
    Show-Usage
    exit 0
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
if (-not $VenvDir) {
    $VenvDir = Join-Path $RepoRoot ".venv"
}

if ($IsWindows -or $env:OS -eq "Windows_NT") {
    $VenvPython = Join-Path $VenvDir "Scripts\python.exe"
    $CliPath = Join-Path $VenvDir "Scripts\media-tools.exe"
} else {
    $VenvPython = Join-Path $VenvDir "bin/python"
    $CliPath = Join-Path $VenvDir "bin/media-tools"
}

function Test-Command($Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Install-Ffmpeg {
    if (Test-Command "ffmpeg") {
        $Path = (Get-Command ffmpeg).Source
        Write-Host "ffmpeg already installed: $Path"
        return
    }

    if (-not ($IsWindows -or $env:OS -eq "Windows_NT")) {
        throw "Automatic ffmpeg installation from setup.ps1 is only supported on Windows. Use scripts/setup.sh --install-system-deps on Linux or macOS."
    }

    if (Test-Command "winget") {
        $Args = @("install", "--id", "Gyan.FFmpeg", "--exact", "--source", "winget")
        if ($Yes) {
            $Args += @("--silent", "--accept-package-agreements", "--accept-source-agreements")
        }
        & winget @Args
        return
    }

    if (Test-Command "choco") {
        $Args = @("install", "ffmpeg")
        if ($Yes) { $Args += "-y" }
        & choco @Args
        return
    }

    if (Test-Command "scoop") {
        & scoop install ffmpeg
        return
    }

    throw "No supported Windows package manager found. Install ffmpeg manually, or install winget/choco/scoop and re-run setup."
}

function Get-PiperVoiceUrlParts($Voice) {
    $Match = [regex]::Match($Voice, '^([a-z]{2}_[A-Z]{2})-(.+)-(low|medium|high)$')
    if (-not $Match.Success) {
        throw "Unsupported Piper voice name format: $Voice"
    }

    $Language = $Match.Groups[1].Value
    $Speaker = $Match.Groups[2].Value
    $Quality = $Match.Groups[3].Value
    $Family = $Language.Split('_')[0]
    return @($Family, $Language, $Speaker, $Quality)
}

function Get-PiperVoiceDir {
    if ($env:MEDIA_TOOLS_PIPER_VOICE_DIR) {
        return $env:MEDIA_TOOLS_PIPER_VOICE_DIR
    }

    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        $Base = if ($env:LOCALAPPDATA) { $env:LOCALAPPDATA } else { Join-Path $HOME "AppData\Local" }
        return Join-Path $Base "media-tools\Cache\voices\piper"
    }

    if ($IsMacOS) {
        return Join-Path $HOME "Library/Caches/media-tools/voices/piper"
    }

    $CacheBase = if ($env:XDG_CACHE_HOME) { $env:XDG_CACHE_HOME } else { Join-Path $HOME ".cache" }
    return Join-Path $CacheBase "media-tools/voices/piper"
}

function Download-PiperVoiceFiles {
    $Parts = Get-PiperVoiceUrlParts $PiperVoice
    $BaseUrl = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/$($Parts[0])/$($Parts[1])/$($Parts[2])/$($Parts[3])"
    $VoiceDir = Get-PiperVoiceDir
    New-Item -ItemType Directory -Force -Path $VoiceDir | Out-Null

    foreach ($Suffix in @(".onnx", ".onnx.json")) {
        $FileName = "$PiperVoice$Suffix"
        $Target = Join-Path $VoiceDir $FileName
        if (Test-Path $Target) {
            Write-Host "Piper voice file already exists: $Target"
            continue
        }
        $Url = "$BaseUrl/$FileName"
        Write-Host "Downloading $Url"
        Invoke-WebRequest -Uri $Url -OutFile $Target
        Write-Host "Saved $Target"
    }
}

if ($InstallSystemDeps) {
    Install-Ffmpeg
}

& $Python -m venv $VenvDir
& $VenvPython -m pip install --upgrade pip setuptools wheel
& $VenvPython -m pip install -e $RepoRoot

if ($DownloadPiperVoice) {
    Download-PiperVoiceFiles
}

Write-Host "Setup complete."
Write-Host ""
Write-Host "Run:"
Write-Host "  $CliPath --help"
Write-Host ""
Write-Host "Optional checks:"
Write-Host "  ffmpeg -version"
Write-Host "  $VenvPython -m media_tools --help"
