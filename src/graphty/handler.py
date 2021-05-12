from typing import Any
from .typing import CallKey


class Handler:
    def __init__(self, next=None):
        self.next = next

    def __setitem__(self, key: CallKey, value: Any) -> None:
        """When executed set the returned value for the call."""
        if self.next is not None:
            self.next[key] = value

    def __getitem__(self, key: CallKey) -> Any:
        """Otherwise retrieve the value that should be returned."""
        if self.next is not None:
            return self.next[key]
        return Ellipsis
