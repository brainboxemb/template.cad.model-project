# template.cad.model-project

Minimal template for a CAD model project built around independent model roots.

The template is intentionally small. It is the clean baseline for model
repositories that need Forge authoring without inheriting product-specific CI,
site or historical repository structure.

## Repository shape

```text
.github/workflows/
  ci.yml
  merge-policy.yml
AGENTS.md
README.md
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

Merge rule:

```text
issue/* or feature/*
        |
        | squash
        v
       dev
        |
        | merge commit
        v
       main
```

Synchronization from `main` back to `dev` also preserves history with a
merge commit.

## CI and working builds

`ci.yml` is the stable project/CI configuration.

`build.yml` is a human/agent work instruction. Normal CI does not read it.
On `main` it is ignored.

Generated files go below `build/` and are never model source.

## First model

`models/simple-box` is the smallest Forge proof: one parameterized native Box.

See [docs/manual.md](docs/manual.md) for the exact local build command.
