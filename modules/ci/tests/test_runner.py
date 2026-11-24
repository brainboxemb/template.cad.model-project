from pathlib import Path
import unittest
from unittest.mock import patch

from cad_model_ci.config import BuildSelection, ForgeDependency, ProjectConfig
from cad_model_ci.items import CadModel, PythonModule
from cad_model_ci.runner import execute


class RunnerTests(unittest.TestCase):
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

    @patch("cad_model_ci.runner.build_module")
    @patch("cad_model_ci.runner.test_module")
    def test_selected_module_is_the_only_module_tested(
        self,
        test_module,
        build_module,
    ):
        selected = (PythonModule("ci", Path("modules/ci")),)
        execute(
            repo=Path("."),
            project=self.project(),
            selection=BuildSelection("issue/1", ("ci",), (), ("test",)),
            namespace="dev",
            modules=selected,
            models=(),
        )
        test_module.assert_called_once_with(selected[0])
        build_module.assert_not_called()

    @patch("cad_model_ci.runner.build_models")
    @patch("cad_model_ci.runner.build_module")
    def test_build_outputs_are_scoped_below_namespace(
        self,
        build_module,
        build_models,
    ):
        module = PythonModule("ci", Path("modules/ci"))
        model = CadModel(
            id="box",
            root=Path("models/box"),
            builder="forge",
            source=Path("scpf/model.py"),
        )
        execute(
            repo=Path("."),
            project=self.project(),
            selection=BuildSelection("issue/36", ("ci",), ("box",), ("build",)),
            namespace="dev",
            modules=(module,),
            models=(model,),
        )
        build_module.assert_called_once_with(module, Path("build/dev"))
        build_models.assert_called_once()
        self.assertEqual(build_models.call_args.kwargs["namespace"], "dev")
        self.assertEqual(build_models.call_args.kwargs["models"], (model,))


if __name__ == "__main__":
    unittest.main()
