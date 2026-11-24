# Repository plan

This file contains unfinished work only.

## Now

### #48 — first durable model page

Publish `simple-box` through the accepted Hugo 0.169.0 + Hextra v0.13.0
presentation layer.

The page must join:

- presentation metadata from `model.yml`;
- source/build identity from `ci.yml`;
- accepted artifacts from generated `build/main`.

The shared page layout supports optional model-owned `page.md` prose and
declarative `extra_views`; it must not contain model-name branches.

Stable publication goes to generated `gh-pages` only after a successful
`main` run. PR site builds are read-only.

## Accepted architecture

- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- cancel-in-progress;
- item-local impact/watch metadata;
- local merge-policy dispatches target CI and branch cleanup;
- standalone cleanup removes merged temporary branches;
- direct Forge -> durable JSON -> one SolidCraft replay batch;
- generated `build` branch with `dev/` and `main/` scopes;
- compact model `ci.yml` with implicit primary snapshot;
- physical model owners may expand into multiple build variants;
- internal Python capabilities run directly from source.

## Next

### #47 — model-group ordering before dependencies

After the first live model page is proven, add simple group priorities so
basic/component models can be migrated before advanced assemblies.

Priority is ordering only. Add explicit model dependencies later when the first
migrated assembly provides a concrete selection-propagation case.
