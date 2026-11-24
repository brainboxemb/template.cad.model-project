from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cad_model_build.forge import build_model, install_url


class ForgeBuildTests(unittest.TestCase):
    def test_install_url_contains_exact_commit(self):
        commit = "a" * 40
        self.assertIn(
            commit,
            install_url("brainboxemb/lib.py.solidcraft.forge", commit),
        )

    @patch("cad_model_build.forge.subprocess.run")
    def test_model_output_is_written_below_build_root(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "model.py"
            source.write_text("object()\n", encoding="utf-8")
            output = root / "build" / "models" / "box" / "solidcraft.json"

            def fake_run(command, check):
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text("{}\n", encoding="utf-8")

            run.side_effect = fake_run
            actual = build_model(model_id="box", source=source, output_root=root / "build")
            self.assertEqual(actual, output)


if __name__ == "__main__":
    unittest.main()
