# Repository plan

This file contains unfinished work only.

## Now

### #7 — self-contained local CI modules

Replace the rejected inline model-building workflow with the intended local
architecture:

- workflow YAML is thin;
- root `ci.yml` owns the exact Forge pin and project roots;
- root `build.yml` owns current branch/model/task selection for humans/agents;
- CI never reads `build.yml`;
- small `cad_project.*` modules own configuration, model discovery, Forge
  execution, CI, working builds and merge policy;
- each module has focused tests;
- no shared CAD-CI or shared merge workflow is used.

Acceptance:

1. unit tests for the local modules are green;
2. CI builds `models/simple-box` from `ci.yml`;
3. generated result is below `build/models/simple-box/`;
4. changing/adding a model does not require a central model catalog;
5. a working build rejects stale `build.yml.branch`;
6. feature -> dev is squash;
7. dev -> main and main -> dev are merge commits.

## Later

Use the accepted template to migrate one real CAD project before adding site,
release, gallery or additional engine features.

## Repository setting still required

GitHub branch/ruleset protection should require pull requests for `main` and
`dev` so direct pushes/manual merges cannot bypass the local merge policy.

The connected GitHub app cannot configure administration-level protection.
