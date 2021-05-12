from typing import Any
from .typing import CallKey

from .handler import Handler


class NullHandler(Handler):
    """Handler that does nothing.

    Example:
        >>> handler = NullHandler()
        >>> handler[1]
        Ellipsis
    """

    def __getitem__(self, key: CallKey) -> Any:
        """We never cache any values on this handler."""
        return Ellipsis

    def __setitem__(self, key: CallKey, value: Any) -> None:
        """Never process any function results."""
        pass
