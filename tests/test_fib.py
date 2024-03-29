"""Test some simple combinations of functions and handlers."""
from snake.shifter import Context
from snake.shifter import key
from snake.shifter.typing import Decorator


def test_fib(decorator: Decorator) -> None:
    """Check that caching fibonacci works."""

    @decorator
    def fib(x: int) -> int:
        if x <= 1:
            return 1
        return fib(x - 1) + fib(x - 2)

    with Context(dict()) as d:
        assert fib(0) == 1
        assert fib(1) == 1
        assert fib(2) == 2
        assert fib(3) == 3

        assert d[key(fib, 0)] == 1
        assert d[key(fib, 1)] == 1
        assert d[key(fib, 2)] == 2
        assert d[key(fib, 3)] == 3
