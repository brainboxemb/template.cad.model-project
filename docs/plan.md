# Repository plan

This file contains unfinished work only.

## Now

### #22 — dispatch branch cleanup after local merge

Local merge-policy already dispatches target CI after a successful merge.

Also dispatch the independent branch-cleanup workflow on the same target ref,
because GITHUB_TOKEN merges do not reliably emit pull_request: closed events.

Cleanup ownership remains entirely in modules/branch-cleanup.

## Accepted

- work branches use matching build.yml;
- dev uses changes since the last successful integration baseline;
- main runs full;
- superseded CI runs are cancelled;
- item impact is local to each item;
- local merge-policy dispatches target CI;
- branch cleanup is a separate module.

## Next

After the automatic cleanup dispatch is live-proven, migrate one real CAD
project before adding site/release/gallery scope.
