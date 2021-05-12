import logging

from collections import defaultdict
from graphty import Context
from graphty import key
from graphty.logging import LoggingHandler
from graphty.typing import Decorator



# do we have filters and handlers, like logging?
# or shoud we collapse the wrapper to using just get/set to make ti easier.
# make Ellipsis the sentinel for the call.

# a logging filter could pick ip the node trace (and context)...
# chain of command must always be nested?


def test_compose(decorator: Decorator, caplog) -> None:
    """Compose a logger and a cache"""

    @decorator
    def fib(x: int) -> int:
        if x <= 1:
            return 1
        return fib(x - 1) + fib(x - 2)

    caplog.clear()
    d = defaultdict(Ellipsis)
    l = LoggingHandler(level=logging.INFO, logger=logging.getLogger(""))
    with Context(l, d):
        assert fib(0) == 1

    assert caplog.records[0].getMessage() == f"{key(fib, 0)!r} ..."
    assert caplog.records[1].getMessage() == f"{key(fib, 0)!r} = 1"
    assert d[key(fib, 0)] == 1
