"""Type stubs for more_abc.abc_loogging."""

import logging
from abc import abstractmethod
from typing import Any

__all__ = ["AbstractLogHandler", "AbstractLogFormatter", "AbstractLogFilter"]


class AbstractLogHandler(logging.Handler):
    """Abstract base class for log handlers, extending
    :class:`logging.Handler`.

    Subclasses must implement :meth:`configure` and :meth:`emit`.
    """

    _handler_config: dict[str, Any]

    def __init__(self, level: int = logging.NOTSET) -> None: ...

    @abstractmethod
    def configure(self, config: Any) -> None:
        """Configure the handler."""
        ...

    @abstractmethod
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record."""
        ...

    def close(self) -> None: ...


class AbstractLogFormatter(logging.Formatter):
    """Abstract base class for log formatters, extending
    :class:`logging.Formatter`.

    Subclasses must implement :meth:`format`.
    """

    @abstractmethod
    def format(self, record: logging.LogRecord) -> str:
        """Format a log record into a string."""
        ...


class AbstractLogFilter(logging.Filter):
    """Abstract base class for log filters, extending
    :class:`logging.Filter`.

    Subclasses must implement :meth:`filter`.
    """

    @abstractmethod
    def filter(self, record: logging.LogRecord) -> bool:
        """Determine whether a log record should be processed."""
        ...
