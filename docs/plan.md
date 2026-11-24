# Repository plan

This file contains unfinished work only.

## Current baseline

Stage 1 establishes the smallest useful CAD model-project template:

- permanent branches: `main` and `dev`;
- feature -> dev uses squash;
- dev <-> main integration preserves history with merge commits;
- root `ci.yml` is stable CI/project configuration;
- root `build.yml` is human/agent working-build selection only;
- model roots live independently below `models/`;
- generated output lives below ignored `build/`;
- one Forge model proves the initial authoring/build path.

## Now

### #1 — stage-1 baseline

Acceptance:

1. repository structure and documentation exist;
2. `dev` is the only permanent development branch;
3. shared merge policy is configured for `main` + `dev`;
4. normal CI builds the Forge `simple-box` without reading `build.yml`;
5. the result is written below `build/models/simple-box/`;
6. no repository Python helper/orchestrator is required.

## External owner gaps

These are tracked in their owner repositories and must not be worked around by
copying generic code here:

- `lib.py.cad.ci #141` — normal root configuration name `ci.yml`;
- `lib.py.cad.ci #142` — reusable generic Forge model builder.

The stage-1 direct Forge compile is intentionally small. Replace it with the
released generic CAD-CI path once those owner capabilities are accepted.

## Next

After stage 1:

- prove a second independent model can be added without editing the first;
- add focused model verification only where the model needs it;
- migrate a real CAD project to this structure before expanding the template.

Do not add site generation, release automation, multiple development branches
or a central model catalog until a real migrated project demonstrates the need.
