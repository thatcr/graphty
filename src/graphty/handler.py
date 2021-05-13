"""Base implementation for handling graphty events."""
from typing import Any

from .typing import Node


class Handler:
    """Base class for all graphty event handlers.

    This class exposes the basic dict protocol for getitem and setitem
    which graphty hooks into functions to allow the handler to intercept
    calls and the results.
    """

    def __init__(self, next=None):
        """Configure the handler, with the given underlying handler to pass through."""
        self.next = next

    def __setitem__(self, key: Node, value: Any) -> None:
        """When executed set the returned value for the call."""
        if self.next is not None:
            self.next[key] = value

    def __getitem__(self, key: Node) -> Any:
        """Otherwise retrieve the value that should be returned."""
        if self.next is not None:
            return self.next[key]
        return Ellipsis
