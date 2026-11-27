# Agent guidance

## Purpose

This repository is a reusable, self-contained CAD model-project template.

Models and Python capabilities use the same ownership pattern: each item has
its own directory, configuration and tests/verification.

## Start work

Before changing anything, read the canonical `docs/plan.md` from stable
`main`, even when the current work will happen on `dev`.

Then classify the change:

- repository-governance only: if the complete change is limited to
  `AGENTS.md`, `docs/plan.md` and/or `docs/handoff.md`, create a
  short-lived `docs/*` branch from `main` and target `main` directly;
- normal product/model/module work: create a short-lived branch from `dev`,
  update root `build.yml.branch` to the exact branch name, select only the
  modules/models and tasks this branch changes, and keep generated output below
  `build/`.

Do not treat a branch-local copy of `docs/plan.md` as a competing plan.

## Branch model

Permanent source branches are only `main` and `dev`.

Required integration:

- normal short-lived branch -> `dev`: squash;
- governance-only `docs/*` branch from `main` -> `main`: squash, only
  when every changed path is one of `AGENTS.md`, `docs/plan.md`,
  `docs/handoff.md`;
- `dev` -> `main`: merge commit when promoting accepted development;
- `main` -> `dev`: merge commit only when `main` contains actual product
  content that is not already present on `dev`, for example a stable-branch
  hotfix. Do not sync plan/handoff metadata to `dev` merely because it changed
  on `main`.

### Mandatory merge execution rule

This repository deliberately does **not** let an agent choose the merge method.

For every source-branch integration above, including the governance-only
`docs/* -> main` route, an agent MUST post `/merge` on the pull request and
let `.github/workflows/merge-policy.yml` perform the merge.

An agent MUST NOT:

- call GitHub's direct merge API;
- enable or use auto-merge;
- use a UI merge as a fallback;
- manually choose squash, merge or rebase.

If `/merge` fails, stop the integration and repair the merge-policy path.
Never bypass the policy. This rule exists specifically to prevent an agent from
selecting the wrong merge method.

Do not create a `main` -> `dev` PR merely to copy the promotion merge
commit back into `dev`.

Temporary branches use only configured prefixes from root `ci.yml`.

After a successful same-repository short-lived PR is merged into its allowed
target (`dev` for normal work, or `main` for governance-only `docs/*`
work), its source branch is removed by `modules/branch-cleanup`.

`main` and `dev` are never cleanup candidates.

The generated `build` branch is not a source branch. It stores generated technical
output for the permanent source scopes and is never a cleanup candidate.

The generated `gh-pages` branch is also not a source branch. Pages are built
from `main + build/main` and `dev + build/dev`, assembled as one tree, and
published there after successful build publication.

## CI selection modes

CI has three modes.

### Work branch / PR

If `build.yml.branch` matches the actual branch, use its explicit
module/model/task selection.

If it does not match, ignore `build.yml` and run full. A stale build file is
not a CI failure.

### process-disabled model owners

A model-local `ci.yml` may set `process: false` to park that physical owner.

The owner remains discoverable and dependency-validated. A matching work-branch
`build.yml` may explicitly select it for focused work. Normal/full/incremental
automatic selection on permanent lanes excludes it, and dependent expansion
must not automatically re-add it.

### dev

Ignore `build.yml`.

Use the last successful dev **push/workflow_dispatch** CI SHA as baseline and
the current dev SHA as target. Build/test the changed items in that Git range,
plus item-declared impact.

A cancelled dev run never advances the successful baseline. If two squash
merges arrive quickly, the newer run therefore includes changes not completed
by the cancelled run.

If no safe successful baseline exists, run full.

### main

Ignore `build.yml` and run full.

## Build output

Successful permanent-branch model builds publish to the generated branch
configured by `ci.yml.generated.build_branch`.

The generated branch contains complete build scopes:

```text
dev/
  build-plan.json
  models/
main/
  build-plan.json
  models/
```

PR/work-branch output is verification-only and is never published. Incremental
`dev` publication replaces only rebuilt model directories and preserves other
active model output. `main` is full and replaces its complete scope.

## Pages

Hugo/Hextra presentation lives below `site/`.

The page data boundary is explicit:

- `model.yml`: presentation metadata;
- `ci.yml`: build/source identity and variants;
- generated `build/main`: accepted model artifacts;
- optional model-local `page.md`: additional background prose;
- optional model metadata `extra_views`: additional reference/build views.

Shared layouts must not branch on model names. Model-specific content belongs in
model-owned metadata/resources. Pages never runs Forge or SolidCraft.

Pages runs separately from CAD CI. After successful permanent build
publication, CI dispatches `pages.yml` and finishes without waiting. That
workflow rebuilds both the stable root and `/dev/`, then publishes the complete
tree to `ci.yml.generated.pages_branch` (`gh-pages`).

## Item impact

Impact is declared by the item that owns it, not by a central model catalog.

- `modules/ci`: `impact: full`;
- `modules/build`: `impact: models`;
- other modules default to self;
- models default to self.

An item may add extra watched paths, for example its thin workflow YAML.

## Python modules

Every Python capability is a standalone item:

```text
modules/<id>/
  ci.yml
  pyproject.toml
  src/
  tests/
```

Tests for a capability live under that module. Root-level Python tests are not
allowed.

## Models

Every CAD model is a standalone item under `models/<id>/`.

Do not create a central model catalog in Python.

## Workflows

Workflow YAML stays thin and bootstraps only its owning module.

The CI workflow uses concurrency with cancellation so a newer run supersedes an
older run for the same Git ref.

## External ownership

Forge compiler/API behavior remains owned by
`lib.py.solidcraft.forge`.

Normal repository CI/build/merge/cleanup behavior is local to repositories
created from this template.
