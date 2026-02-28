# """Type stubs for `more_abc.abc_json`."""

import json
from typing import Any, Iterator

__all__ = [
    "AbstractJSONEncoder",
    "AbstractJSONDecoder",
]


class AbstractJSONEncoder(json.JSONEncoder):
    # """Abstract base class for JSON encoders, extending json.JSONEncoder."""

    def default(self, o: Any) -> Any: ...
    def encode(self, o: Any) -> str: ...
    def iterencode(self, o: Any, _one_shot: bool = ...) -> Iterator[str]: ...


class AbstractJSONDecoder(json.JSONDecoder):
    # """Abstract base class for JSON decoders, extending json.JSONDecoder."""

    def decode(self, s: str, _w: Any = ...) -> Any: ...
    def raw_decode(self, s: str, idx: int = ...) -> tuple[Any, int]: ...
