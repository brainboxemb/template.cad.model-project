# Repository plan

This file contains unfinished work only.

## Now

### #86 — adopt Forge v0.15.0

Adopt release source `efc88bfcaf452051d721347f2e5ca561decad654`
while keeping SolidCraft 0.48.1/runtime v0.3.5 unchanged.

This release carries native applied-feature pattern sources (#347), the
component-context replay fix (#753), and native exploded assembly views (#751).


### #81 — make local /merge mandatory for agents

The repository-local merge policy exists specifically to prevent agents from
choosing the wrong merge method.

For every source-branch integration, agents must use a PR conversation comment:

```text
/merge
```

The merge-policy workflow remains the sole owner of merge-method selection.

Direct GitHub merge API calls, auto-merge and UI/manual merge fallback are
forbidden for agents. A failed merge-policy run must be repaired, never
bypassed.

## Accepted architecture

- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- cancel-in-progress;
- item-local impact/watch metadata;
- directory-local model build priority;
- explicit physical-model dependency graph for assembly impact;
- local merge-policy owns all source-branch integration and dispatches target CI;
- standalone cleanup removes merged temporary branches;
- direct Forge -> JSON -> one SolidCraft replay batch;
- Forge v0.15.0 / SolidCraft 0.48.1 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- compact model `ci.yml` with optional primary snapshot camera;
- physical model owners may expand into multiple build variants;
- Pages links durable CAD artifacts from `build` and never republishes them;
- Pages publishes stable `/` and development `/dev/` presentation as one generated `gh-pages` tree.

## Next

Accept #81 through the local `/merge` path itself, then promote it to
`main` through the same policy. Sync the agent rule to the active CAD
migration repository.
