# Repository plan

This file contains unfinished work only.

## Now

### #11 — independent branch cleanup

Add `modules/branch-cleanup` as a standalone Python item.

Acceptance:

1. module owns its config, package and tests;
2. same-repository merged temporary branch -> dev is removable;
3. main/dev are never removable;
4. manual sweep requires no open PR plus merged-PR proof;
5. workflow bootstraps only the cleanup module;
6. current stale bootstrap branches are removed after acceptance.

### merge-policy build.yml preservation

Update `modules/merge-policy` in its own PR so integration preserves the
target branch's own `build.yml`. Do not solve this in CI or cleanup.

## Accepted direction

Python capabilities and CAD models are independent build items. Non-main
branches use `build.yml` to select exactly what is tested/built; main ignores
it and runs the complete repository.

## Later

After module boundaries, cleanup and branch-local build selection are proven,
migrate one real CAD project before adding site/release/gallery scope.
