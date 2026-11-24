from pathlib import Path
import unittest
from unittest.mock import patch

from cad_model_ci.config import BuildSelection, ForgeDependency, ProjectConfig
from cad_model_ci.items import PythonModule
from cad_model_ci.runner import execute


class RunnerTests(unittest.TestCase):
    @patch("cad_model_ci.runner.build_module")
    @patch("cad_model_ci.runner.test_module")
    def test_selected_module_is_the_only_module_tested(self, test_module, build_module):
        project = ProjectConfig(
            stable_branch="main",
            development_branch="dev",
            forge=ForgeDependency("brainboxemb/lib.py.solidcraft.forge", "0.13.2", "a" * 40),
            modules_root=Path("modules"),
            models_root=Path("models"),
            output_root=Path("build"),
        )
        selected = (PythonModule("ci", Path("modules/ci")),)
        execute(
            repo=Path("."),
            project=project,
            selection=BuildSelection("issue/1", ("ci",), (), ("test",)),
            modules=selected,
            models=(),
        )
        test_module.assert_called_once_with(selected[0])
        build_module.assert_not_called()


if __name__ == "__main__":
    unittest.main()
