"""Implementation of call tracker using a function wrapper via a decorator.

This a reference implementation to make it clear how the
handler interacts with the function and to provide a
benchmark implementation to test the other approaches against.
"""
import functools
from typing import Any
from typing import Callable
from typing import cast
from typing import TypeVar

from .key_type import make_key_type

F = TypeVar("F", bound=Callable[..., Any])


def shift(func: F) -> F:
    """Wrap a function with calls to a handler to modify it's behaviour.

    Args:
        func: the function to modify

    Returns:
        the modified function
    """
    key_type = make_key_type(func)

    # import the global context handler stack here, which we bind into the wrapper
    from .context import Context

    @functools.wraps(func)
    def _func(*args: Any, **kwargs: Any) -> Any:
        handler = Context._handlers[-1]

        key = key_type.from_call(*args, **kwargs)

        if key in handler:
            value = handler[key]
            if type(value) is Exception:
                raise value.args[0] from value.args[0]

            return value
        try:
            retval = func(*args, **kwargs)
            handler[key] = retval
            return retval
        except Exception as exc:
            handler[key] = Exception(exc)
            raise

    _func.__key__ = key_type  # type: ignore

    return cast(F, _func)
