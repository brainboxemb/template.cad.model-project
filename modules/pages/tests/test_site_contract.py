from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
SITE = ROOT / "site"


class SiteContractTests(unittest.TestCase):
    def test_site_mounts_source_metadata_and_stable_build_scope(self):
        mounts = (SITE / "config/_default/module.toml").read_text(
            encoding="utf-8"
        )
        self.assertIn('source = "../models"', mounts)
        self.assertIn('target = "assets/cad-source"', mounts)
        self.assertIn('source = "../prepared-build/main"', mounts)
        self.assertIn('target = "assets/build"', mounts)

    def test_adapter_joins_model_ci_and_build_plan_without_model_names(self):
        adapter = (SITE / "content/models/_content.gotmpl").read_text(
            encoding="utf-8"
        )
        self.assertIn('resources.Match "cad-source/**/model.yml"', adapter)
        self.assertIn('resources.Get (printf "cad-source/%s/ci.yml"', adapter)
        self.assertIn('resources.Get "build/build-plan.json"', adapter)
        self.assertIn('index $ci "variants"', adapter)
        self.assertIn('where $rows "id" $slug', adapter)
        self.assertNotIn("simple-box", adapter)
        self.assertNotIn("simple-mft", adapter)

    def test_shared_layout_supports_model_owned_context_and_extra_views(self):
        page = (SITE / "layouts/models/single.html").read_text(encoding="utf-8")
        self.assertIn('.Resources.Get "page.md"', page)
        self.assertIn('index $m "extra_views"', page)
        self.assertIn('.Resources.Get "scpf-source.py"', page)
        self.assertIn('.Resources.Get "solidcraft.json"', page)
        self.assertNotIn("simple-box", page)
        self.assertNotIn("simple-mft", page)

    def test_workflow_uses_generic_pages_verifier_without_model_ids(self):
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("python -m cad_model_pages.verify", workflow)
        self.assertIn("--build-scope prepared-build/main", workflow)
        self.assertNotIn("simple-box", workflow)
        self.assertNotIn("simple-mft", workflow)

    def test_workflow_uses_official_pages_artifact_deployment(self):
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "actions/configure-pages@983d7736d9b0ae728b81ab479565c72886d7745b",
            workflow,
        )
        self.assertIn(
            "actions/upload-pages-artifact@56afc609e74202658d3ffba0e8f6dda462b719fa",
            workflow,
        )
        self.assertIn(
            "actions/deploy-pages@368f82528645a54fb793d4d04e342629a3f51346",
            workflow,
        )
        self.assertIn("pages: write", workflow)
        self.assertIn("id-token: write", workflow)
        self.assertNotIn("cad_model_pages.publish", workflow)
        self.assertNotIn("pages_branch", workflow)

    def test_site_uses_accepted_hextra_version(self):
        go_mod = (SITE / "go.mod").read_text(encoding="utf-8")
        self.assertIn("github.com/imfing/hextra v0.13.0", go_mod)


if __name__ == "__main__":
    unittest.main()
