"""CLI entrypoint for project CI."""

from __future__ import annotations

from pathlib import Path

from .config import BuildSelection, current_branch, load_build, load_project
from .items import discover_models, discover_modules, select
from .runner import execute


def main() -> None:
    repo = Path.cwd()
    project = load_project(repo)
    branch = current_branch(repo)

    modules = discover_modules(repo, project)
    models = discover_models(repo, project)

    if branch == project.stable_branch:
        selection = BuildSelection(
            branch=branch,
            modules=None,
            models=None,
            tasks=("test", "build"),
        )
    else:
        selection = load_build(repo, branch)

    execute(
        repo=repo,
        project=project,
        selection=selection,
        modules=select(modules, selection.modules),
        models=select(models, selection.models),
    )


if __name__ == "__main__":
    main()
