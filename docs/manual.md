# Model project manual

## Stable configuration

Root `ci.yml` defines permanent branches, exact Forge pin and repository
roots.

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
