"""Construct a simple call graph and test it's accurate."""
from typing import Any
from typing import Callable
from typing import Dict

from snake.shifter import Context
from snake.shifter.typing import CallKey
from snake.shifter.typing import Decorator


class TransformedCallHandler:
    """Store the set of calls that each call makes."""

    transforms: Dict[Callable[..., Any], Callable[..., Any]]

    def __init__(self) -> None:
        """Initialize a set of transforms."""
        self.transforms = dict()

    def __contains__(self, key: CallKey) -> bool:
        """Override the call if we have a transform."""
        return key.func__ in self.transforms  # type: ignore

    def __getitem__(self, key: CallKey) -> Any:
        """Invoke the transform function."""
        return self.transforms[key.func__](*key[:-1])  # type: ignore

    def __setitem__(self, key: CallKey, value: Any) -> None:
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

    handler = TransformedCallHandler()
    with Context(handler):
        assert g(1, 2) == 3
        handler.transforms[f.__wrapped__] = lambda x: x + 1  # type: ignore
        assert g(1, 2) == 5
