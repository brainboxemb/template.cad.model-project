"""CLI entrypoint for one configured CAD model build."""

from __future__ import annotations

import argparse
from pathlib import Path

from .forge import build_model, install_forge


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--forge-repository", required=True)
    parser.add_argument("--forge-version", required=True)
    parser.add_argument("--forge-commit", required=True)
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()

    install_forge(args.forge_repository, args.forge_commit)
    build_model(
        model_id=args.model_id,
        source=Path(args.source),
        output_root=Path(args.output_root),
    )


if __name__ == "__main__":
    main()
