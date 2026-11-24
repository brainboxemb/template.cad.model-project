from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cad_project.ci import run


class CiTests(unittest.TestCase):
    @patch("cad_project.ci.build_model")
    @patch("cad_project.ci.install_forge")
    def test_ci_builds_all_discovered_models_without_build_yml(self, install, build):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "ci.yml").write_text(
                "schema: 1\n"
                "dependencies:\n"
                "  forge:\n"
                "    repository: brainboxemb/lib.py.solidcraft.forge\n"
                "    version: 0.13.2\n"
                "    commit: ea5710a5d2d33b0633b93c5da95dd5b74f126aa4\n"
                "models: {root: models}\n"
                "output: {root: build}\n",
                encoding="utf-8",
            )
            model = repo / "models" / "one"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf" / "model.py").write_text("object()\n", encoding="utf-8")
            (model / "ci.yml").write_text(
                "schema: 1\nid: one\nbuilder: forge\nsource: scpf/model.py\n",
                encoding="utf-8",
            )
            run(repo)
            install.assert_called_once()
            self.assertEqual(build.call_count, 1)


if __name__ == "__main__":
    unittest.main()
