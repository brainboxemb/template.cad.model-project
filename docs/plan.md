# Repository plan

This file contains unfinished work only.

## Now

### #75 — explicit physical-model dependencies

Add model-local dependency edges for real assembly/component relationships.

Contract:

```yaml
dependencies:
  - hub75-panel
  - corner-bracket
```

Dependencies name physical model owner ids. They are validated for unknown ids,
self references and cycles. Model selection closes transitively over downstream
dependents, and build-plan order is dependency-first.

Directory group priority remains ordering metadata only; it never creates a
dependency.

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
- internal Python capabilities run directly from source;
- Pages runs separately from CAD CI and is explicitly dispatched after build publication;
- Pages publishes stable `/` and development `/dev/` as one generated `gh-pages` tree.

## Next

After #75 is accepted on `main`, sync the generic CI/build changes to the
active CAD migration repository and migrate the final six historical roots.
