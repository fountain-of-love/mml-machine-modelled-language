"""Uniform write/check command orchestration for reproducible research runners."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Any, Callable, Sequence


ResultAction = Callable[[Any], None]


@dataclass(frozen=True)
class ResearchCommand:
    """Callbacks that keep research policy outside generic CLI mechanics."""

    description: str
    run: Callable[[], Any]
    write: ResultAction
    check: ResultAction
    render: Callable[[Any], str]
    validate: ResultAction | None = None
    write_help: str = "Write machine-readable and human-readable results."
    check_help: str = "Check without changing results."


def run_research_command(
    command: ResearchCommand, argv: Sequence[str] | None = None
) -> Any:
    """Parse the common mode, execute callbacks in order, and print the report."""
    parser = argparse.ArgumentParser(description=command.description)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help=command.write_help)
    mode.add_argument("--check", action="store_true", help=command.check_help)
    args = parser.parse_args(argv)

    result = command.run()
    if command.validate is not None:
        command.validate(result)
    if args.write:
        command.write(result)
    else:
        command.check(result)
    print(command.render(result))
    return result
