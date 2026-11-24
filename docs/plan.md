# Repository plan

This file contains unfinished work only.

## Now

### #72 — support a model-owned primary snapshot camera

Extend the generic model-build contract so a physical model can optionally own
the camera used for its primary `model.png`.

The contract is:

```yaml
snapshot:
  camera:
    target: [0, 0, 160]
    yaw: -0.24
    pitch: 0.20
    distance: 920
    fov: 0
```

Omitting `snapshot` preserves the existing SolidCraft default camera.
Additional named `snapshots:` remain independent.

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

After #72 is accepted on `main`, sync the build-module change to the active
CAD migration repository and continue the final six-root migration batch.
