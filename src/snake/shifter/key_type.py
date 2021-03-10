"""Build a type to represent a function signature."""
import inspect
from collections import namedtuple
from typing import Any
from typing import Callable
from typing import cast
from typing import Type

from .typing import CallKey


def _from_call(cls: Any, *args: Any, **kwargs: Any) -> CallKey:
    """Build a call key by unpacking functionc all arguments."""
    bound = cls.__signature__.bind(*args, **kwargs)
    bound.apply_defaults()
    return cast(CallKey, cls(*bound.arguments.values()))


def make_key_type(func: Callable[..., Any]) -> Type[CallKey]:
    """Construct a type representing a functions signature."""
    sig = inspect.signature(func)

    # make a format string that unpacks and names the parameters nicely
    repr_fmt = (
        (
            func.__name__
            if "<locals>" in func.__qualname__
            else func.__module__ + "." + func.__qualname__
        )
        + "("
        + ", ".join(name + "={!r}" for name in sig.parameters.keys())
        + ")"
    )

    # patch the repr so it looked pretty
    def _repr(self: Any) -> str:
        return repr_fmt.format(*self[:-1])

    key_type = type(
        func.__name__,
        (
            namedtuple(
                func.__name__,
                tuple(sig.parameters.keys()) + ("func__",),
                defaults=tuple(p.default for p in sig.parameters.values()) + (func,),
                module=func.__module__,
            ),
            CallKey,
        ),
        {
            "__repr__": _repr,
            "__func__": func,
            "__module__": func.__module__,
            "__signature__": sig,
            "from_call": classmethod(_from_call),
        },
    )

    return key_type
