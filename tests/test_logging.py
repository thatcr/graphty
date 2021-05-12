"""Test some simple combinations of functions and handlers."""
import logging

from typing import Callable
from typing import Any

from graphty import Context
from graphty import key
from graphty.logging import LoggingHandler
from graphty.typing import Decorator


def test_fib(print: Callable[..., Any], decorator: Decorator, caplog) -> None:
    """Check that caching fibonacci works."""

    caplog.set_level(logging.INFO)

    @decorator
    def fib(x: int) -> int:
        if x <= 1:
            return 1
        return fib(x - 1) + fib(x - 2)

    with Context(
        LoggingHandler(level=logging.INFO, logger=logging.getLogger())
    ) as handler:
        assert fib(0) == 1
        assert fib(1) == 1
        assert fib(2) == 2
        assert fib(3) == 3

    caplog.clear()
    with Context(
        LoggingHandler(level=logging.INFO, logger=logging.getLogger())
    ) as handler:
        assert fib(0) == 1

    assert caplog.records[0].getMessage() == f"{key(fib, 0)!r} ..."
    assert caplog.records[1].getMessage() == f"{key(fib, 0)!r} = 1"

    for record in caplog.records:
        assert record.func == 'fib'        
        assert record.kwargs['x'] == '0'            