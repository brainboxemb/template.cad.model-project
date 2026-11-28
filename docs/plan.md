# Repository plan

This file is the canonical repository plan on stable `main` and contains
unfinished work only. Agents working on any lane must read this `main` copy;
branch-local copies are not independent plans.

Governance-only changes to `AGENTS.md`, `docs/plan.md` and
`docs/handoff.md` use a short-lived `docs/*` branch created from `main`
and return directly to `main` through repository-local `/merge`. Do not
create a `main -> dev` sync merely to copy plan/handoff metadata.

## Now

### #141 — materialize rolling test output over durable dev baseline

Fix the generic rolling `test` publication discovered by the real CAD catalog:
keep PR builds bounded, but publish one complete review scope by copying the
current durable `build/dev` scope and overlaying the selected candidate model
outputs. Preserve candidate source/SHA/toolchain evidence at the test-plan
level and each baseline model row's own build-source evidence.

## Accepted architecture

- stable `main` owns the canonical repository plan and handoff state;
- normal product/model/module work starts from `dev`, with optional permanent
  `exp` for isolated experiments and explicit `dev <-> exp` checkpoints;
- work branch selection from matching `build.yml`;
- incremental `dev` and `exp` CI from each lane's last successful integration baseline;
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
- generated `build` branch with `main/`, `dev/`, `exp/` and one rolling
  `test/` scope; matching temporary `build.yml` opts into test publication
  with `output.scope: test` and fully replaces that single review scope;
- compact model `ci.yml` with optional primary snapshot camera;
- physical model owners may expand into multiple build variants;
- Pages links durable CAD artifacts from `build` and never republishes them;
- Pages publishes stable `/`, development `/dev/`, experimental `/exp/`
  and current rolling review `/test/` as one generated `gh-pages` tree;
- rolling test evidence retains exact source branch/SHA plus optional Forge
  qualification SHA, with no per-PR output directories or cleanup lifecycle.

## Next

After #141 is qualified and promoted, sync the exact template fix into
`brainboxemb/2026-011-02.cad.solidcraft` PR #291 and complete the real
bounded `simple-box` `/test/` acceptance before merging CAD #285.
