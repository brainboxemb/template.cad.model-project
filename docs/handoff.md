# Repository handoff

~~~text
Continue work on brainboxemb/template.cad.model-project.

Read AGENTS.md and the canonical docs/plan.md from stable main first, regardless
of which development lane will be used.

Core rules:

- main is stable and owns the canonical repository plan/handoff state;
- dev is the only permanent development source branch;
- normal short-lived product/model/module work starts from dev and squash-merges
  back to dev;
- governance-only changes limited to AGENTS.md, docs/plan.md and
  docs/handoff.md start from main on a docs/* branch and squash directly back
  to main through /merge;
- do not maintain a competing branch-local plan on dev;
- do not create main -> dev merely to copy plan/handoff metadata;
- dev -> main promotion is a merge commit;
- main -> dev happens only for real stable-only product content missing from
  dev, never merely to copy a promotion merge commit;
- every source integration uses repository-local /merge; never choose the merge
  method manually;
- root ci.yml owns stable toolchain and generated branch configuration;
- root build.yml is the exact normal work-branch selection;
- main ignores build.yml and runs full;
- internal Python capabilities live under modules/<id>/ and execute from src/;
- CAD models are physical owner roots discovered from model-local ci.yml;
- one owner may expand into multiple build variants;
- generated CAD output is stored on build/{dev,main};
- model.png is implicit; STL and additional snapshots are opt-in model config;
- site/model presentation uses shared Hugo/Hextra layouts;
- model.yml owns presentation metadata, ci.yml owns build/source identity;
- optional page.md and extra_views extend a model page without custom
  model-name branches;
- Pages runs separately and is dispatched after build publication; CI does not
  wait for it;
- generated gh-pages publishes main at / and dev at /dev/;
- Pages uses branch publication, not deploy-pages/github-pages environment
  deployment.
~~~
