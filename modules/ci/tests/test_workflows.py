from pathlib import Path
import unittest


class WorkflowBoundaryTests(unittest.TestCase):
    def test_ci_workflow_runs_internal_modules_from_source(self):
        text = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("PYTHONPATH: modules/ci/src", text)
        self.assertIn("python -m cad_model_ci", text)
        self.assertNotIn("pip install -e modules/ci", text)
        self.assertNotIn("simple-box", text)
        self.assertNotIn("lib.py.solidcraft.forge", text)
        self.assertNotIn("python -m scpf", text)

    def test_pr_job_is_read_only_and_durable_job_can_publish(self):
        text = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("if: github.event_name == 'pull_request'", text)
        self.assertIn("contents: read", text)
        self.assertIn("if: github.event_name != 'pull_request'", text)
        self.assertIn("contents: write", text)
        self.assertIn("python -m cad_model_build.publish", text)
        self.assertIn("PYTHONPATH: modules/build/src", text)

    def test_merge_workflow_runs_merge_policy_from_source(self):
        text = Path(".github/workflows/merge-policy.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("PYTHONPATH: modules/merge-policy/src", text)
        self.assertIn("python -m cad_model_merge_policy", text)
        self.assertNotIn("pip install -e modules/merge-policy", text)
        self.assertNotIn("tool.cad.ci", text)


if __name__ == "__main__":
    unittest.main()
