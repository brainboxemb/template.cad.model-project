from pathlib import Path
import unittest


class WorkflowBoundaryTests(unittest.TestCase):
    def test_ci_workflow_only_bootstraps_ci_module(self):
        text = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("pip install -e modules/ci", text)
        self.assertIn("python -m cad_model_ci", text)
        self.assertNotIn("simple-box", text)
        self.assertNotIn("lib.py.solidcraft.forge", text)
        self.assertNotIn("python -m scpf", text)

    def test_merge_workflow_only_bootstraps_merge_policy_module(self):
        text = Path(".github/workflows/merge-policy.yml").read_text(encoding="utf-8")
        self.assertIn("pip install -e modules/merge-policy", text)
        self.assertIn("python -m cad_model_merge_policy", text)
        self.assertNotIn("tool.cad.ci", text)


if __name__ == "__main__":
    unittest.main()
