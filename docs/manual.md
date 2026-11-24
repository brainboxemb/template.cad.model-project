# Model project manual

## Stable configuration

Root `ci.yml` defines permanent branches, the exact Forge pin and roots for
modules, models and generated output.

## Working selection

Every non-main work branch updates root `build.yml`.

Example CI-module-only PR:

```yaml
schema: 1
branch: issue/12-ci-change

modules:
  - ci
models: []
tasks:
  - test
  - build
```

Example model-only PR:

```yaml
schema: 1
branch: issue/13-simple-box

modules: []
models:
  - simple-box
tasks:
  - build
```

Use `all` for either item class when required.

If the branch value is stale, CI fails.

On `main`, `build.yml` is ignored and all configured items run.

## Python module shape

```text
modules/<id>/
  ci.yml
  pyproject.toml
  src/
  tests/
```

A module PR keeps its tests inside the module and selects that module in
`build.yml`.

## Model shape

```text
models/<id>/
  ci.yml
  model.yml
  <engine source>
```

Model-specific verification stays with the model.

## Output

Generated artifacts are written below root `build/`.

## Workflows

CI workflow:

```text
checkout
  -> bootstrap modules/ci
  -> python -m cad_model_ci
```

Merge workflow:

```text
checkout
  -> bootstrap modules/merge-policy
  -> python -m cad_model_merge_policy
```

Forge pins and model names do not belong in workflow YAML.
