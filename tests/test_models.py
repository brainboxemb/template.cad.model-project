from pathlib import Path
import tempfile
import unittest

from cad_project.config import ConfigError, ProjectConfig, ForgeDependency
from cad_project.models import discover_models, select_models


class ModelTests(unittest.TestCase):
    def project(self):
        return ProjectConfig(
            forge=ForgeDependency("brainboxemb/lib.py.solidcraft.forge", "0.13.2", "a" * 40),
            models_root=Path("models"),
            output_root=Path("build"),
        )

    def test_discovers_independent_model_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            model = repo / "models" / "one"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf" / "model.py").write_text("object()\n", encoding="utf-8")
            (model / "ci.yml").write_text(
                "schema: 1\nid: one\nbuilder: forge\nsource: scpf/model.py\n",
                encoding="utf-8",
            )
            models = discover_models(repo, self.project())
            self.assertEqual([item.id for item in models], ["one"])

    def test_select_rejects_unknown_model(self):
        with self.assertRaisesRegex(ConfigError, "unknown model"):
            select_models((), ("missing",))


if __name__ == "__main__":
    unittest.main()
