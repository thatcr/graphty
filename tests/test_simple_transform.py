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
        return key.func__ in self.transforms

    def __getitem__(self, key: CallKey) -> Any:
        """Invoke the transform function."""
        # call the transform
        print(key)
        return self.transforms[key.func__](*key[:-1])

    def __setitem__(self, key: CallKey, value: Any) -> None:
        """Nothing to do."""
        pass


def test_transforms(decorator: Decorator):
    """Test we can intercept a function call."""

    @decorator
    def f(x):
        return x

    @decorator
    def g(a, b):
        return f(a) + f(b)

    with Context(TransformedCallHandler()):
        assert g(1, 2) == 3

    with Context(TransformedCallHandler()) as handler:
        handler.transforms[f.__wrapped__] = lambda x: x + 1

        assert g(1, 2) == 5
