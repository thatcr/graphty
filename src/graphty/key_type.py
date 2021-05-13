"""Build a type to represent a function signature."""
import inspect
from collections import namedtuple
from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import FrozenSet
from typing import Type

from .context import get_handler
from .typing import CallKey


def _from_call(cls: Any, *args: Any, **kwargs: Any) -> CallKey:
    """Build a call key by unpacking functionc all arguments."""
    bound = cls.__signature__.bind(*args, **kwargs)
    bound.apply_defaults()
    return cast(CallKey, cls(*bound.arguments.values()))


class CallKeyImpl(object):
    """Default implementation of call key methods that redirect to the handler."""

    def __repr__(self: Any) -> str:
        """Make a human readable string from the key"""
        return self.__repr_fmt__.format(*self[:-1])

    @property
    def parents(self) -> FrozenSet[CallKey]:
        """Return the set of CallKeys that call this key."""
        return get_handler().parents[self]

    @property
    def children(self) -> FrozenSet[CallKey]:
        """Return the set of CallKeys called by this key."""
        return get_handler().children[self]

    @property
    def result(self) -> Any:
        """Return the result of the call, or raise any exception raised."""
        retval = get_handler().retvals[self]
        if isinstance(retval, Exception):
            raise retval.args[0]
        return retval

    @property
    def exception(self) -> Exception:
        """Return any exception raised by the call, or None if there is none."""
        retval = get_handler().retvals[self]
        if isinstance(retval, Exception):
            return retval.args[0]
        return None

    @property
    def func(self):
        return (
            self.func__.__name__
            if "<locals>" in self.func__.__qualname__
            else self.func__.__module__ + "." + self.func__.__qualname__
        )

    @property
    def kwargs(self):
        return {self._fields[i]: repr(self[i]) for i in range(0, len(self) - 1)}


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

    key_type = type(
        func.__name__,
        (
            CallKey,
            CallKeyImpl,
            namedtuple(
                func.__name__,
                tuple(sig.parameters.keys()) + ("func__",),
                defaults=tuple(p.default for p in sig.parameters.values()) + (func,),
                module=func.__module__,
            ),
        ),
        {
            "__repr_fmt__": repr_fmt,
            "__func__": func,
            "__module__": func.__module__,
            "__signature__": sig,
            "from_call": classmethod(_from_call),
            **CallKeyImpl.__dict__,
        },
    )

    return key_type
