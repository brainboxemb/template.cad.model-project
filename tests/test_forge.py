from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cad_project.config import ForgeDependency, ModelConfig
from cad_project.forge import build_model, forge_install_url


class ForgeTests(unittest.TestCase):
    def test_install_url_uses_exact_commit(self):
        dependency = ForgeDependency(
            "brainboxemb/lib.py.solidcraft.forge",
            "0.13.2",
            "ea5710a5d2d33b0633b93c5da95dd5b74f126aa4",
        )
        self.assertIn(dependency.commit, forge_install_url(dependency))

    @patch("cad_project.forge.subprocess.run")
    def test_build_uses_model_owned_source_and_build_root(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            model_root = repo / "models" / "box"
            (model_root / "scpf").mkdir(parents=True)
            (model_root / "scpf" / "model.py").write_text("object()\n", encoding="utf-8")
            model = ModelConfig(
                id="box",
                builder="forge",
                source=Path("scpf/model.py"),
                root=model_root,
            )
            output = repo / "build" / "models" / "box" / "solidcraft.json"

            def fake_run(command, check):
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text("{}\n", encoding="utf-8")

            run.side_effect = fake_run
            actual = build_model(model, repo / "build")
            self.assertEqual(actual, output)
            self.assertIn(str(model_root / "scpf" / "model.py"), run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
