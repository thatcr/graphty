"""Base classes for core abstractions, typing."""
from typing import Any
from typing import Callable
from typing import FrozenSet
from typing import TypeVar

from typing_extensions import Protocol
from typing_extensions import runtime_checkable


@runtime_checkable
class CallKey(Protocol):
    """A class representing the call signature of a function."""

    @classmethod
    def from_call(cls, *args: Any, **kwargs: Any) -> "CallKey":
        """Generate a call signature from supplied arguments."""
        ...

    @property
    def parents(self) -> "FrozenSet[CallKey]":
        """Return the set of CallKeys that call this key."""
        ...

    @property
    def children(self) -> "FrozenSet[CallKey]":
        """Return the set of CallKeys called by this key."""
        ...

    @property
    def result(self) -> Any:
        """Return the result of the call, or raise any exception raised."""
        ...

    @property
    def exception(self) -> Exception:
        """Return any exception raised by the call, or None if there is none."""
        ...


@runtime_checkable
class CallHandler(Protocol):
    """Handler invoked from node functions when they are called."""

    def __contains__(self, key: CallKey) -> bool:
        """Check to see if we should execute the current call."""
        ...

    def __setitem__(self, key: CallKey, value: Any) -> None:
        """When executed set the returned value for the call."""
        ...

    def __getitem__(self, key: CallKey) -> Any:
        """Otherwise retrieve the value that should be returned."""
        ...


F = TypeVar("F", bound=Callable[..., Any])


@runtime_checkable
class Decorator(Protocol):
    """Protocol for transforming a function to a shifted function."""

    def __call__(self, func: F) -> F:
        """Process the supplied function so it can be shifted."""
        ...