# Repository plan

This file contains unfinished work only.

## Accepted baseline

Stage 1 is accepted:

- permanent source branches: `main` and `dev`;
- short-lived branch -> `dev`: squash through the shared merge policy;
- `dev` -> `main` and `main` -> `dev`: merge commits;
- root `ci.yml` is stable project/CI configuration;
- root `build.yml` is human/agent working-build selection only;
- normal CI does not read `build.yml`;
- independent model roots live below `models/`;
- generated output lives below ignored `build/`;
- `models/simple-box` builds successfully with exact Forge v0.13.2.

The first accepted stable baseline is main commit
`c297799bd87b1ead3a92ad0813f5b213ad921734`.

The first policy-driven permanent synchronization is dev commit
`5581f7521d023facce0da9f4b23f17800716d5c9`, a two-parent merge commit.
Its policy-dispatched CI run `45369555427` is green.

## External owner gaps

Do not work around these by copying generic code into the template:

- `lib.py.cad.ci #141` — normal root configuration name `ci.yml`;
- `lib.py.cad.ci #142` — reusable generic Forge model builder.

The current direct Forge compile is intentionally small and temporary.

## Next

Use this template to migrate one real CAD model project before expanding it.

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
`main` and `dev` so manual merge/direct-push paths cannot bypass that policy.
This repository currently has no ruleset. Configure that in GitHub repository
settings; it cannot be written by the connected GitHub app used here.
