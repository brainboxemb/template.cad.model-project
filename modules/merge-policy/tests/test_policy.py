import unittest
from unittest.mock import patch

from cad_model_merge_policy.__main__ import dispatch_workflow
from cad_model_merge_policy.policy import MergePolicyError, merge_method


class MergePolicyTests(unittest.TestCase):
    def test_feature_to_dev_is_squash(self):
        self.assertEqual(merge_method(head="issue/10-change", base="dev"), "squash")

    def test_dev_to_main_is_merge_commit(self):
        self.assertEqual(merge_method(head="dev", base="main"), "merge")

    def test_main_to_dev_is_merge_commit(self):
        self.assertEqual(merge_method(head="main", base="dev"), "merge")

    def test_feature_to_main_is_rejected(self):
        with self.assertRaises(MergePolicyError):
            merge_method(head="issue/10-change", base="main")

    @patch("cad_model_merge_policy.__main__.api")
    def test_dispatch_workflow_targets_local_workflow_and_base_ref(self, api):
        dispatch_workflow("owner/repo", "ci.yml", "dev", "token")
        api.assert_called_once_with(
            "owner/repo",
            "actions/workflows/ci.yml/dispatches",
            "token",
            method="POST",
            body={"ref": "dev"},
        )

    @patch("cad_model_merge_policy.__main__.api")
    def test_cleanup_workflow_uses_same_target_ref(self, api):
        dispatch_workflow("owner/repo", "branch-cleanup.yml", "dev", "token")
        api.assert_called_once_with(
            "owner/repo",
            "actions/workflows/branch-cleanup.yml/dispatches",
            "token",
            method="POST",
            body={"ref": "dev"},
        )


if __name__ == "__main__":
    unittest.main()
