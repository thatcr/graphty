from typing import Any
from .typing import CallKey


# code issue it that the dict-based API doesn't wrap the function call
# so doesn't have policy over what's actually executed.

# unless we layer the


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
