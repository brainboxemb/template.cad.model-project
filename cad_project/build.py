"""Run a human/agent working build selected by build.yml."""

from __future__ import annotations

from pathlib import Path

from .config import current_branch, load_build_config, load_project_config
from .forge import build_model, install_forge
from .models import discover_models, select_models


def run(repo: Path) -> None:
    branch = current_branch(repo)
    project = load_project_config(repo)
    build = load_build_config(repo, branch)
    models = select_models(discover_models(repo, project), build.models)

    if "build" in build.tasks:
        install_forge(project.forge)
        output_root = repo / project.output_root
        for model in models:
            build_model(model, output_root)


def main() -> None:
    run(Path.cwd())


if __name__ == "__main__":
    main()
