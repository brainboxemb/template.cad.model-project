# Agent guidance

## Purpose

This repository is a reusable, self-contained CAD model-project template.

Keep it smaller and clearer than the product repositories created from it.

## Start work

Before changing models:

1. read `docs/plan.md`;
2. read `build.yml`;
3. compare `build.yml.branch` with the actual Git branch;
4. update `build.yml` immediately when a new work branch is created;
5. change only the selected model(s) and their owned tests/configuration;
6. keep generated output below `build/`.

On `main`, ignore `build.yml`.

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

The repository owns this policy locally. Do not replace it with a shared
reusable merge workflow.

## CI architecture

The repository owns its CI implementation locally.

GitHub workflow YAML must stay thin. It may:

- define triggers and permissions;
- check out the repository;
- bootstrap the local Python package;
- invoke focused local project modules.

Workflow YAML must **not** contain:

- Forge repository/version/commit pins;
- model ids or model paths;
- direct `python -m scpf` model execution;
- model selection logic;
- build-output path logic;
- merge-method classification;
- large shell/Python implementations.

Those responsibilities belong in versioned repository configuration and small,
tested Python modules.

The root `ci.yml` is the stable CI/build contract. It owns:

- exact Forge dependency repository/version/commit;
- model source root;
- generated output root.

Normal CI uses `ci.yml` and builds the repository model set. It never reads
`build.yml`.

## Working builds

Root `build.yml` is only for humans/agents.

It owns:

- the exact work-branch name;
- selected model ids or `all`;
- requested work tasks.

If `build.yml.branch` does not equal the actual branch, the file is stale and
a working build must refuse to run.

`main` ignores `build.yml`.

## Generated output

All generated output belongs below root `build/`.

Never write generated output into a model source directory.

## Models

Every `models/<id>/` directory is independently owned.

A model root contains its own:

- `ci.yml`;
- `model.yml`;
- engine source such as `scpf/model.py`;
- focused tests or verification when needed.

Do not create a central model catalog in Python.

## Python modules

Repository Python follows the same ownership rule as models: small modules with
one clear responsibility and focused tests.

Current modules are deliberately separated:

- `cad_project.config` — configuration parsing/validation;
- `cad_project.models` — independent model discovery/selection;
- `cad_project.forge` — Forge installation and one-model execution;
- `cad_project.ci` — CI entrypoint using only `ci.yml`;
- `cad_project.build` — developer/agent entrypoint using `build.yml`;
- `cad_project.merge_policy` — branch-role and merge-method policy.

Do not add a catch-all `scripts/ci/*.py` layer.

A module should be independently changeable and verifiable by its own focused
tests.

## External ownership

Forge compiler/API behavior still belongs in `lib.py.solidcraft.forge`.

This template does **not** depend on shared CAD-CI or shared merge workflows.
Do not move its normal repository execution back into `tool.cad.ci` or
`lib.py.cad.ci`.
