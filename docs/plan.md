# Repository plan

This file contains unfinished work only.

## Now

### #10 — independent Python module roots

Perform the one-time migration from root `cad_project/` + root `tests/` to
independent module items under `modules/`.

Acceptance:

1. `modules/ci`, `modules/build` and `modules/merge-policy` each own
   `ci.yml`, package source and tests;
2. root Python package/tests are removed;
3. branch `build.yml` selects modules/models/tasks;
4. CI tests/builds only selected items on non-main branches;
5. main ignores `build.yml` and runs everything;
6. simple-box still builds through `modules/build`;
7. workflows only bootstrap their owning local module.

### merge-policy build.yml preservation

After the module layout is accepted, update `modules/merge-policy` in its own
PR so branch integration preserves the target branch's own `build.yml`.

That module owns the rule; do not add exceptions in `modules/ci`.

## Later

After module boundaries and branch-local build selection are proven, migrate
one real CAD project to this template before adding site/release/gallery scope.
