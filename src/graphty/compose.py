# unless the getitem is nested, we can't process the result nicely.
# remember the multi-layer cache case, where we have bigger objects on disk.

from typing import Any
from .typing import CallKey


class CompositeHandler:
    """Handler that composes multiple handlers."""

    def __init__(self, handlers):
        self.handlers = handlers

    def __getitem__(self, key: CallKey) -> Any:
        """We never cache any values on this handler."""
        for handler in self.handlers:
            result = handler[key]
            if result is not Ellipsis:
                return result

        return Ellipsis

    def __setitem__(self, key: CallKey, value: Any) -> None:
        for handler in self.handlers:
            handler[key] = value


# make a better combinator for this?