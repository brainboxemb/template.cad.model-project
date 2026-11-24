# Agent guidance

## Purpose

This repository is a reusable, self-contained CAD model-project template.

Models and Python capabilities use the same ownership pattern: each item has
its own directory, configuration and tests/verification.

## Start work

Before changing anything:

1. read `docs/plan.md`;
2. create/switch to a short-lived branch from `dev`;
3. update root `build.yml.branch` to the exact branch name;
4. select only the modules/models this branch changes;
5. select only the required tasks;
6. keep generated output below `build/`.

## Branch model

Permanent source branches are only `main` and `dev`.

Required integration:

- short-lived branch -> `dev`: squash;
- `dev` -> `main`: merge commit;
- `main` -> `dev`: merge commit.

Temporary branches use only configured prefixes from root `ci.yml`.

After a successful same-repository short-lived PR is merged into `dev`, its
source branch is removed by `modules/branch-cleanup`.

A standalone cleanup sweep may remove old temporary branches only when there is
no open PR and a merged PR proves integration into `dev`.

`main` and `dev` are never cleanup candidates.

## ci.yml and build.yml

Root `ci.yml` is stable repository configuration. It owns:

- permanent branch names and temporary branch prefixes;
- exact Forge repository/version/commit;
- module root;
- model root;
- generated output root.

Root `build.yml` is branch-specific execution selection.

On a non-main branch it must contain the exact current branch name, selected
modules/models and tasks. A mismatch is stale and CI fails.

On `main`, `build.yml` is ignored and the complete repository is
tested/built.

## Python modules

Every Python capability is a standalone item:

```text
modules/<id>/
  ci.yml
  pyproject.toml
  src/
  tests/
```

Tests for a Python capability live under that module. Root-level Python tests
are not allowed.

Current modules:

- `modules/ci` — configuration, selection and orchestration;
- `modules/build` — model build execution;
- `modules/merge-policy` — branch integration/merge method;
- `modules/branch-cleanup` — safe temporary branch cleanup.

A PR changing one module selects only that module in `build.yml`.

## Models

Every CAD model is a standalone item under `models/<id>/` with its own config,
metadata, engine source and model-owned verification when needed.

Do not create a central model catalog in Python.

## Workflows

Workflow YAML stays thin and bootstraps only its owning module.

- CI workflow -> `modules/ci`;
- merge workflow -> `modules/merge-policy`;
- branch cleanup workflow -> `modules/branch-cleanup`.

## build.yml merge ownership

`build.yml` is branch-local state. Target-branch preservation during
integration belongs to `modules/merge-policy`, not CI, build or cleanup.

## External ownership

Forge compiler/API behavior remains owned by
`lib.py.solidcraft.forge`.

Normal repository CI/build/merge/cleanup behavior is local to repositories
created from this template.
