# Repository plan

This file contains unfinished work only.

## Current acceptance

The template now has:

- one stable `main` and one development `dev` branch;
- independent Python modules with module-local tests;
- independent CAD model roots;
- branch-local work selection through `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- CI cancellation for superseded runs;
- item-local impact/watch metadata;
- local merge-policy with target CI dispatch;
- independent branch cleanup.

## Now

### #20 — end-to-end local merge acceptance

Prove one docs-only PR through:

```text
work branch
  -> matching build.yml
  -> /merge
  -> squash into dev
  -> explicit target CI dispatch
  -> incremental docs-only dev run
  -> branch cleanup
```

Expected: no CAD model or unrelated module build.

## Next

After this acceptance proof, use the template to migrate one real CAD project
before adding site/release/gallery scope.
