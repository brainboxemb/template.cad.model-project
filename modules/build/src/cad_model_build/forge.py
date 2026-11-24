"""Install an exact Forge revision and compile one model."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def install_url(repository: str, commit: str) -> str:
    return f"git+https://github.com/{repository}.git@{commit}#subdirectory=scpf"


def install_forge(repository: str, commit: str) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            install_url(repository, commit),
        ],
        check=True,
    )


def build_model(*, model_id: str, source: Path, output_root: Path) -> Path:
    target = output_root / "models" / model_id
    target.mkdir(parents=True, exist_ok=True)
    output = target / "solidcraft.json"
    subprocess.run(
        [sys.executable, "-m", "scpf", str(source), "--out", str(output)],
        check=True,
    )
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError(f"Forge produced no output: {output}")
    return output
