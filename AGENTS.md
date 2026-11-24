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

Permanent source branches:

- `main` — stable;
- `dev` — development/integration.

Required merge behavior:

- short-lived branch -> `dev`: squash;
- `dev` -> `main`: merge commit;
- `main` -> `dev`: merge commit.

Feature branches never merge directly to `main`.

## ci.yml and build.yml

Root `ci.yml` is stable repository configuration. It owns:

- permanent branch names;
- exact Forge repository/version/commit;
- module root;
- model root;
- generated output root.

Root `build.yml` is branch-specific execution selection.

On a non-main branch it must contain:

- the exact current branch name;
- selected modules or `all`;
- selected models or `all`;
- tasks such as `test` and `build`.

If `build.yml.branch` does not match the actual branch, CI must fail as stale.

On `main`, `build.yml` is ignored and the complete repository is
tested/built.

## Python modules

Every Python capability is a standalone item below:

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

- `modules/ci` — project config, item discovery, branch selection and
  orchestration;
- `modules/build` — model build execution;
- `modules/merge-policy` — branch integration policy.

A PR that changes one module should select that one module in `build.yml` so
only that module is built/tested.

Do not create a repository-wide Python package or root `tests/` directory.

## Models

Every CAD model is a standalone item below:

```text
models/<id>/
  ci.yml
  model.yml
  <engine source>
  <model-owned verification when needed>
```

Do not create a central model catalog in Python.

## Workflows

Workflow YAML stays thin.

`.github/workflows/ci.yml` may bootstrap only `modules/ci` and invoke it.
It must not name Forge, models or build output paths.

`.github/workflows/merge-policy.yml` may bootstrap only
`modules/merge-policy` and invoke it.

## build.yml merge ownership

`build.yml` is branch-local state.

When a short-lived branch is squashed into `dev`, or permanent branches are
integrated, the target branch must retain/receive its own valid `build.yml`
rather than inheriting a stale source-branch name.

This normalization belongs to `modules/merge-policy`, not to CI or model code.

## External ownership

Forge compiler/API behavior remains owned by
`lib.py.solidcraft.forge`.

Normal project CI/build/merge behavior for repositories created from this
template is local to the repository; it does not use shared CAD-CI workflows.
