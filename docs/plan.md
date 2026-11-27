# Repository plan

This file is the canonical repository plan on stable `main` and contains
unfinished work only. Agents working on any lane must read this `main` copy;
branch-local copies are not independent plans.

Governance-only changes to `AGENTS.md`, `docs/plan.md` and
`docs/handoff.md` use a short-lived `docs/*` branch created from `main`
and return directly to `main` through repository-local `/merge`. Do not
create a `main -> dev` sync merely to copy plan/handoff metadata.

## Now

No active work selected.

## Accepted architecture

- stable `main` owns the canonical repository plan and handoff state;
- normal product/model/module work starts from `dev`;
- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- cancel-in-progress;
- item-local impact/watch metadata;
- directory-local model build priority;
- explicit physical-model dependency graph for assembly impact;
- `process: false` keeps a model owner discoverable and explicitly selectable
  on a matching work branch while excluding it from automatic/full permanent-lane
  model selection and automatic dependent expansion;
- local merge-policy owns all source-branch integration and dispatches target CI;
- governance-only `docs/* -> main` is squash and exhaustively restricted to
  `AGENTS.md`, `docs/plan.md` and `docs/handoff.md`;
- standalone cleanup removes merged temporary branches from their accepted
  integration target;
- direct Forge -> JSON -> one SolidCraft replay batch;
- Forge v0.19.0 / SolidCraft 0.49.0 / runtime v0.3.6 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- compact model `ci.yml` with optional primary snapshot camera;
- physical model owners may expand into multiple build variants;
- Pages links durable CAD artifacts from `build` and never republishes them;
- Pages publishes stable `/` and development `/dev/` presentation as one
  generated `gh-pages` tree.

## Next

No next work selected. Select an open issue deliberately before implementation;
do not infer work from stale branch-local plan text.
