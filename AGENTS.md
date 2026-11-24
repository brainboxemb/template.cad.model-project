# Agent guidance

## Purpose

This repository is a reusable CAD model-project template.

Keep it smaller and clearer than the product repositories created from it.

## Start work

Before changing models:

1. read `docs/plan.md`;
2. read `build.yml`;
3. confirm the work targets the `dev` development line;
4. change only the selected model(s) and their owned tests/configuration;
5. keep generated output below `build/`.

## Branch model

Permanent source branches are only:

- `main`;
- `dev`.

Use short-lived branches for changes.

Required integration:

- short-lived branch -> `dev`: squash merge;
- `dev` -> `main`: merge commit;
- `main` -> `dev`: merge commit.

Do not merge feature branches directly to `main`.

## CI versus working builds

Do not mix CI selection with current agent/developer work selection.

- root `ci.yml` is stable project/CI configuration;
- root `build.yml` is current work selection for humans/agents;
- GitHub CI never uses `build.yml`;
- `main` ignores `build.yml`;
- generated output is always below root `build/`.

A feature branch based on `dev` may change the model/task selection in
`build.yml`. The `branch: dev` field identifies the permanent development
line the work plan belongs to.

## Models

Every `models/<id>/` directory is independently owned.

A model root contains its own:

- `ci.yml`;
- `model.yml`;
- engine source such as `scpf/model.py`;
- focused tests or verification when needed.

Do not create a central Python catalog that needs to know every model.

## Python

Prefer no repository Python outside model source unless a repository concern
actually requires it.

If Python is needed, use small independent modules with one responsibility and
focused tests, for example:

```text
project/
  build_config.py
  branch_state.py
tests/
  test_build_config.py
  test_branch_state.py
```

Do not add a catch-all `scripts/ci/*.py` orchestration layer.

Each module must be independently testable and reviewable in a small PR.

## Ownership

- Forge authoring/compiler behavior belongs in `lib.py.solidcraft.forge`.
- Generic CAD-CI behavior belongs in `lib.py.cad.ci` / `tool.cad.ci`.
- This repository owns only project configuration and model source.

Do not copy generic owner code into this template to work around an upstream
gap.
