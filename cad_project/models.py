"""Discover independent model roots and resolve build selections."""

from __future__ import annotations

from pathlib import Path

from .config import ConfigError, ModelConfig, ProjectConfig, load_model_config


def discover_models(repo: Path, project: ProjectConfig) -> tuple[ModelConfig, ...]:
    root = repo / project.models_root
    if not root.is_dir():
        raise ConfigError(f"models root does not exist: {root}")

    models: list[ModelConfig] = []
    seen: set[str] = set()
    for child in sorted(root.iterdir(), key=lambda value: value.name):
        if not child.is_dir() or not (child / "ci.yml").is_file():
            continue
        model = load_model_config(child)
        if model.id in seen:
            raise ConfigError(f"duplicate model id: {model.id}")
        seen.add(model.id)
        models.append(model)

    if not models:
        raise ConfigError(f"no models found below: {root}")
    return tuple(models)


def select_models(
    models: tuple[ModelConfig, ...],
    selected_ids: tuple[str, ...] | None,
) -> tuple[ModelConfig, ...]:
    if selected_ids is None:
        return models

    by_id = {model.id: model for model in models}
    missing = [model_id for model_id in selected_ids if model_id not in by_id]
    if missing:
        raise ConfigError(f"unknown model(s): {', '.join(missing)}")
    return tuple(by_id[model_id] for model_id in selected_ids)
