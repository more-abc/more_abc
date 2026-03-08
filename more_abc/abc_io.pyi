"""Type stubs for more_abc.abc_io."""

import io
from abc import abstractmethod
from _typeshed import ReadableBuffer, WriteableBuffer

__all__ = ["AbstractRawIO", "AbstractBufferedIO", "AbstractTextIO"]


class AbstractRawIO(io.RawIOBase):
    """Abstract base class for raw binary I/O, extending
    :class:`io.RawIOBase`.

    Subclasses must implement :meth:`read`, :meth:`readinto`,
    and :meth:`write`.
    """

    @abstractmethod
    def read(self, size: int = -1) -> bytes:
        """Read and return up to *size* bytes."""
        ...

    @abstractmethod
    def readinto(self, b: WriteableBuffer) -> int:
        """Read bytes into a pre-allocated buffer *b*."""
        ...

    @abstractmethod
    def write(self, b: ReadableBuffer) -> int:
        """Write bytes *b* to the stream."""
        ...


class AbstractBufferedIO(io.BufferedIOBase):
    """Abstract base class for buffered binary I/O, extending
    :class:`io.BufferedIOBase`.

    Subclasses must implement :meth:`read`, :meth:`read1`,
    and :meth:`write`.
    """

    @abstractmethod
    def read(self, size: int | None = None) -> bytes:
        """Read and return up to *size* bytes."""
        ...

    @abstractmethod
    def read1(self, size: int = -1) -> bytes:
        """Read up to *size* bytes with at most one raw read call."""
        ...

    @abstractmethod
    def write(self, b: ReadableBuffer) -> int:
        """Write bytes *b* to the stream."""
        ...


class AbstractTextIO(io.TextIOBase):
    """Abstract base class for text I/O, extending :class:`io.TextIOBase`.

    Subclasses must implement :meth:`read`, :meth:`readline`,
    and :meth:`write`.
    """

    @abstractmethod
    def read(self, size: int | None = None) -> str:
        """Read and return at most *size* characters."""
        ...

    @abstractmethod
    def readline(self, size: int = -1) -> str:
        """Read until newline or EOF and return a single line."""
        ...

    @abstractmethod
    def write(self, s: str) -> int:
        """Write string *s* to the stream."""
        ...
