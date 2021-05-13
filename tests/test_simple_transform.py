"""Construct a simple call graph and test it's accurate."""
from typing import Any
from typing import Callable
from typing import Dict

from graphty import Context
from graphty import Handler
from graphty.typing import Decorator
from graphty.typing import Node


class TransformedHandler(Handler):
    """Store the set of calls that each call makes."""

    transforms: Dict[Callable[..., Any], Callable[..., Any]]

    def __init__(self) -> None:
        """Initialize a set of transforms."""
        self.transforms = dict()

    def __getitem__(self, key: Node) -> Any:
        """Invoke the transform function."""
        if key.func in self.transforms:
            return self.transforms[key.func__](*key[:-1])  # type: ignore
        return Ellipsis

    def __setitem__(self, key: Node, value: Any) -> None:
        """Nothing to do."""
        pass


def test_transforms(decorator: Decorator) -> None:
    """Test we can intercept a function call."""

    @decorator
    def f(x: int) -> int:
        return x

    @decorator
    def g(a: int, b: int) -> int:
        return f(a) + f(b)

    handler = TransformedHandler()
    with Context(handler):
        assert g(1, 2) == 3
        handler.transforms[f.__wrapped__] = lambda x: x + 1  # type: ignore
        assert g(1, 2) == 5
