from pathlib import Path
import tempfile
import unittest

from cad_model_ci.config import ForgeDependency, ProjectConfig
from cad_model_ci.items import discover_models, discover_modules, select


class ItemTests(unittest.TestCase):
    def project(self):
        return ProjectConfig(
            stable_branch="main",
            development_branch="dev",
            forge=ForgeDependency("brainboxemb/lib.py.solidcraft.forge", "0.13.2", "a" * 40),
            modules_root=Path("modules"),
            models_root=Path("models"),
            output_root=Path("build"),
        )

    def test_discovers_module_and_model_roots_independently(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            module = repo / "modules" / "ci"
            module.mkdir(parents=True)
            (module / "ci.yml").write_text(
                "schema: 1\nid: ci\nkind: python\n", encoding="utf-8"
            )
            model = repo / "models" / "box"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf" / "model.py").write_text("object()\n", encoding="utf-8")
            (model / "ci.yml").write_text(
                "schema: 1\nid: box\nbuilder: forge\nsource: scpf/model.py\n",
                encoding="utf-8",
            )
            self.assertEqual([x.id for x in discover_modules(repo, self.project())], ["ci"])
            self.assertEqual([x.id for x in discover_models(repo, self.project())], ["box"])

    def test_selection_returns_only_requested_item(self):
        items = (type("Item", (), {"id": "one"})(), type("Item", (), {"id": "two"})())
        self.assertEqual([x.id for x in select(items, ("two",))], ["two"])


if __name__ == "__main__":
    unittest.main()
