# Repository handoff

~~~text
Continue work on brainboxemb/template.cad.model-project.

Read AGENTS.md and docs/plan.md first.

Core rules:

- main is stable; dev is the only permanent development branch;
- feature -> dev is squash; dev <-> main uses merge commits;
- root ci.yml is stable project configuration including exact Forge pin;
- root build.yml is the exact current work-branch selection;
- main ignores build.yml and runs all items;
- Python capabilities are independent modules under modules/<id>/ with their
  own ci.yml, package source and tests;
- Python tests never live at repository root;
- CAD models are independent roots under models/<id>/;
- CI and merge workflows are thin bootstraps for their owning local module;
- generated output belongs below build/;
- build.yml target-branch preservation belongs to modules/merge-policy.

For a one-module PR, select only that module in build.yml.
~~~
