from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from cad_model_build.runtime import _export_drawings, _export_stl, _snapshot


class SnapshotRuntimeTests(unittest.TestCase):
    @patch("cad_model_build.runtime.subprocess.run")
    def test_primary_snapshot_uses_solidcraft_default_camera(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_text("model", encoding="utf-8")
            target = root / "model.png"

            def fake_run(command, **kwargs):
                Path(command[command.index("--out") + 1]).write_bytes(b"png")

            run.side_effect = fake_run
            _snapshot(saved, target, None)

            command = run.call_args.args[0]
            self.assertNotIn("--camera", command)

    @patch("cad_model_build.runtime.subprocess.run")
    def test_primary_snapshot_can_define_camera(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_text("model", encoding="utf-8")
            target = root / "model.png"

            def fake_run(command, **kwargs):
                Path(command[command.index("--out") + 1]).write_bytes(b"png")

            run.side_effect = fake_run
            _snapshot(saved, target, {"yaw": -0.4})

            command = run.call_args.args[0]
            self.assertIn("--camera", command)

    @patch("cad_model_build.runtime.subprocess.run")
    def test_additional_snapshot_can_define_camera(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_text("model", encoding="utf-8")
            target = root / "top.png"

            def fake_run(command, **kwargs):
                Path(command[command.index("--out") + 1]).write_bytes(b"png")

            run.side_effect = fake_run
            _snapshot(saved, target, {"pitch": -1.55})

            command = run.call_args.args[0]
            self.assertIn("--camera", command)

    @patch("cad_model_build.runtime.subprocess.run")
    def test_exploded_snapshot_uses_isolated_saved_design_checkpoint(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_bytes(b"assembled")
            target = root / "exploded.png"

            def fake_run(command, **kwargs):
                if command[1] == "run":
                    script = Path(command[2])
                    payload = __import__("json").loads(script.read_text())
                    self.assertEqual(
                        payload,
                        {
                            "commands": [{
                                "command": "explode.show",
                                "params": {"view": "Assembly review"},
                            }]
                        },
                    )
                    checkpoint = Path(command[command.index("--save") + 1])
                    checkpoint.write_bytes(b"exploded")
                elif command[1] == "snapshot":
                    source = Path(command[2])
                    self.assertNotEqual(source, saved)
                    self.assertEqual(source.read_bytes(), b"exploded")
                    Path(command[command.index("--out") + 1]).write_bytes(b"png")
                else:
                    self.fail(f"unexpected SolidCraft command: {command}")

            run.side_effect = fake_run
            _snapshot(
                saved,
                target,
                {"yaw": -0.4},
                exploded_view="Assembly review",
            )

            self.assertEqual(run.call_count, 2)
            self.assertEqual(saved.read_bytes(), b"assembled")
            self.assertEqual(target.read_bytes(), b"png")

    @patch("cad_model_build.runtime.subprocess.run")
    def test_missing_exploded_view_fails_clearly(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_bytes(b"assembled")
            target = root / "exploded.png"
            run.side_effect = subprocess.CalledProcessError(
                1,
                ["solidcraft-cli", "run"],
            )

            with self.assertRaisesRegex(
                RuntimeError,
                "could not select exploded view 'Missing'",
            ):
                _snapshot(
                    saved,
                    target,
                    None,
                    exploded_view="Missing",
                )

    @patch("cad_model_build.runtime.subprocess.run")
    def test_stl_export_uses_adapter_default_when_quality_is_unspecified(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_bytes(b"sc")
            target = root / "model.stl"

            def fake_run(command, **kwargs):
                target.write_bytes(b"solid")

            run.side_effect = fake_run
            _export_stl(
                saved=saved,
                target=target,
                artifact_options={},
            )

            command = run.call_args.args[0]
            self.assertNotIn("--quality", command)

    @patch("cad_model_build.runtime.subprocess.run")
    def test_stl_export_maps_explicit_quality_to_solidcraft(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_bytes(b"sc")
            target = root / "model.stl"

            def fake_run(command, **kwargs):
                target.write_bytes(b"solid")

            run.side_effect = fake_run
            _export_stl(
                saved=saved,
                target=target,
                artifact_options={"stl": {"quality": "fine"}},
            )

            command = run.call_args.args[0]
            quality = command.index("--quality")
            self.assertEqual(command[quality + 1], "fine")

    @patch("cad_model_build.runtime.subprocess.run")
    def test_drawing_export_uses_replay_bound_native_drawing(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "models/part/model.sc"
            saved.parent.mkdir(parents=True)
            saved.write_bytes(b"sc")
            work = root / "work"
            work.mkdir()
            row = {
                "id": "part",
                "drawings": [{
                    "name": "Part",
                    "drawing": "$drawing_1",
                    "sheet": "$drawing_1_sheet",
                    "orientation": "$drawing_1_orientation",
                    "path": "models/part/drawings/Part.pdf",
                    "preview": "models/part/drawings/Part.png",
                    "inspect": "models/part/drawings/Part.json",
                }],
            }
            document = {
                "artifacts": {
                    "drawings": [{
                        "name": "Part",
                        "drawing": "$drawing_1",
                        "sheet": "$drawing_1_sheet",
                        "orientation": "$drawing_1_orientation",
                        "pdf": "drawings/Part.pdf",
                        "png": "drawings/Part.png",
                        "inspect": "drawings/Part.json",
                        "expected": {},
                    }]
                }
            }

            def fake_run(command, **kwargs):
                script = Path(command[2])
                payload = __import__("json").loads(script.read_text())
                for export in (
                    item for item in payload["commands"]
                    if item["command"] == "drawing.export"
                ):
                    path = Path(export["params"]["path"])
                    if export["params"]["format"] == "pdf":
                        path.write_bytes(b"%PDF-1.7\n")
                    else:
                        path.write_bytes(b"\x89PNG\r\n\x1a\npreview")

            run.side_effect = fake_run
            produced = _export_drawings(
                document=document,
                row=row,
                variables={
                    "$drawing_1": "D1",
                    "$drawing_1_sheet": "S1",
                    "$drawing_1_orientation": "landscape",
                },
                saved=saved,
                output_root=root,
                work_dir=work,
                replay_results=[{
                    "name": "Part",
                    "sheets": [],
                    "properties": {},
                }],
            )
            self.assertEqual(
                produced,
                (
                    root / "models/part/drawings/Part.pdf",
                    root / "models/part/drawings/Part.png",
                    root / "models/part/drawings/Part.json",
                ),
            )
            script = __import__("json").loads(
                (work / "drawing-export-1.json").read_text()
            )
            exports = [
                item for item in script["commands"]
                if item["command"] == "drawing.export"
            ]
            self.assertEqual(
                [item["params"]["format"] for item in exports],
                ["pdf", "png"],
            )
            self.assertEqual(exports[1]["params"]["dpi"], 144)



if __name__ == "__main__":
    unittest.main()
