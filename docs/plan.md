# Repository plan

This file contains unfinished work only.

## Now

### #69 — verify Pages PRs against the matching durable build scope

Use dev evidence for development-target PRs and dev-to-main promotions.
Keep model-only migration validation in CAD CI and Pages publication unchanged.

## Accepted architecture

- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- cancel-in-progress;
- item-local impact/watch metadata;
- local merge-policy dispatches target CI and branch cleanup;
- standalone cleanup removes merged temporary branches;
- direct Forge -> JSON -> one SolidCraft replay batch;
- generated `build` branch with `dev/` and `main/` scopes;
- compact model `ci.yml` with implicit primary snapshot;
- physical model owners may expand into multiple build variants;
- internal Python capabilities run directly from source;
- Pages runs separately from CAD CI and is explicitly dispatched after build publication;
- Pages publishes stable `/` and development `/dev/` as one generated `gh-pages` tree.

## Next

Use the accepted template baseline for the real CAD model migration. Add explicit model dependencies only when the first
advanced/assembly migration supplies a concrete dependency case.
