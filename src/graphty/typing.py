"""Base classes for core abstractions, typing."""
from typing import Any
from typing import Callable
from typing import FrozenSet
from typing import Mapping
from typing import TypeVar

from typing_extensions import Protocol
from typing_extensions import runtime_checkable


@runtime_checkable
class Node(Protocol):
    """A class representing the call signature of a function."""

    @classmethod
    def from_call(cls, *args: Any, **kwargs: Any) -> "Node":
        """Generate a call signature from supplied arguments."""
        ...

    @property
    def parents(self) -> "FrozenSet[Node]":
        """Return the set of CallKeys that call this key."""
        ...

    @property
    def children(self) -> "FrozenSet[Node]":
        """Return the set of CallKeys called by this key."""
        ...

    @property
    def result(self) -> Any:
        """Return the result of the call, or raise any exception raised."""
        ...

    @property
    def exception(self) -> Exception:
        """Return any exception raised by the call, or None if there is none."""

    @property
    def kwargs(self) -> Mapping[str, str]:
        """Return a string formatted dict of the call arguments."""

    @property
    def funcname(self) -> str:
        """Return a string name for the function."""

    @property
    def func(self) -> Callable[..., Any]:
        """Return the function object for this CallKey."""


F = TypeVar("F", bound=Callable[..., Any])


@runtime_checkable
class Decorator(Protocol):
    """Protocol for transforming a function to a shifted function."""

    def __call__(self, func: F) -> F:
        """Process the supplied function so it can be shifted."""
        ...
