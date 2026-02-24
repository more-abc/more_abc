"""This submodule is an extension of the ABC functionality within the `logging` module."""

import abc
import logging

__all__ = ["AbstractLogHandler", "AbstractLogFormatter", "AbstractLogFilter"]


class AbstractLogHandler(logging.Handler, metaclass=abc.ABCMeta):
    """Abstract base class for log handlers, extending logging.Handler.

    All custom log handlers should subclass this to guarantee a consistent
    interface.  Subclasses must implement :meth:`configure` and :meth:`emit`.
    """

    def __init__(self, level=logging.NOTSET):
        super().__init__(level=level)
        self._handler_config = {}

    @abc.abstractmethod
    def configure(self, config) -> None:
        """Configure the handler.

        Args:
            config: A mapping of configuration options (e.g. output path,
                    format string, log-level threshold).
        """
        raise NotImplementedError("Subclasses must implement configure()")

    @abc.abstractmethod
    def emit(self, record):
        """Emit a log record.

        Overrides the core method of :class:`logging.Handler`.  Subclasses
        must implement the concrete logic for writing / dispatching the record.

        Args:
            record: The log record to handle.
        """
        raise NotImplementedError("Subclasses must implement emit()")

    def close(self):
        """Close the handler and release all held resources."""
        self.acquire()
        try:
            self._handler_config.clear()
            super().close()
        finally:
            self.release()


class AbstractLogFormatter(logging.Formatter, metaclass=abc.ABCMeta):
    """Abstract base class for log formatters, extending logging.Formatter.

    All custom formatters should subclass this to guarantee a consistent
    interface.  Subclasses must implement :meth:`format`.
    """

    @abc.abstractmethod
    def format(self, record):
        """Format a log record into a string.

        Args:
            record: The log record to format.

        Returns:
            The formatted log string.
        """
        raise NotImplementedError("Subclasses must implement format()")


class AbstractLogFilter(logging.Filter, metaclass=abc.ABCMeta):
    """Abstract base class for log filters, extending logging.Filter.

    All custom filters should subclass this to guarantee a consistent
    interface.  Subclasses must implement :meth:`filter`.
    """

    @abc.abstractmethod
    def filter(self, record):
        """Determine whether a log record should be processed.

        Args:
            record: The log record to evaluate.

        Returns:
            True to allow the record through; False to discard it.
        """
        raise NotImplementedError("Subclasses must implement filter()")
