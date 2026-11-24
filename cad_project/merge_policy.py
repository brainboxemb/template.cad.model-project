"""Repository-local PR merge-method policy."""

from __future__ import annotations

import argparse
import json
import os
from urllib import request, error


class MergePolicyError(RuntimeError):
    """Raised when a PR cannot be merged under the repository policy."""


_ALLOWED_CHECK_RESULTS = {"success", "neutral", "skipped"}


def merge_method(*, head: str, base: str) -> str:
    if base == "dev" and head not in {"main", "dev"}:
        return "squash"
    if (head, base) in {("dev", "main"), ("main", "dev")}:
        return "merge"
    raise MergePolicyError(f"unsupported branch integration: {head} -> {base}")


def _api(repository: str, path: str, token: str, *, method: str = "GET", body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = request.Request(
        f"https://api.github.com/repos/{repository}/{path}",
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with request.urlopen(req) as response:
            return json.load(response)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise MergePolicyError(f"GitHub API {exc.code}: {detail}") from exc


def _require_green_checks(repository: str, sha: str, token: str) -> None:
    result = _api(repository, f"commits/{sha}/check-runs", token)
    check_runs = result.get("check_runs", [])
    if not check_runs:
        raise MergePolicyError("pull request head has no check runs")
    incomplete = [run["name"] for run in check_runs if run.get("status") != "completed"]
    if incomplete:
        raise MergePolicyError(f"checks still running: {', '.join(incomplete)}")
    failed = [
        run["name"]
        for run in check_runs
        if run.get("conclusion") not in _ALLOWED_CHECK_RESULTS
    ]
    if failed:
        raise MergePolicyError(f"checks not green: {', '.join(failed)}")


def execute(
    *,
    repository: str,
    pull_request_number: int,
    actor: str,
    repository_owner: str,
    token: str,
) -> str:
    if actor != repository_owner:
        raise MergePolicyError("only the repository owner may execute /merge")

    pr = _api(repository, f"pulls/{pull_request_number}", token)
    if pr.get("state") != "open":
        raise MergePolicyError("pull request is not open")

    head = pr["head"]["ref"]
    base = pr["base"]["ref"]
    method = merge_method(head=head, base=base)
    head_sha = pr["head"]["sha"]
    _require_green_checks(repository, head_sha, token)

    result = _api(
        repository,
        f"pulls/{pull_request_number}/merge",
        token,
        method="PUT",
        body={
            "sha": head_sha,
            "merge_method": method,
        },
    )
    if not result.get("merged"):
        raise MergePolicyError(result.get("message", "GitHub did not merge PR"))
    return result["sha"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--pull-request-number", required=True, type=int)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--repository-owner", required=True)
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN")
    if not token:
        raise MergePolicyError("GH_TOKEN is required")

    sha = execute(
        repository=args.repository,
        pull_request_number=args.pull_request_number,
        actor=args.actor,
        repository_owner=args.repository_owner,
        token=token,
    )
    print(sha)


if __name__ == "__main__":
    main()
