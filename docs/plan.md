# Repository plan

This file contains unfinished work only.

## Now

### #28 — central CI merge gate

The local merge-policy must qualify only the PR-specific central `ci` check.

Do not let merge-policy, branch cleanup or unrelated check-runs on the same SHA
block the merge gate.

Acceptance:

1. green PR-specific ci allows merge;
2. pending ci blocks;
3. failed ci blocks;
4. missing PR-specific ci blocks;
5. unrelated merge/cleanup checks are ignored.

## Accepted architecture

- work branch selection from matching build.yml;
- incremental dev CI from the last successful integration baseline;
- full main CI;
- cancel-in-progress;
- item-local impact/watch metadata;
- local merge-policy dispatches target CI and branch cleanup;
- standalone cleanup removes merged temporary branches.

## Next

After #28 is live-proven on main -> dev synchronization, migrate one real CAD
project before expanding site/release/gallery scope.
