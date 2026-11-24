import unittest

from cad_project.merge_policy import MergePolicyError, merge_method


class MergePolicyTests(unittest.TestCase):
    def test_feature_to_dev_is_squash(self):
        self.assertEqual(
            merge_method(head="issue/9-change", base="dev"),
            "squash",
        )

    def test_dev_to_main_is_merge_commit(self):
        self.assertEqual(merge_method(head="dev", base="main"), "merge")

    def test_main_to_dev_is_merge_commit(self):
        self.assertEqual(merge_method(head="main", base="dev"), "merge")

    def test_other_integrations_are_rejected(self):
        with self.assertRaises(MergePolicyError):
            merge_method(head="issue/9-change", base="main")


if __name__ == "__main__":
    unittest.main()
