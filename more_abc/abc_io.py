"""This submodule is an extension of the ABC functionality within the `io` module."""

import abc
import io

__all__ = [
    "AbstractRawIO",
    "AbstractBufferedIO",
    "AbstractTextIO",
]


class AbstractRawIO(io.RawIOBase, metaclass=abc.ABCMeta):
    """Abstract base class for raw binary I/O, extending io.RawIOBase.

    All custom raw I/O implementations should subclass this to guarantee a
    consistent interface.  Subclasses must implement :meth:`read`,
    :meth:`readinto`, and :meth:`write`.
    """

    @abc.abstractmethod
    def read(self, size=-1):
        """
        Read and return up to *size* bytes.
        """
        raise NotImplementedError("Subclasses must implement read()")

    @abc.abstractmethod
    def readinto(self, b):
        """
        Read bytes into a pre-allocated buffer *b*.
        """
        raise NotImplementedError("Subclasses must implement readinto()")

    @abc.abstractmethod
    def write(self, b):
        """
        Write bytes *b* to the stream.
        """
        raise NotImplementedError("Subclasses must implement write()")


class AbstractBufferedIO(io.BufferedIOBase, metaclass=abc.ABCMeta):
    """
    Abstract base class for buffered binary I/O, extending io.BufferedIOBase.

    All custom buffered I/O implementations should subclass this to guarantee
    a consistent interface.  Subclasses must implement :meth:`read`,
    :meth:`read1`, and :meth:`write`.
    """

    @abc.abstractmethod
    def read(self, size=None):
        """
        Read and return up to *size* bytes.
        """
        raise NotImplementedError("Subclasses must implement read()")

    @abc.abstractmethod
    def read1(self, size=-1):
        """
        Read and return up to *size* bytes with at most one raw read call.
        """
        raise NotImplementedError("Subclasses must implement read1()")

    @abc.abstractmethod
    def write(self, b):
        """
        Write bytes *b* to the stream.
        """
        raise NotImplementedError("Subclasses must implement write()")


class AbstractTextIO(io.TextIOBase, metaclass=abc.ABCMeta):
    """
    Abstract base class for text I/O, extending io.TextIOBase.

    All custom text I/O implementations should subclass this to guarantee a
    consistent interface.  Subclasses must implement :meth:`read`,
    :meth:`readline`, and :meth:`write`.
    """

    @abc.abstractmethod
    def read(self, size=None):
        """
        Read and return at most *size* characters.
        """
        raise NotImplementedError("Subclasses must implement read()")

    @abc.abstractmethod
    def readline(self, size=-1):
        """
        Read until newline or EOF and return a single line.
        """
        raise NotImplementedError("Subclasses must implement readline()")

    @abc.abstractmethod
    def write(self, s):
        """
        Write string *s* to the stream.
        """
        raise NotImplementedError("Subclasses must implement write()")
