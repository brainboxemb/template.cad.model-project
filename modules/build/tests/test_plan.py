from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cad_model_build.config import (
    ForgePin,
    ModelConfig,
    ProjectConfig,
    SnapshotSpec,
    SolidCraftPin,
)
from cad_model_build.plan import resolve_plan


class BuildPlanTests(unittest.TestCase):
    def project(self):
        return ProjectConfig(
            stable_branch="main",
            development_branch="dev",
            build_branch="build",
            forge=ForgePin("brainboxemb/lib.py.solidcraft.forge", "0.14.0", "a" * 40),
            solidcraft=SolidCraftPin(
                "ghcr.io/brainboxemb/cad-solidcraft:v0.3.5",
                "0.48.1",
            ),
            models_root=Path("models"),
            output_root=Path("build"),
        )

    @patch("cad_model_build.plan.source_sha", return_value="b" * 40)
    def test_plan_resolves_native_outputs_optional_stl_and_snapshots(self, _source_sha):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            root = repo / "models" / "box"
            model = ModelConfig(
                id="box",
                root=root,
                source=Path("scpf/model.py"),
                artifacts=("stl",),
                snapshots=(SnapshotSpec("top.png", {"pitch": -1.55}),),
            )
            plan = resolve_plan(
                repo=repo,
                project=self.project(),
                models=(model,),
                selected_ids=("box",),
                namespace="dev",
            )
            row = plan["models"][0]
            self.assertEqual(plan["namespace"], "dev")
            self.assertEqual(plan["source_sha"], "b" * 40)
            self.assertEqual(row["built_source_sha"], "b" * 40)
            self.assertEqual(row["commands"], "models/box/solidcraft.json")
            self.assertEqual(row["native"]["sc"], "models/box/model.sc")
            self.assertEqual(row["native"]["step"], "models/box/model.step")
            self.assertEqual(row["native"]["png"], "models/box/model.png")
            self.assertEqual(row["native"]["stl"], "models/box/model.stl")
            self.assertEqual(row["snapshots"][0]["path"], "models/box/top.png")
            self.assertNotIn("snapshot_camera", row)
            self.assertNotIn("extra_png", row["native"])

    @patch("cad_model_build.plan.source_sha", return_value="b" * 40)
    def test_main_is_a_valid_output_namespace(self, _source_sha):
        with tempfile.TemporaryDirectory() as tmp:
            plan = resolve_plan(
                repo=Path(tmp),
                project=self.project(),
                models=(),
                selected_ids=(),
                namespace="main",
            )
            self.assertEqual(plan["namespace"], "main")
            self.assertEqual(plan["models"], [])


if __name__ == "__main__":
    unittest.main()
