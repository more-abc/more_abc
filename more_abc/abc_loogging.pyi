"""Type stubs for more_abc.abc_loogging."""

import logging
from typing import Any, Dict

__all__ = ["AbstractLogHandler", "AbstractLogFormatter", "AbstractLogFilter"]


class AbstractLogHandler(logging.Handler):
    """Abstract base class for log handlers, extending logging.Handler."""

    _handler_config: Dict[str, Any]

    def __init__(self, level: int = ...) -> None: ...
    def configure(self, config: Dict[str, Any]) -> None: ...
    def emit(self, record: logging.LogRecord) -> None: ...
    def close(self) -> None: ...


class AbstractLogFormatter(logging.Formatter):
    """Abstract base class for log formatters, extending logging.Formatter."""

    def format(self, record: logging.LogRecord) -> str: ...


class AbstractLogFilter(logging.Filter):
    """Abstract base class for log filters, extending logging.Filter."""

    def filter(self, record: logging.LogRecord) -> bool: ...
