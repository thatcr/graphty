"""Send call and return events to a python logging."""
import logging
from typing import Any

from .handler import Handler
from .typing import CallKey


class LoggingHandler(Handler):
    """Output call an return events to a logger."""

    def __init__(self, logger, level=logging.DEBUG, next=None):
        """Initialize the handler with a given logger and level."""
        super().__init__(next=next)
        self.level = level
        self.logger = logger
        self.indent = 0

    def __getitem__(self, key: CallKey) -> Any:
        """We never cache any values on this handler."""
        self.logger.log(
            self.level,
            f"{'  ' * self.indent}{key!r} ...",
            extra={"funcname": key.funcname, "kwargs": key.kwargs},
        )
        return super().__getitem__(key)

    def __setitem__(self, key: CallKey, value: Any) -> None:
        """Log the result of calling the function."""
        self.indent -= 1
        self.logger.log(
            self.level,
            f"{'  ' * self.indent}{key!r} = {value!r}",
            extra={"funcname": key.funcname, "kwargs": key.kwargs},
        )
        super().__setitem__(key, value)
