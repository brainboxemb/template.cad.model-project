"""Execute the selected module tests/builds and CAD model batch."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from .config import BuildSelection, ProjectConfig
from .items import CadModel, PythonModule


def _run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def install_module(module: PythonModule) -> None:
    _run([sys.executable, "-m", "pip", "install", "-e", str(module.root)])


def test_module(module: PythonModule) -> None:
    install_module(module)
    _run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(module.root / "tests"),
            "-v",
        ]
    )


def build_module(module: PythonModule, output_root: Path) -> None:
    target = output_root / "modules" / module.id
    target.mkdir(parents=True, exist_ok=True)
    _run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--wheel-dir",
            str(target),
            str(module.root),
        ]
    )


def build_models(
    *,
    repo: Path,
    build_module_root: Path,
    namespace: str,
    models: tuple[CadModel, ...],
) -> None:
    if not models:
        return
    install_module(PythonModule("build", build_module_root))
    command = [
        sys.executable,
        "-m",
        "cad_model_build",
        "--repo",
        str(repo),
        "--namespace",
        namespace,
    ]
    for model in models:
        command.extend(["--model", model.id])
    _run(command)


def execute(
    *,
    repo: Path,
    project: ProjectConfig,
    selection: BuildSelection,
    namespace: str,
    modules: tuple[PythonModule, ...],
    models: tuple[CadModel, ...],
) -> None:
    output_root = repo / project.output_root / namespace
    if "test" in selection.tasks:
        for module in modules:
            test_module(module)
    if "build" in selection.tasks:
        for module in modules:
            build_module(module, output_root)
        build_models(
            repo=repo,
            build_module_root=repo / project.modules_root / "build",
            namespace=namespace,
            models=models,
        )
