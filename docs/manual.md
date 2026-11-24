# Model project manual

## Branch workflow

Create work from `dev`.

```text
dev
  -> issue/<number>-short-name
  -> pull request to dev
  -> squash merge
```

Promote an accepted development checkpoint:

```text
dev -> main
```

That integration uses a merge commit.

Synchronize stable history back with:

```text
main -> dev
```

That also uses a merge commit.

## ci.yml

Root `ci.yml` is the stable project/CI contract.

It owns repository-wide build dependencies and item discovery. Forge is pinned
there by semantic version and exact commit:

```yaml
schema: 1

dependencies:
  forge:
    repository: brainboxemb/lib.py.solidcraft.forge
    version: 0.13.2
    commit: ea5710a5d2d33b0633b93c5da95dd5b74f126aa4

items:
  - models/*
```

Do not move dependency pins into GitHub Actions.

Each model owns its local item configuration at:

```text
models/<id>/ci.yml
```

## build.yml

Root `build.yml` is for humans/agents only.

Example one-model work:

```yaml
schema: 1
branch: dev

models:
  - simple-box

tasks:
  - build
```

Example all-model work:

```yaml
schema: 1
branch: dev

models: all

tasks:
  - build
```

Normal CI never reads `build.yml`.
`main` ignores it.

## Model roots

A model is independent:

```text
models/simple-box/
  ci.yml
  model.yml
  scpf/model.py
```

Adding or changing another model should not require editing
`models/simple-box`.

## Generated output

All generated model output belongs below:

```text
build/
```

The directory is ignored and is never model source.

## CI implementation boundary

Repository GitHub Actions must not install Forge or execute models directly.

The repository declares **what** exists in `ci.yml` and model-local
`ci.yml`. The released shared CAD-CI stack owns **how** those models are
selected, built and verified.

If the shared stack cannot yet consume the declared contract, leave CI blocked
and fix the owning shared layer. Do not add a local Python/shell/workflow
implementation.

## Python modules

Do not create repository Python merely to wrap a shell command.

When Python is genuinely required, create one small module per responsibility
and a matching focused test module. Do not create one Python file that owns the
whole repository or knows every model.
