# Repository plan

This file contains unfinished work only.

## Now

### #47 — model-group ordering before dependencies

Add directory-level group priorities so model migration/build order can proceed
from low-level models through components to advanced assemblies.

Priority is ordering only:

```text
basic / fundamentals   10
components             20
advanced / assemblies  30
```

Models inherit the nearest group `ci.yml`; equal priorities sort by owner id.
Do not add dependency propagation in this issue.

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
- Pages publishes stable `/` and development `/dev/` in one deployment.

## Next

After #47 is accepted, treat this template as the v1 baseline and start
migrating real CAD models. Add explicit model dependencies only when the first
advanced/assembly migration supplies a concrete dependency case.
