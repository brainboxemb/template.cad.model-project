# Repository handoff

Use this as the session entrypoint, not as a status log.

## Handoff message

~~~text
Continue work on brainboxemb/template.cad.model-project.

Start by inspecting current GitHub branches, issues and pull requests, then read
AGENTS.md and docs/plan.md.

Repository rules:

- main is stable;
- dev is the single permanent development branch;
- feature branches squash into dev;
- dev -> main and main -> dev preserve history with merge commits;
- root ci.yml is stable CI/project configuration;
- root build.yml is human/agent work selection only and main ignores it;
- generated output belongs below build/;
- every models/<id>/ root is independent;
- repository Python, when necessary, must be split into small independently
  tested modules rather than one central scripts/CI layer;
- GitHub Actions is orchestration-only and must never install/run Forge or
  contain model build logic;
- Forge version/commit belongs in root ci.yml;
- generic Forge/CAD-CI behavior must be fixed in its owner repository, not
  copied locally.

Use docs/plan.md for unfinished work. Do not infer current priorities from this
handoff.
~~~
