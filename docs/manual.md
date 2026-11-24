# Model project manual

## Stable configuration

Root `ci.yml` defines permanent source branches, the generated build branch,
exact Forge/SolidCraft pins and repository roots.

## Branch integration

Promote accepted development with a merge-commit PR from `dev` to `main`.

Do not routinely merge `main` back into `dev` after that promotion. The
promotion merge commit itself does not need to be copied back.

Use `main` -> `dev` only when `main` contains real content that `dev`
does not have, such as a stable-branch hotfix. That integration also uses a
merge commit.

## CI modes

### Work branch / PR

A matching root `build.yml` controls exactly what runs:

```yaml
schema: 1
branch: issue/15-ci-change

modules:
  - ci
models: []
tasks:
  - test
  - build
```

If the branch field does not match the actual work branch, the file is ignored
and CI falls back to full.

### dev

`build.yml` is ignored.

CI finds the most recent successful push/workflow_dispatch run on `dev` and
uses its SHA as the baseline. The current `dev` SHA is the target.

```text
git diff --name-only <successful-baseline> <current-dev>
```

Only changed items plus declared impact run.

Because superseded runs are cancelled, an unfinished run never becomes the
baseline. A later dev run therefore automatically catches all changes since
the last successful one.

### main

`build.yml` is ignored and the complete repository runs.

## Item impact

Item-local `ci.yml` may declare:

```yaml
impact: self
```

or:

```yaml
impact: models
```

or:

```yaml
impact: full
```

Items can add extra watched paths:

```yaml
watch:
  - .github/workflows/ci.yml
```

Model ids are discovered from model roots; they are never centrally listed in
Python.

## Output

Generated artifacts remain below root `build/`.


## Model builds

Root `ci.yml` pins the complete qualified CAD toolchain:

- Forge repository, version and exact commit;
- released SolidCraft runtime image and exact SolidCraft version.

Model-local `ci.yml` owns build execution. A minimal processed model declares
its id, Forge source and optional build extras such as STL or snapshot framing.

CI selects physical model ids. The build module then performs one repository
scan and writes a deterministic `build-plan.json`.

For every selected model the normal build path is fixed:

```text
model.py
  -> pinned Forge on the CI runner
  -> solidcraft.json
  -> one shared SolidCraft Docker replay batch
  -> model.sc
  -> model.step
  -> model.png
  -> optional model.stl / extra PNG snapshots
```

Forge compilation and SolidCraft replay are separate visible phases. The
stored `solidcraft.json` is exactly the document replayed by SolidCraft.

During a run, generated output is written below the checkout:

```text
build/
  dev/
    build-plan.json
    models/
  main/
    build-plan.json
    models/
```

Successful permanent-branch runs then publish that scope to the generated
`build` branch. On that branch the repository root is:

```text
dev/
  build-plan.json
  models/
main/
  build-plan.json
  models/
```

PR/work-branch builds are verification-only and never publish. Incremental
`dev` publication replaces only selected model directories, preserves
unselected active models, and removes model directories that are no longer
active. A full `main` build replaces the complete `main/` scope.

Publication uses normal non-force pushes and checks that the source branch still
points at the source SHA being published. Pages/Hugo/`gh-pages` are a separate
later concern.
