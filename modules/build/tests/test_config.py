from pathlib import Path
import tempfile
import unittest

from cad_model_build.config import discover_models, load_project


PROJECT = """schema: 1
branches:
  stable: main
  development: dev
dependencies:
  forge:
    repository: brainboxemb/lib.py.solidcraft.forge
    version: 0.14.0
    commit: cd46d6797df319b9d13605c11568990113772700
  solidcraft:
    image: ghcr.io/brainboxemb/cad-solidcraft:v0.3.5
    version: 0.48.1
roots:
  modules: modules
  models: models
  output: build
"""


class BuildConfigTests(unittest.TestCase):
    def test_nested_model_root_artifacts_and_snapshots_are_discovered(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "ci.yml").write_text(PROJECT, encoding="utf-8")
            model = repo / "models" / "components" / "box"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf/model.py").write_text("object()\n", encoding="utf-8")
            (model / "ci.yml").write_text(
                """schema: 1
id: box
builder: forge
source: scpf/model.py
artifacts: [stl]
snapshot:
  camera:
    target: [0, 0, 5]
    distance: 80
  extra:
    - name: top.png
      camera:
        pitch: -1.55
""",
                encoding="utf-8",
            )

            project = load_project(repo)
            models = discover_models(repo, project)
            self.assertEqual(len(models), 1)
            self.assertEqual(models[0].id, "box")
            self.assertEqual(models[0].artifacts, ("stl",))
            self.assertEqual(models[0].snapshot.extra[0].name, "top.png")
            self.assertEqual(models[0].root, model)

    def test_process_false_model_is_not_discovered(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "ci.yml").write_text(PROJECT, encoding="utf-8")
            model = repo / "models" / "box"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf/model.py").write_text("object()\n", encoding="utf-8")
            (model / "ci.yml").write_text(
                "schema: 1\nid: box\nbuilder: forge\n"
                "source: scpf/model.py\nprocess: false\n",
                encoding="utf-8",
            )
            self.assertEqual(discover_models(repo, load_project(repo)), ())


if __name__ == "__main__":
    unittest.main()
