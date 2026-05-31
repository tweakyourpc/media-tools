from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from media_tools.paths import resolve_piper_model
from media_tools.transcribe import format_timestamp
from media_tools.tts import normalize_text


class MediaToolsTests(unittest.TestCase):
    def test_normalize_text(self) -> None:
        self.assertEqual(normalize_text("Hello.\n\nWorld…"), "Hello. World.")

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


if __name__ == "__main__":
    unittest.main()
