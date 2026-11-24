# Repository plan

This file contains unfinished work only.

## Accepted architecture

The template now uses:

- `main` as stable branch;
- `dev` as the single development branch;
- squash for short-lived branch -> dev;
- merge commits for permanent branch integration;
- independent Python modules with module-local tests;
- independent CAD model roots;
- root `ci.yml` for stable project configuration and exact Forge pin;
- root `build.yml` for explicit work-branch selection;
- incremental dev CI from the last successful integration baseline;
- full main CI;
- cancel-in-progress for superseded CI runs;
- item-local impact/watch metadata;
- local merge-policy with explicit target-CI dispatch;
- independent branch cleanup with explicit post-merge dispatch.

## Current acceptance

### #26

Final docs-only end-to-end proof:

```text
work branch
  -> matching build.yml: no items
  -> /merge
  -> squash to dev
  -> dispatch CI(dev)
  -> dispatch branch-cleanup(dev)
  -> docs-only incremental dev run
  -> temporary branch removed
```

## Next

Use this template to migrate one real CAD project before adding
site/release/gallery scope.
