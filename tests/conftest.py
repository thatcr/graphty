"""Common fixures for testing grafty."""
import sys
from typing import Any

import pytest
from _pytest.python import Metafunc
from rich.console import Console


def pytest_generate_tests(metafunc: Metafunc) -> None:
    """Map decorator fixture to list of decorators to test."""
    import graphty.wrapper

    decorators = [graphty.wrapper.shift]

    if "decorator" in metafunc.fixturenames:
        metafunc.parametrize(
            "decorator", decorators, ids=[d.__module__ for d in decorators]
        )


@pytest.fixture(name="print", autouse=True, scope="session")
def _print() -> Any:
    """Create a full-color rich terminal for logging."""
    console = Console(
        force_terminal=True,
        force_interactive=False,
        file=sys.stdout,
        record=False,
    )

    return console.print
