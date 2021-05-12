import logging

from collections import defaultdict
from graphty import Context
from graphty import key
from graphty.logging import LoggingHandler
from graphty.typing import Decorator


def test_compose(decorator: Decorator, caplog) -> None:
    """Compose a logger and a cache"""

    caplog.set_level(logging.INFO)

    @decorator
    def fib(x: int) -> int:
        if x <= 1:
            return 1
        return fib(x - 1) + fib(x - 2)

    caplog.clear()
    d = defaultdict(lambda: Ellipsis)
    l = LoggingHandler(level=logging.INFO, logger=logging.getLogger(""))
    with Context(l, d) as handler:
        assert fib(0) == 1

    assert caplog.records[0].getMessage() == f"{key(fib, 0)!r} ..."
    assert caplog.records[1].getMessage() == f"{key(fib, 0)!r} = 1"
    assert d[key(fib, 0)] == 1
