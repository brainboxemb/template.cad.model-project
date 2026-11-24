"""Install the configured Forge revision and build Forge model roots."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from .config import ForgeDependency, ModelConfig


def forge_install_url(dependency: ForgeDependency) -> str:
    return (
        f"git+https://github.com/{dependency.repository}.git@"
        f"{dependency.commit}#subdirectory=scpf"
    )


def install_forge(dependency: ForgeDependency) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            forge_install_url(dependency),
        ],
        check=True,
    )


def build_model(model: ModelConfig, output_root: Path) -> Path:
    model_output = output_root / "models" / model.id
    model_output.mkdir(parents=True, exist_ok=True)
    output = model_output / "solidcraft.json"

    subprocess.run(
        [
            sys.executable,
            "-m",
            "scpf",
            str(model.root / model.source),
            "--out",
            str(output),
        ],
        check=True,
    )
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError(f"Forge produced no output: {output}")
    return output
