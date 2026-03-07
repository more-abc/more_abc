"""This submodule is an extension of the ABC functionality within the `logging` module."""

import abc
import logging
from .devtools import abc_logger

__all__ = ["AbstractLogHandler", "AbstractLogFormatter", "AbstractLogFilter"]


class AbstractLogHandler(logging.Handler, metaclass=abc.ABCMeta):
    """
    Abstract base class for log handlers, extending logging.Handler.

    All custom log handlers should subclass this to guarantee a consistent
    interface.  Subclasses must implement :meth:`configure` and :meth:`emit`.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("AbstractLogHandler subclassed: %r", cls)

    def __init__(self, level=logging.NOTSET):
        abc_logger.debug("%r.__init__(level=%r)", self.__class__.__name__, level)
        super().__init__(level=level)
        self._handler_config = {}

    @abc.abstractmethod
    def configure(self, config) -> None:
        """
        Configure the handler.
        """
        abc_logger.debug("%r.configure(config=%r) called", self.__class__.__name__, config)
        raise NotImplementedError("Subclasses must implement configure()")

    @abc.abstractmethod
    def emit(self, record):
        """
        Emit a log record.

        Overrides the core method of :class:`logging.Handler`.  Subclasses
        must implement the concrete logic for writing / dispatching the record.
        """
        abc_logger.debug("%r.emit(record=%r) called", self.__class__.__name__, record)
        raise NotImplementedError("Subclasses must implement emit()")

    def close(self):
        """Close the handler and release all held resources."""
        abc_logger.debug("%r.close() called", self.__class__.__name__)
        self.acquire()
        try:
            self._handler_config.clear()
            super().close()
        finally:
            self.release()


class AbstractLogFormatter(logging.Formatter, metaclass=abc.ABCMeta):
    """
    Abstract base class for log formatters, extending logging.Formatter.

    All custom formatters should subclass this to guarantee a consistent
    interface.  Subclasses must implement :meth:`format`.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("AbstractLogFormatter subclassed: %r", cls)

    @abc.abstractmethod
    def format(self, record):
        """
        Format a log record into a string.
        """
        abc_logger.debug("%r.format(record=%r) called", self.__class__.__name__, record)
        raise NotImplementedError("Subclasses must implement format()")


class AbstractLogFilter(logging.Filter, metaclass=abc.ABCMeta):
    """
    Abstract base class for log filters, extending logging.Filter.

    All custom filters should subclass this to guarantee a consistent
    interface.  Subclasses must implement :meth:`filter`.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("AbstractLogFilter subclassed: %r", cls)

    @abc.abstractmethod
    def filter(self, record):
        """
        Determine whether a log record should be processed.
        """
        abc_logger.debug("%r.filter(record=%r) called", self.__class__.__name__, record)
        raise NotImplementedError("Subclasses must implement filter()")
