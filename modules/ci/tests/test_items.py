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
            forge=ForgeDependency(
                "brainboxemb/lib.py.solidcraft.forge",
                "0.14.0",
                "a" * 40,
            ),
            modules_root=Path("modules"),
            models_root=Path("models"),
            output_root=Path("build"),
        )

    def test_discovers_item_local_impact_and_nested_model_watch(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            module = repo / "modules" / "ci"
            module.mkdir(parents=True)
            (module / "ci.yml").write_text(
                "schema: 1\nid: ci\nkind: python\nimpact: full\n"
                "watch: [.github/workflows/ci.yml]\n",
                encoding="utf-8",
            )
            model = repo / "models" / "components" / "box"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf" / "model.py").write_text(
                "object()\n",
                encoding="utf-8",
            )
            (model / "ci.yml").write_text(
                "schema: 1\nid: box\nbuilder: forge\n"
                "source: scpf/model.py\nprocess: true\n",
                encoding="utf-8",
            )
            modules = discover_modules(repo, self.project())
            models = discover_models(repo, self.project())
            self.assertEqual(modules[0].impact, "full")
            self.assertIn("modules/ci/**", modules[0].watch)
            self.assertIn(".github/workflows/ci.yml", modules[0].watch)
            self.assertIn("models/components/box/**", models[0].watch)

    def test_process_false_model_is_not_selected_as_an_item(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            model = repo / "models" / "box"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf/model.py").write_text("object()\n", encoding="utf-8")
            (model / "ci.yml").write_text(
                "schema: 1\nid: box\nbuilder: forge\n"
                "source: scpf/model.py\nprocess: false\n",
                encoding="utf-8",
            )
            self.assertEqual(discover_models(repo, self.project()), ())

    def test_selection_returns_only_requested_item(self):
        items = (
            type("Item", (), {"id": "one"})(),
            type("Item", (), {"id": "two"})(),
        )
        self.assertEqual([x.id for x in select(items, ("two",))], ["two"])


if __name__ == "__main__":
    unittest.main()
