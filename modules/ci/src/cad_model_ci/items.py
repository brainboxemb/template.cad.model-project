"""Discover independently owned Python modules and CAD models."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import yaml

from .config import ConfigError, ProjectConfig


_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass(frozen=True)
class PythonModule:
    id: str
    root: Path


@dataclass(frozen=True)
class CadModel:
    id: str
    root: Path
    builder: str
    source: Path


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
        result.append(PythonModule(_id(data, path), child))
    return tuple(result)


def discover_models(repo: Path, project: ProjectConfig) -> tuple[CadModel, ...]:
    root = repo / project.models_root
    result: list[CadModel] = []
    for child in sorted(root.iterdir(), key=lambda value: value.name):
        path = child / "ci.yml"
        if not child.is_dir() or not path.is_file():
            continue
        data = _load(path)
        model_id = _id(data, path)
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
        result.append(CadModel(model_id, child, builder, source_path))
    return tuple(result)


def select(items, selected_ids: tuple[str, ...] | None):
    if selected_ids is None:
        return items
    by_id = {item.id: item for item in items}
    missing = [item_id for item_id in selected_ids if item_id not in by_id]
    if missing:
        raise ConfigError(f"unknown item(s): {', '.join(missing)}")
    return tuple(by_id[item_id] for item_id in selected_ids)
