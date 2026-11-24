from pathlib import Path
import unittest


class WorkflowBoundaryTests(unittest.TestCase):
    def test_ci_workflow_contains_only_local_tooling_entrypoint(self):
        workflow = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertNotIn("simple-box", workflow)
        self.assertNotIn("lib.py.solidcraft.forge", workflow)
        self.assertNotIn("python -m scpf", workflow)
        self.assertNotIn("tool.cad.ci", workflow)
        self.assertIn("python -m cad_project.ci", workflow)

    def test_merge_policy_is_repository_local(self):
        workflow = Path(".github/workflows/merge-policy.yml").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("tool.cad.ci", workflow)
        self.assertNotIn("uses: brainboxemb/", workflow)
        self.assertIn("python -m cad_project.merge_policy", workflow)


if __name__ == "__main__":
    unittest.main()
