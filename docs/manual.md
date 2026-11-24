# Model project manual

## Branch workflow

Create work from `dev`.

```text
dev
  -> issue/<number>-short-name
  -> pull request to dev
  -> squash merge
```

Promote accepted development with `dev -> main`; synchronize with
`main -> dev`. Both permanent-branch integrations use merge commits.

## ci.yml

Root `ci.yml` is the stable CI/build contract:

```yaml
schema: 1

dependencies:
  forge:
    repository: brainboxemb/lib.py.solidcraft.forge
    version: 0.13.2
    commit: ea5710a5d2d33b0633b93c5da95dd5b74f126aa4

models:
  root: models

output:
  root: build
```

CI reads this file. Workflow YAML does not repeat these values.

## Model roots

Every direct child below `models/` with a `ci.yml` is independent.

```text
models/simple-box/
  ci.yml
  model.yml
  scpf/model.py
```

Minimal model CI config:

```yaml
schema: 1
id: simple-box
builder: forge
source: scpf/model.py
```

## build.yml

`build.yml` is for humans/agents, not CI.

On a work branch:

```yaml
schema: 1
branch: issue/12-change-box

models:
  - simple-box

tasks:
  - build
```

For all models use `models: all`.

When a new branch is created, update `branch` immediately. A mismatch is a
stale work plan and `python -m cad_project.build` refuses to run.

On `main`, `build.yml` is ignored.

## Commands

Install the local project package:

```bash
python -m pip install -e .
```

Run module tests:

```bash
python -m unittest discover -s tests -v
```

Run normal repository CI locally:

```bash
python -m cad_project.ci
```

Run the current developer/agent selection:

```bash
python -m cad_project.build
```

Both build paths write generated output below `build/`.

## Python structure

Keep modules small and independently tested. Do not replace them with one large
CI script or place model-specific knowledge into generic modules.
