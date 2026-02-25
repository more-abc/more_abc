"""Type stubs for more_abc.abc_io."""

import io
from typing import Optional
from _typeshed import ReadableBuffer, WriteableBuffer

__all__ = ["AbstractRawIO", "AbstractBufferedIO", "AbstractTextIO"]


class AbstractRawIO(io.RawIOBase):
    """Abstract base class for raw binary I/O, extending io.RawIOBase."""

    def read(self, size: int = ...) -> bytes: ...
    def readinto(self, b: WriteableBuffer) -> int: ...
    def write(self, b: ReadableBuffer) -> int: ...


class AbstractBufferedIO(io.BufferedIOBase):
    """Abstract base class for buffered binary I/O, extending io.BufferedIOBase."""

    def read(self, size: Optional[int] = ...) -> bytes: ...
    def read1(self, size: int = ...) -> bytes: ...
    def write(self, b: ReadableBuffer) -> int: ...


class AbstractTextIO(io.TextIOBase):
    """Abstract base class for text I/O, extending io.TextIOBase."""

    def read(self, size: Optional[int] = ...) -> str: ...
    def readline(self, size: int = ...) -> str: ...
    def write(self, s: str) -> int: ...
