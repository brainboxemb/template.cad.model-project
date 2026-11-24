# Repository plan

This file contains unfinished work only.

## Now

### #88 — upgrade Forge baseline to v0.15.0

The template must track the accepted Forge baseline used by the current CAD
repository. Forge v0.15.0 fixes component-context restoration during headless
replay (#753), preventing component-local joined Cylinder tool geometry from
remaining visible in root/world space.

Accepted pin:

- Forge v0.15.0
- commit `efc88bfcaf452051d721347f2e5ca561decad654`
- SolidCraft 0.48.1
- runtime `ghcr.io/brainboxemb/cad-solidcraft:v0.3.5`

## Accepted architecture

- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- cancel-in-progress;
- item-local impact/watch metadata;
- directory-local model build priority;
- explicit physical-model dependency graph for assembly impact;
- local merge-policy owns all source-branch integration and dispatches target CI;
- standalone cleanup removes merged temporary branches;
- direct Forge -> JSON -> one SolidCraft replay batch;
- Forge v0.15.0 / SolidCraft 0.48.1 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- compact model `ci.yml` with optional primary snapshot camera;
- physical model owners may expand into multiple build variants;
- Pages links durable CAD artifacts from `build` and never republishes them;
- Pages publishes stable `/` and development `/dev/` presentation as one generated `gh-pages` tree.

## Next

Accept #88 through local `/merge`, promote it to `main`, then sync the exact
toolchain pin to the active CAD repository and rebuild `hub75-screen`.
