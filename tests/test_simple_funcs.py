"""Test some simple combinations of functions and handlers."""
from collections import defaultdict
from unittest.mock import MagicMock

import pytest

from graphty import Context
from graphty import node
from graphty.typing import Decorator


def test_simple_func(
    decorator: Decorator,
) -> None:
    """Check we can construct a key, and cache in a dict."""

    @decorator
    def f(a: int, b: int) -> int:
        return a + b

    with Context(defaultdict(lambda: Ellipsis)) as d:
        f(1, 2)
        f(1, 2)

    assert d[node(f, 1, 2)] == 3


def test_simple_failing_func(decorator: Decorator) -> None:
    """Check we can construct a key, and cache in a dict."""
    # store a ref to the thrown exception outside the function
    # so we can check it's the same one returned
    exception = None

    @decorator
    def f(a: int, b: int) -> int:
        nonlocal exception
        # this exception should be cached by the wrapper
        # so we only see it once
        exception = RuntimeError("failure")

        raise exception

    with Context(defaultdict(lambda: Ellipsis)) as d:
        # check we get the exception as thrown from the function above
        try:
            f(1, 2)
        except RuntimeError as e:
            assert e is exception
            assert e.__traceback__.tb_frame.f_code.co_filename == __file__

        # check it again, to check that the cached exception gets
        # the right traceback
        try:
            f(1, 2)
        except RuntimeError as e:
            assert e is exception
            assert e.__traceback__.tb_frame.f_code.co_filename == __file__

    assert type(d[node(f, 1, 2)]) is Exception
    assert d[node(f, 1, 2)].args[0] is exception


def test_mock_null_handler(decorator: Decorator) -> None:
    """Check that a null mock handler is called correctly."""
    handler = MagicMock()
    handler.__getitem__.return_value = Ellipsis
    handler.__setitem__.return_value = None

    @decorator
    def f(a: int, b: int) -> int:
        return a + b

    with Context(handler):
        assert f(1, 2) == 3

    handler.__getitem__.assert_called_once_with(node(f, 1, 2))
    handler.__setitem__.assert_called_once_with(node(f, 1, 2), 3)


def test_mock_cached_handler(decorator: Decorator) -> None:
    """Check that a fixed value mock handler is called correctly."""
    return_value = -1
    handler = MagicMock()
    handler.__getitem__.return_value = return_value
    handler.__setitem__.return_value = None

    @decorator
    def f(a: int, b: int) -> int:
        raise AssertionError("this function should not be called")

    with pytest.raises(AssertionError):
        f(1, 2)

    with Context(handler):
        assert f(1, 2) is return_value

    handler.__getitem__.assert_called_once_with(node(f, 1, 2))
    handler.__setitem__.assert_not_called()
