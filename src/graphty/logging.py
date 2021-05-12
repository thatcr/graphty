import logging
from typing import Any

from .typing import CallHandler
from .typing import CallKey


class LoggingHandler(object):
    def __init__(self, logger, level=logging.DEBUG):
        self.level = level
        self.logger = logger
        self.indent = 0

    def __contains__(self, key: CallKey) -> bool:
        """Avoid handling anything."""
        self.logger.log(
            self.level, f"{'  ' * self.indent}{key!r} ...",          
            extra={"func" : key.func, "kwargs" : key.kwargs}
        )
        self.indent += 1
        return False

    def __getitem__(self, key: CallKey) -> Any:
        """We never cache any values on this handler."""
        # we don't know the value to log, unless we pass through
        
        # how do we nest calls here?
        raise NotImplementedError()

    def __setitem__(self, key: CallKey, value: Any) -> None:
        """Log the result of calling the function"""
        self.indent -= 1
        self.logger.log(
            self.level,
            f"{'  ' * self.indent}{key!r} = {value!r}",
            extra={"func" : key.func, "kwargs" : key.kwargs}
        )
        pass
