from pathlib import Path
import tempfile
import unittest

from cad_model_pages.build import _stage_build_scope


class PagesBuildTests(unittest.TestCase):
    def test_stages_any_durable_scope_at_site_mount_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            durable = root / "durable-dev"
            source.mkdir()
            durable.mkdir()
            (durable / "build-plan.json").write_text(
                '{"schema": 1}',
                encoding="utf-8",
            )

            staged = _stage_build_scope(source, durable)

            self.assertEqual(staged, source / "prepared-build/main")
            self.assertEqual(
                (staged / "build-plan.json").read_text(encoding="utf-8"),
                '{"schema": 1}',
            )


if __name__ == "__main__":
    unittest.main()
