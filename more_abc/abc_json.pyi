"""Type stubs for more_abc.abc_json."""

import json
from abc import abstractmethod
from typing import Any, Iterator

__all__ = [
    "AbstractJSONEncoder",
    "AbstractJSONDecoder",
]


class AbstractJSONEncoder(json.JSONEncoder):
    """Abstract base class for JSON encoders, extending
    :class:`json.JSONEncoder`.

    Subclasses must implement :meth:`default`, :meth:`encode`,
    and :meth:`iterencode`.
    """

    @abstractmethod
    def default(self, o: Any) -> Any:
        """Return a serializable object for *o*."""
        ...

    @abstractmethod
    def encode(self, o: Any) -> str:
        """Return a JSON string representation of *o*."""
        ...

    @abstractmethod
    def iterencode(self, o: Any, _one_shot: bool = False) -> Iterator[str]:
        """Encode *o* and yield each string chunk as available."""
        ...


class AbstractJSONDecoder(json.JSONDecoder):
    """Abstract base class for JSON decoders, extending
    :class:`json.JSONDecoder`.

    Subclasses must implement :meth:`decode` and :meth:`raw_decode`.
    """

    @abstractmethod
    def decode(self, s: str) -> Any:  # type: ignore[override]
        """Return the Python representation of *s*."""
        ...

    @abstractmethod
    def raw_decode(self, s: str, idx: int = 0) -> tuple[Any, int]:
        """Decode a JSON document from *s* starting at index *idx*."""
        ...
