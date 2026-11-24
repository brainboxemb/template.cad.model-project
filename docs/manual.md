# Model project manual

## Branch workflow

Create work from `dev`.

```text
dev
  -> issue/<number>-short-name
  -> pull request to dev
  -> squash merge
```

Promote an accepted development checkpoint with a pull request:

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

Root `ci.yml` describes the stable project/CI item set.

It does not describe what an agent happens to be working on today.

Each model owns its own item configuration at:

```text
models/<id>/ci.yml
```

## build.yml

Root `build.yml` is for humans/agents.

Example one-model work:

```yaml
schema: 1
branch: dev

models:
  - simple-box

tasks:
  - build
```

Example future all-model work:

```yaml
schema: 1
branch: dev

models: all

tasks:
  - build
```

Normal GitHub CI never reads `build.yml`.
`main` ignores it.

A feature branch may update its model/task selection before work starts. Keep
`branch: dev` because the plan belongs to the single permanent development
line.

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

## Local Forge build

Stage 1 uses Forge v0.13.2 at exact commit:

```text
ea5710a5d2d33b0633b93c5da95dd5b74f126aa4
```

Create a virtual environment and install exactly that package:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "git+https://github.com/brainboxemb/lib.py.solidcraft.forge.git@ea5710a5d2d33b0633b93c5da95dd5b74f126aa4#subdirectory=scpf"
```

Build the example:

```bash
mkdir -p build/models/simple-box
python -m scpf models/simple-box/scpf/model.py \
  --out build/models/simple-box/solidcraft.json
```

The output is generated work and stays below ignored `build/`.

## Python modules

Do not create repository Python merely to wrap a shell command.

When Python is genuinely required, create one small module per responsibility
and a matching focused test module. Do not create one Python file that owns the
whole repository or knows every model.
