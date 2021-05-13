"""Grafty."""
from typing import Any
from typing import Callable

from .context import Context
from .context import get_handler
from .handler import Handler
from .typing import Node
from .wrapper import shift


def node(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Node:
    """Construct a key to a function call with the given arguments."""
    # since we are preserving fundamental python types as far as possible
    # we disable type checking here, __key__ is an implementation detail.
    return func.__key__.from_call(*args, **kwargs)  # type: ignore


__all__ = ["Context", "Handler", "node", "shift", "get_handler"]
