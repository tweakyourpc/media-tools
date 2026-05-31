from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch
import unittest

from media_tools.convert import convert_gif_to_mp4
from media_tools.paths import resolve_piper_model
from media_tools.transcribe import format_timestamp
from media_tools.tts import normalize_text


class MediaToolsTests(unittest.TestCase):
    def test_normalize_text(self) -> None:
        self.assertEqual(normalize_text("Hello.\n\nWorld…"), "Hello. World.")

    def test_normalize_text_collapses_runs_of_dots(self) -> None:
        self.assertEqual(normalize_text("Hello...   World…"), "Hello. World.")

    def test_format_timestamp(self) -> None:
        self.assertEqual(format_timestamp(3723.456), "01:02:03.456")

    def test_resolve_piper_model(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            model = base / "en_US-lessac-high.onnx"
            config = base / "en_US-lessac-high.onnx.json"
            model.write_text("model", encoding="utf-8")
            config.write_text("config", encoding="utf-8")

            resolved_model, resolved_config = resolve_piper_model(voice_dir=base)

            self.assertEqual(resolved_model, model)
            self.assertEqual(resolved_config, config)

    def test_gif_conversion_uses_quiet_even_dimension_ffmpeg_args(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "odd.gif"
            source.write_bytes(b"GIF89a")
            destination = Path(tmp) / "odd.mp4"

            with patch("media_tools.convert.shutil.which", return_value="/usr/bin/ffmpeg"):
                with patch("media_tools.convert.subprocess.run") as run:
                    result = convert_gif_to_mp4(source, output_path=destination)

            self.assertEqual(result.input_path, source.resolve())
            self.assertEqual(result.output_path, destination.resolve())
            run.assert_called_once_with(
                [
                    "/usr/bin/ffmpeg",
                    "-y",
                    "-loglevel",
                    "error",
                    "-i",
                    str(source.resolve()),
                    "-vf",
                    "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                    "-movflags",
                    "+faststart",
                    "-pix_fmt",
                    "yuv420p",
                    str(destination.resolve()),
                ],
                check=True,
            )


if __name__ == "__main__":
    unittest.main()
