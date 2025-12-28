from __future__ import annotations

import argparse
import subprocess
from typing import List


def generate_revision(message: str, autogenerate: bool = True) -> None:
    """Call Alembic revision with the given message."""
    cmd: List[str] = ["alembic", "revision", "-m", message]
    if autogenerate:
        cmd.append("--autogenerate")
    subprocess.check_call(cmd)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an Alembic migration revision.")
    parser.add_argument("message", help="Migration message, e.g. 'add users table'")
    parser.add_argument(
        "--no-autogenerate",
        action="store_true",
        help="Create an empty revision without schema autogeneration.",
    )
    args = parser.parse_args()
    generate_revision(args.message, autogenerate=not args.no_autogenerate)


if __name__ == "__main__":
    main()
