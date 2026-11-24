"""Load and validate project, model and working-build configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
from typing import Any

import yaml


class ConfigError(ValueError):
    """Raised when repository configuration is missing or inconsistent."""


_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_COMMIT = re.compile(r"^[0-9a-f]{40}$")
_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass(frozen=True)
class ForgeDependency:
    repository: str
    version: str
    commit: str


@dataclass(frozen=True)
class ProjectConfig:
    forge: ForgeDependency
    models_root: Path
    output_root: Path


@dataclass(frozen=True)
class ModelConfig:
    id: str
    builder: str
    source: Path
    root: Path


@dataclass(frozen=True)
class BuildConfig:
    branch: str
    models: tuple[str, ...] | None
    tasks: tuple[str, ...]


def _mapping(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"missing config: {path}") from exc
    except yaml.YAMLError as exc:
        raise ConfigError(f"invalid YAML: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"config must be a mapping: {path}")
    return data


def _relative_path(value: object, field: str, path: Path) -> Path:
    if not isinstance(value, str) or not value:
        raise ConfigError(f"{field} must be a non-empty string: {path}")
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ConfigError(f"{field} must stay inside the repository: {path}")
    return candidate


def load_project_config(repo: Path) -> ProjectConfig:
    path = repo / "ci.yml"
    data = _mapping(path)
    if data.get("schema") != 1:
        raise ConfigError(f"unsupported schema: {path}")

    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict):
        raise ConfigError(f"dependencies must be a mapping: {path}")
    forge = dependencies.get("forge")
    if not isinstance(forge, dict):
        raise ConfigError(f"dependencies.forge must be a mapping: {path}")

    repository = forge.get("repository")
    version = forge.get("version")
    commit = forge.get("commit")
    if not isinstance(repository, str) or not _REPOSITORY.fullmatch(repository):
        raise ConfigError(f"invalid Forge repository: {path}")
    if not isinstance(version, str) or not version:
        raise ConfigError(f"invalid Forge version: {path}")
    if not isinstance(commit, str) or not _COMMIT.fullmatch(commit):
        raise ConfigError(f"Forge commit must be an exact 40-character SHA: {path}")

    models = data.get("models")
    if not isinstance(models, dict):
        raise ConfigError(f"models must be a mapping: {path}")
    output = data.get("output")
    if not isinstance(output, dict):
        raise ConfigError(f"output must be a mapping: {path}")

    models_root = _relative_path(models.get("root"), "models.root", path)
    output_root = _relative_path(output.get("root"), "output.root", path)
    if models_root == output_root or output_root in models_root.parents:
        raise ConfigError(f"model source and generated output must be separate: {path}")

    return ProjectConfig(
        forge=ForgeDependency(
            repository=repository,
            version=version,
            commit=commit,
        ),
        models_root=models_root,
        output_root=output_root,
    )


def load_model_config(model_root: Path) -> ModelConfig:
    path = model_root / "ci.yml"
    data = _mapping(path)
    if data.get("schema") != 1:
        raise ConfigError(f"unsupported model schema: {path}")

    model_id = data.get("id")
    if not isinstance(model_id, str) or not _ID.fullmatch(model_id):
        raise ConfigError(f"invalid model id: {path}")

    builder = data.get("builder")
    if builder != "forge":
        raise ConfigError(f"unsupported builder {builder!r}: {path}")

    source = _relative_path(data.get("source"), "source", path)
    source_path = model_root / source
    if not source_path.is_file():
        raise ConfigError(f"model source does not exist: {source_path}")

    return ModelConfig(
        id=model_id,
        builder=builder,
        source=source,
        root=model_root,
    )


def load_build_config(repo: Path, current_branch: str) -> BuildConfig:
    if current_branch == "main":
        raise ConfigError("main ignores build.yml; use CI/project configuration")

    path = repo / "build.yml"
    data = _mapping(path)
    if data.get("schema") != 1:
        raise ConfigError(f"unsupported schema: {path}")

    branch = data.get("branch")
    if not isinstance(branch, str) or not branch:
        raise ConfigError(f"branch must be a non-empty string: {path}")
    if branch != current_branch:
        raise ConfigError(
            f"stale build.yml: configured branch {branch!r}, current branch {current_branch!r}"
        )

    raw_models = data.get("models")
    if raw_models == "all":
        models = None
    elif isinstance(raw_models, list) and raw_models and all(
        isinstance(value, str) and _ID.fullmatch(value) for value in raw_models
    ):
        models = tuple(raw_models)
    else:
        raise ConfigError(f"models must be 'all' or a non-empty id list: {path}")

    raw_tasks = data.get("tasks")
    if not isinstance(raw_tasks, list) or not raw_tasks or not all(
        isinstance(value, str) for value in raw_tasks
    ):
        raise ConfigError(f"tasks must be a non-empty string list: {path}")
    tasks = tuple(raw_tasks)
    unsupported = sorted(set(tasks) - {"build"})
    if unsupported:
        raise ConfigError(f"unsupported task(s): {', '.join(unsupported)}")

    return BuildConfig(branch=branch, models=models, tasks=tasks)


def current_branch(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "branch", "--show-current"],
        check=True,
        capture_output=True,
        text=True,
    )
    branch = result.stdout.strip()
    if not branch:
        raise ConfigError("cannot determine current Git branch")
    return branch
