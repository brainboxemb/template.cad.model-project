# template.cad.model-project

Self-contained template for CAD model repositories with independent model roots.

## Repository shape

```text
.github/workflows/
  ci.yml
  merge-policy.yml
cad_project/
  config.py
  models.py
  forge.py
  ci.py
  build.py
  merge_policy.py
tests/
AGENTS.md
README.md
pyproject.toml
ci.yml
build.yml
docs/
  plan.md
  manual.md
  handoff.md
models/
  simple-box/
    ci.yml
    model.yml
    scpf/model.py
build/                  # generated, ignored
```

## Branches

Permanent source branches:

- `main` — stable;
- `dev` — integration/development.

Short-lived branches squash into `dev`. `dev -> main` and `main -> dev`
preserve history with merge commits.

## Configuration split

`ci.yml` is the stable project CI/build contract, including the exact Forge
version and commit.

`build.yml` is the current human/agent work selection. Its `branch` value
must match the actual work branch. `main` ignores it.

## Output

Generated files go below root `build/`.

## First model

`models/simple-box` is the smallest Forge proof: one parameterized native Box.
