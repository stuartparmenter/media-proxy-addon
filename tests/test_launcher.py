import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("launcher", Path(__file__).parents[1] / "run.py")
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class LauncherTest(unittest.TestCase):
    def test_existing_options_and_config_reach_rust(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            options = root / "options.json"
            config = root / "config.yaml"
            options.write_text(json.dumps(dict(host="127.0.0.1", port=9999, log_level="WARNING")))
            config.write_text("youtube:\n  60fps: false\n")
            with patch.object(launcher, "OPTIONS", options), patch.object(launcher, "CONFIG", config), patch.object(launcher.os, "execvp") as execute:
                launcher.main()
            execute.assert_called_once_with("/usr/local/bin/media-proxy", [
                "/usr/local/bin/media-proxy", "--host", "127.0.0.1", "--port", "9999",
                "--log-level", "warning", "--config", str(config)])

    def test_defaults_without_optional_files(self):
        with tempfile.TemporaryDirectory() as directory:
            absent = Path(directory) / "absent"
            with patch.object(launcher, "OPTIONS", absent), patch.object(launcher, "CONFIG", absent), patch.object(launcher.os, "execvp") as execute:
                launcher.main()
            self.assertEqual(execute.call_args.args[1], [
                "/usr/local/bin/media-proxy", "--host", "0.0.0.0", "--port", "8788", "--log-level", "info"])


if __name__ == "__main__":
    unittest.main()
