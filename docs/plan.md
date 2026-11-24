# Repository plan

This file contains unfinished work only.

## Now

### #15 — incremental dev CI

Implement three CI selection modes:

- work branch/PR: matching `build.yml`;
- dev: changed paths since the last successful dev integration build;
- main: full.

Requirements:

1. stale build.yml is ignored, not failed;
2. dev baseline comes only from successful push/workflow_dispatch CI;
3. cancelled dev runs do not advance that baseline;
4. unsafe/missing baseline falls back to full;
5. changed-item impact is item-local;
6. CI concurrency cancels superseded runs.

## Accepted

- independent Python module roots;
- branch-local work selection;
- standalone branch cleanup;
- only main/dev remain as permanent branches.

## Later

After incremental dev selection is proven live, migrate one real CAD project
before expanding site/release/gallery scope.
