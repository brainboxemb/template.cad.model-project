from pathlib import Path
import json
import tempfile
import unittest

from cad_model_pages.verify import PagesVerificationError, verify


class PagesVerifyTests(unittest.TestCase):
    def test_verifies_durable_build_links_without_page_copies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            site = root / "site"
            build = root / "dev"
            model = repo / "models" / "component-a"
            page = site / "models" / "variant-a"
            model.mkdir(parents=True)
            page.mkdir(parents=True)
            build.mkdir(parents=True)
            config = repo / "site/config/_default"
            config.mkdir(parents=True)
            (config / "hugo.toml").write_text(
                '[params]\ncadSourceRepository = "example/cad"\n',
                encoding="utf-8",
            )

            (site / "index.html").write_text(
                "home · Recently updated models",
                encoding="utf-8",
            )
            (site / "models/index.html").write_text(
                "Basic Models · Components · Advanced Models",
                encoding="utf-8",
            )
            for category in ("basic", "components", "advanced"):
                category_page = site / "models" / category
                category_page.mkdir(parents=True)
                link = (
                    '<a href="/models/variant-a/">Variant A</a>'
                    if category == "components"
                    else ""
                )
                (category_page / "index.html").write_text(
                    f'<main class="cad-category-page">'
                    f'<div class="cad-model-grid">{link}</div></main>',
                    encoding="utf-8",
                )

            (model / "model.yml").write_text(
                "section: components\ntitle: Variant A\nparameters: 10 × 20 mm\n",
                encoding="utf-8",
            )

            native = {
                "png": "models/variant-a/model.png",
                "sc": "models/variant-a/model.sc",
                "step": "models/variant-a/model.step",
                "stl": "models/variant-a/model.stl",
            }
            commands = "models/variant-a/solidcraft.json"
            snapshot = "models/variant-a/top.png"
            plan = {
                "schema": 1,
                "namespace": "dev",
                "solidcraft": {"version": "0.48.1"},
                "models": [
                    {
                        "id": "variant-a",
                        "root": "models/component-a",
                        "commands": commands,
                        "native": native,
                        "drawings": [{
                            "name": "Variant A drawing",
                            "drawing": "$drawing_1",
                            "sheet": "$drawing_1_sheet",
                            "orientation": "$drawing_1_orientation",
                            "path": "models/variant-a/drawings/Variant-A.pdf",
                            "preview": "models/variant-a/drawings/Variant-A.png",
                            "inspect": "models/variant-a/drawings/Variant-A.json",
                        }],
                        "snapshots": [{"name": "top.png", "path": snapshot}],
                    }
                ],
            }
            (build / "build-plan.json").write_text(
                json.dumps(plan),
                encoding="utf-8",
            )
            for path in native.values():
                target = build / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"x")
            drawing = build / "models/variant-a/drawings/Variant-A.pdf"
            drawing.parent.mkdir(parents=True, exist_ok=True)
            drawing.write_bytes(b"%PDF-1.7\n")
            drawing.with_suffix(".png").write_bytes(b"\x89PNG\r\n\x1a\npreview")
            drawing.with_suffix(".json").write_text(
                json.dumps({"name": "Variant A drawing"}),
                encoding="utf-8",
            )
            snapshot_path = build / snapshot
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            snapshot_path.write_bytes(b"x")
            command_path = build / commands
            command_path.write_text(
                json.dumps({"commands": [{"command": "Part::Box"}]}),
                encoding="utf-8",
            )

            for name in ("scpf-source.py", "model.yml", "ci.yml"):
                (page / name).write_text("source", encoding="utf-8")

            blob = "https://github.com/example/cad/blob/build/dev/"
            raw = "https://raw.githubusercontent.com/example/cad/build/dev/"
            (page / "index.html").write_text(
                "Variant A · 10 × 20 mm · Built in SolidCraft 0.48.1 · "
                "<code>dev</code> · "
                f"{blob}{commands} · "
                f"{raw}{native['png']} · "
                f"{blob}{native['sc']} · "
                f"{blob}{native['step']} · "
                f"{blob}{native['stl']} · "
                f"{blob}models/variant-a/drawings/Variant-A.pdf · "
                f"{raw}models/variant-a/drawings/Variant-A.pdf · "
                f"{raw}models/variant-a/drawings/Variant-A.png",
                encoding="utf-8",
            )

            verify(repo=repo, site=site, build_scope=build)

            duplicate_drawing = page / "drawings/Variant-A.pdf"
            duplicate_drawing.parent.mkdir(parents=True)
            duplicate_drawing.write_bytes(b"%PDF-1.7\n")
            with self.assertRaisesRegex(
                PagesVerificationError,
                "drawing PDF duplicated in Pages",
            ):
                verify(repo=repo, site=site, build_scope=build)
            duplicate_drawing.unlink()
            duplicate_drawing.parent.rmdir()

            (page / "model.stl").write_bytes(b"duplicate")
            with self.assertRaisesRegex(
                PagesVerificationError,
                "generated artifact duplicated in Pages",
            ):
                verify(repo=repo, site=site, build_scope=build)


    def test_accepts_exp_and_test_build_namespaces(self):
        for namespace in ("exp", "test"):
            with self.subTest(namespace=namespace), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                repo = root / "repo"
                site = root / "site"
                build = root / namespace
                model = repo / "models" / "component-a"
                page = site / "models" / "variant-a"
                model.mkdir(parents=True)
                page.mkdir(parents=True)
                build.mkdir(parents=True)
                config = repo / "site/config/_default"
                config.mkdir(parents=True)
                (config / "hugo.toml").write_text(
                    '[params]\ncadSourceRepository = "example/cad"\n',
                    encoding="utf-8",
                )
                (site / "index.html").write_text(
                    "home · Recently updated models",
                    encoding="utf-8",
                )
                (site / "models/index.html").parent.mkdir(parents=True, exist_ok=True)
                (site / "models/index.html").write_text(
                    "Basic Models · Components · Advanced Models",
                    encoding="utf-8",
                )
                for category in ("basic", "components", "advanced"):
                    category_page = site / "models" / category
                    category_page.mkdir(parents=True)
                    link = (
                        '<a href="/models/variant-a/">Variant A</a>'
                        if category == "components"
                        else ""
                    )
                    (category_page / "index.html").write_text(
                        f'<main class="cad-category-page"><div class="cad-model-grid">{link}</div></main>',
                        encoding="utf-8",
                    )
                (model / "model.yml").write_text(
                    "section: components\ntitle: Variant A\nparameters: 10 mm\n",
                    encoding="utf-8",
                )
                native = {
                    "png": "models/variant-a/model.png",
                    "sc": "models/variant-a/model.sc",
                    "step": "models/variant-a/model.step",
                }
                commands = "models/variant-a/solidcraft.json"
                plan = {
                    "schema": 1,
                    "namespace": namespace,
                    "solidcraft": {"version": "0.49.0"},
                    "models": [{
                        "id": "variant-a",
                        "root": "models/component-a",
                        "commands": commands,
                        "native": native,
                        "drawings": [],
                        "snapshots": [],
                    }],
                }
                (build / "build-plan.json").write_text(json.dumps(plan), encoding="utf-8")
                for path in native.values():
                    target = build / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(b"x")
                command_path = build / commands
                command_path.write_text(
                    json.dumps({"commands": [{"command": "Part::Box"}]}),
                    encoding="utf-8",
                )
                for name in ("scpf-source.py", "model.yml", "ci.yml"):
                    (page / name).write_text("source", encoding="utf-8")
                blob = f"https://github.com/example/cad/blob/build/{namespace}/"
                raw = f"https://raw.githubusercontent.com/example/cad/build/{namespace}/"
                (page / "index.html").write_text(
                    "Variant A · 10 mm · Built in SolidCraft 0.49.0 · "
                    f"<code>{namespace}</code> · "
                    f"{blob}{commands} · "
                    f"{raw}{native['png']} · "
                    f"{blob}{native['sc']} · "
                    f"{blob}{native['step']}",
                    encoding="utf-8",
                )

                verify(repo=repo, site=site, build_scope=build)

    def test_verifies_multi_variant_owner_catalog_and_detail_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            site = root / "site"
            build = root / "dev"
            model = repo / "models" / "component-a"
            model.mkdir(parents=True)
            build.mkdir(parents=True)

            config = repo / "site/config/_default"
            config.mkdir(parents=True)
            (config / "hugo.toml").write_text(
                '[params]\ncadSourceRepository = "example/cad"\n',
                encoding="utf-8",
            )

            (site / "index.html").parent.mkdir(parents=True, exist_ok=True)
            (site / "index.html").write_text(
                "home · Recently updated models",
                encoding="utf-8",
            )
            (site / "models/index.html").parent.mkdir(parents=True, exist_ok=True)
            (site / "models/index.html").write_text(
                "Basic Models · Components · Advanced Models",
                encoding="utf-8",
            )
            owner_href = "/models/owners/component-a/"
            for category in ("basic", "components", "advanced"):
                category_page = site / "models" / category
                category_page.mkdir(parents=True)
                link = (
                    f'<a href="{owner_href}">Component A</a>'
                    if category == "components"
                    else ""
                )
                (category_page / "index.html").write_text(
                    f'<main class="cad-category-page">'
                    f'<div class="cad-model-grid">{link}</div></main>',
                    encoding="utf-8",
                )

            (model / "model.yml").write_text(
                """section: components
title: Component A
variants:
  variant-a:
    title: Variant A
    parameters: 10 × 20 mm
  variant-b:
    title: Variant B
    parameters: 20 × 30 mm
""",
                encoding="utf-8",
            )

            rows = []
            blob = "https://github.com/example/cad/blob/build/dev/"
            raw = "https://raw.githubusercontent.com/example/cad/build/dev/"
            for variant_id, title, parameters in (
                ("variant-a", "Variant A", "10 × 20 mm"),
                ("variant-b", "Variant B", "20 × 30 mm"),
            ):
                native = {
                    "png": f"models/{variant_id}/model.png",
                    "sc": f"models/{variant_id}/model.sc",
                    "step": f"models/{variant_id}/model.step",
                }
                commands = f"models/{variant_id}/solidcraft.json"
                rows.append(
                    {
                        "id": variant_id,
                        "root": "models/component-a",
                        "commands": commands,
                        "native": native,
                        "drawings": [],
                        "snapshots": [],
                    }
                )
                for path in native.values():
                    target = build / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(b"x")
                command_path = build / commands
                command_path.parent.mkdir(parents=True, exist_ok=True)
                command_path.write_text(
                    json.dumps({"commands": [{"command": "Part::Box"}]}),
                    encoding="utf-8",
                )

                page = site / "models" / variant_id
                page.mkdir(parents=True)
                for name in ("scpf-source.py", "model.yml", "ci.yml"):
                    (page / name).write_text("source", encoding="utf-8")
                (page / "index.html").write_text(
                    f"{title} · {parameters} · "
                    "Built in SolidCraft 0.48.1 · <code>dev</code> · "
                    f"{owner_href} · "
                    f"{blob}{commands} · "
                    f"{raw}{native['png']} · "
                    f"{blob}{native['sc']} · "
                    f"{blob}{native['step']}",
                    encoding="utf-8",
                )

            plan = {
                "schema": 1,
                "namespace": "dev",
                "solidcraft": {"version": "0.48.1"},
                "models": rows,
            }
            (build / "build-plan.json").write_text(
                json.dumps(plan),
                encoding="utf-8",
            )

            owner = site / "models" / "owners" / "component-a"
            owner.mkdir(parents=True)
            owner_html = (
                '<a href="/models/variant-a/">Variant A</a>'
                '<a href="/models/variant-b/">Variant B</a>'
            )
            (owner / "index.html").write_text(owner_html, encoding="utf-8")

            verify(repo=repo, site=site, build_scope=build)

            (owner / "index.html").write_text(
                '<a href="/models/variant-a/">Variant A</a>',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                PagesVerificationError,
                "missing variant link for variant-b",
            ):
                verify(repo=repo, site=site, build_scope=build)



if __name__ == "__main__":
    unittest.main()
