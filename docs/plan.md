# Repository plan

This file contains unfinished work only.

## Now

### #17 — dispatch target CI after local merge

After a successful local merge-policy integration, explicitly dispatch the
local CI workflow on the PR base branch.

This is required because GITHUB_TOKEN merges do not reliably create a second
push-triggered Actions run.

Acceptance:

1. merge-policy has actions: write;
2. dispatch occurs only after successful merge;
3. dev target dispatch enters incremental dev CI;
4. main target dispatch enters full CI;
5. rapid dev dispatches are coalesced by CI cancel-in-progress.

## Accepted

- work branches use matching build.yml;
- dev uses changes since last successful integration CI;
- main runs full;
- cancelled dev runs do not advance the baseline;
- item impact is local to each item;
- standalone branch cleanup is active.

## Later

Migrate one real CAD project before adding site/release/gallery scope.
