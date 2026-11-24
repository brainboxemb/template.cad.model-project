from pathlib import Path
import tempfile
import unittest

from cad_project.config import ConfigError, load_build_config, load_project_config


class ConfigTests(unittest.TestCase):
    def test_project_reads_exact_forge_pin_and_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "ci.yml").write_text(
                "schema: 1\n"
                "dependencies:\n"
                "  forge:\n"
                "    repository: brainboxemb/lib.py.solidcraft.forge\n"
                "    version: 0.13.2\n"
                "    commit: ea5710a5d2d33b0633b93c5da95dd5b74f126aa4\n"
                "models: {root: models}\n"
                "output: {root: build}\n",
                encoding="utf-8",
            )
            config = load_project_config(repo)
            self.assertEqual(config.forge.version, "0.13.2")
            self.assertEqual(config.models_root, Path("models"))
            self.assertEqual(config.output_root, Path("build"))

    def test_build_yml_must_match_current_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "build.yml").write_text(
                "schema: 1\nbranch: issue/1-one\nmodels: all\ntasks: [build]\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ConfigError, "stale build.yml"):
                load_build_config(repo, "issue/2-two")

    def test_main_does_not_consume_build_yml(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ConfigError, "main ignores build.yml"):
                load_build_config(Path(tmp), "main")


if __name__ == "__main__":
    unittest.main()
