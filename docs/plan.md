# Repository plan

This file contains unfinished work only.

## Now

### #78 — keep generated CAD artifacts only on the build branch

Remove the accidental duplication of generated CAD output into `gh-pages`.

Pages may inspect the durable build plan and command JSON while rendering, but
must link generated output directly from:

```text
build/<scope>/models/<variant>/...
```

The model page uses build-plan paths for command JSON, PNG, SC, STEP, optional
STL and named snapshots. Stable and development Pages resolve `main` and
`dev` build scopes independently.

Source-owned presentation content may remain normal Hugo page resources.

## Accepted architecture

- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- cancel-in-progress;
- item-local impact/watch metadata;
- directory-local model build priority;
- explicit physical-model dependency graph for assembly impact;
- local merge-policy dispatches target CI and branch cleanup;
- standalone cleanup removes merged temporary branches;
- direct Forge -> JSON -> one SolidCraft replay batch;
- Forge v0.14.0 / SolidCraft 0.48.1 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- compact model `ci.yml` with optional primary snapshot camera;
- physical model owners may expand into multiple build variants;
- Pages links durable CAD artifacts from `build` and never republishes them;
- Pages publishes stable `/` and development `/dev/` presentation as one generated `gh-pages` tree.

## Next

After #78 is accepted on `main`, sync the Pages fix to the active CAD
migration repository and continue the final six-root migration.
