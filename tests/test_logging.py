"""Test some simple combinations of functions and handlers."""
import logging
from typing import Any
from typing import Callable

from _pytest.logging import LogCaptureFixture

from graphty import Context
from graphty import node
from graphty.logging import LoggingHandler
from graphty.typing import Decorator


def test_logging(
    print: Callable[..., Any], decorator: Decorator, caplog: LogCaptureFixture
) -> None:
    """Check that caching fibonacci works."""
    caplog.set_level(logging.INFO)

    @decorator
    def fib(x: int) -> int:
        if x <= 1:
            return 1
        return fib(x - 1) + fib(x - 2)

    with Context(LoggingHandler(level=logging.INFO, logger=logging.getLogger())):
        assert fib(0) == 1
        assert fib(1) == 1
        assert fib(2) == 2
        assert fib(3) == 3

    caplog.clear()
    with Context(LoggingHandler(level=logging.INFO, logger=logging.getLogger())):
        assert fib(0) == 1

    assert caplog.records[0].getMessage() == f"{node(fib, 0)!r} ..."
    assert caplog.records[1].getMessage() == f"{node(fib, 0)!r} = 1"

    for record in caplog.records:
        assert record.funcname == "fib"  # type: ignore[attr-defined]
        assert record.kwargs["x"] == "0"  # type: ignore[attr-defined]
