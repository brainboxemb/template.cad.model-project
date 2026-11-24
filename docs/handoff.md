# Repository handoff

Use this as the session entrypoint, not as a status log.

## Handoff message

~~~text
Continue work on brainboxemb/template.cad.model-project.

Start by inspecting current GitHub branches, issues and pull requests, then read
AGENTS.md and docs/plan.md.

Repository rules:

- main is stable; dev is the single permanent development branch;
- feature branches squash into dev;
- dev -> main and main -> dev use merge commits;
- the repository owns CI and merge policy locally; no shared reusable workflow;
- workflow YAML stays thin and calls small local cad_project modules;
- root ci.yml contains stable CI/build configuration including the exact Forge
  version/commit;
- root build.yml is human/agent work selection only;
- build.yml.branch must match the actual work branch; main ignores build.yml;
- generated output belongs below build/;
- every models/<id>/ root is independent;
- Python modules must remain small, separately tested and free of central model
  catalog knowledge.

Use docs/plan.md for unfinished work.
~~~
