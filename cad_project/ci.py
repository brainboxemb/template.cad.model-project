"""Run repository CI from stable ci.yml only."""

from __future__ import annotations

from pathlib import Path

from .config import load_project_config
from .forge import build_model, install_forge
from .models import discover_models


def run(repo: Path) -> None:
    project = load_project_config(repo)
    models = discover_models(repo, project)
    install_forge(project.forge)
    output_root = repo / project.output_root
    for model in models:
        build_model(model, output_root)


def main() -> None:
    run(Path.cwd())


if __name__ == "__main__":
    main()
