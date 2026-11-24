# Repository plan

This file contains unfinished work only.

## Current baseline

The repository structure is established:

- permanent source branches: `main` and `dev`;
- short-lived branch -> `dev`: squash through the shared merge policy;
- `dev` -> `main` and `main` -> `dev`: merge commits;
- root `ci.yml` is the intended stable project/CI configuration;
- root `build.yml` is human/agent working-build selection only;
- independent model roots live below `models/`;
- generated output belongs below ignored `build/`;
- `models/simple-box` is a valid minimal Forge model source;
- Forge is pinned in root `ci.yml` by version and exact commit.

The direct GitHub Actions Forge build used during bootstrap was rejected as
consumer-local CI implementation. Its successful run proves only that the model
source compiles; it is **not** accepted as the project CI architecture.

## Now

### #7 — remove repository-local CI implementation

Required:

1. no model build implementation in `.github/workflows/`;
2. `AGENTS.md` prohibits runtime/package/model build logic in repository
   workflows;
3. shared merge policy remains active without dispatching a local integration
   workflow;
4. model CI remains unavailable rather than being locally reimplemented until
   the released shared CAD-CI layer can consume this repository contract.

### Stage-1 shared CI completion

Stage 1 is complete only when the released shared CAD-CI stack can consume:

- root `ci.yml`;
- its exact Forge dependency pin;
- independent `models/*` roots;
- model-local `builder: forge`;
- generated output below `build/`;

without repository-owned generic build scripts or model commands in Actions.

External owner gaps:

- `lib.py.cad.ci #141` — normal root config name `ci.yml`;
- `lib.py.cad.ci #142` — generic Forge model builder.

Do not work around these gaps in this repository.

## Next

After shared CI works, use this template to migrate one real CAD model project
before expanding it.

That migration should prove:

1. a second independent model can be added without editing the first;
2. model-specific verification remains model-owned;
3. project-specific Python, if needed, is split into small independently tested
   modules;
4. no site, release or model-catalog machinery is added without a demonstrated
   project need.

## Repository setting still required

The shared merge policy selects the correct merge method when `/merge` is
used.

GitHub branch/ruleset protection must additionally require pull requests for
`main` and `dev` so direct pushes/manual merges cannot bypass that policy.
The connected GitHub app cannot configure administration-level protection.
