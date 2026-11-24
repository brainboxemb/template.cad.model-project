"""Discover independently owned Python modules and CAD models."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import yaml

from .config import ConfigError, ProjectConfig


_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_IMPACTS = {"self", "models", "full"}


@dataclass(frozen=True)
class PythonModule:
    id: str
    root: Path
    impact: str = "self"
    watch: tuple[str, ...] = ()


@dataclass(frozen=True)
class CadModel:
    id: str
    root: Path
    builder: str
    source: Path
    watch: tuple[str, ...] = ()


def _load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema") != 1:
        raise ConfigError(f"invalid item config: {path}")
    return value


def _id(data: dict[str, Any], path: Path) -> str:
    value = data.get("id")
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise ConfigError(f"invalid item id: {path}")
    return value


def _impact(data: dict[str, Any], path: Path) -> str:
    value = data.get("impact", "self")
    if value not in _IMPACTS:
        raise ConfigError(f"impact must be one of {sorted(_IMPACTS)}: {path}")
    return value


def _watch(
    data: dict[str, Any],
    *,
    default: str,
    path: Path,
) -> tuple[str, ...]:
    extra = data.get("watch", [])
    if not isinstance(extra, list) or not all(
        isinstance(value, str) and value for value in extra
    ):
        raise ConfigError(f"watch must be a string list: {path}")
    return (default, *extra)


def discover_modules(repo: Path, project: ProjectConfig) -> tuple[PythonModule, ...]:
    root = repo / project.modules_root
    result: list[PythonModule] = []
    for child in sorted(root.iterdir(), key=lambda value: value.name):
        path = child / "ci.yml"
        if not child.is_dir() or not path.is_file():
            continue
        data = _load(path)
        if data.get("kind") != "python":
            raise ConfigError(f"module kind must be python: {path}")
        relative = child.relative_to(repo).as_posix()
        result.append(
            PythonModule(
                id=_id(data, path),
                root=child,
                impact=_impact(data, path),
                watch=_watch(data, default=f"{relative}/**", path=path),
            )
        )
    return tuple(result)


def discover_models(repo: Path, project: ProjectConfig) -> tuple[CadModel, ...]:
    root = repo / project.models_root
    result: list[CadModel] = []
    seen: set[str] = set()

    for path in sorted(root.rglob("ci.yml")):
        child = path.parent
        data = _load(path)
        process = data.get("process", True)
        if type(process) is not bool:
            raise ConfigError(f"model process must be boolean: {path}")
        if not process:
            continue

        model_id = _id(data, path)
        if model_id in seen:
            raise ConfigError(f"duplicate model id {model_id!r}: {path}")
        seen.add(model_id)

        builder = data.get("builder")
        source = data.get("source")
        if builder != "forge":
            raise ConfigError(f"unsupported model builder {builder!r}: {path}")
        if not isinstance(source, str):
            raise ConfigError(f"model source must be a string: {path}")
        source_path = Path(source)
        if source_path.is_absolute() or ".." in source_path.parts:
            raise ConfigError(f"model source must remain inside model root: {path}")
        if not (child / source_path).is_file():
            raise ConfigError(f"model source does not exist: {child / source_path}")

        relative = child.relative_to(repo).as_posix()
        result.append(
            CadModel(
                id=model_id,
                root=child,
                builder=builder,
                source=source_path,
                watch=_watch(data, default=f"{relative}/**", path=path),
            )
        )
    return tuple(result)


def select(items, selected_ids: tuple[str, ...] | None):
    if selected_ids is None:
        return items
    by_id = {item.id: item for item in items}
    missing = [item_id for item_id in selected_ids if item_id not in by_id]
    if missing:
        raise ConfigError(f"unknown item(s): {', '.join(missing)}")
    return tuple(by_id[item_id] for item_id in selected_ids)
