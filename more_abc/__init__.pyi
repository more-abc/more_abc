# """Type stubs for more_abc (package root)."""

from abc import (
    ABC as ABC,
    ABCMeta as ABCMeta,
    abstractmethod as abstractmethod,
    get_cache_token as get_cache_token,
    update_abstractmethods as update_abstractmethods,
)
from typing import Any, Callable, TypeVar

from .more import (
    ABCMixin as ABCMixin,
    ABCclassType as ABCclassType,
    ABCMetaclassType as ABCMetaclassType,
    ABCException as ABCException,
    ABCWarning as ABCWarning,
)
from .decorator import (
    abstract_class as abstract_class,
    abstractproperty as abstractproperty,
    abstract_lru_cache as abstract_lru_cache,
)
from .abc_dataclasses import abstractdataclass as abstractdataclass
from .abc_enum import (
    ABCEnumMeta as ABCEnumMeta,
    ABCEnum as ABCEnum,
    ABCIntEnum as ABCIntEnum,
    ABCFlag as ABCFlag,
    ABCIntFlag as ABCIntFlag,
)
from .abc_loogging import (
    AbstractLogFilter as AbstractLogFilter,
    AbstractLogFormatter as AbstractLogFormatter,
    AbstractLogHandler as AbstractLogHandler,
)
from .abc_io import (
    AbstractBufferedIO as AbstractBufferedIO,
    AbstractRawIO as AbstractRawIO,
    AbstractTextIO as AbstractTextIO,
)
from .abc_json import (
    AbstractJSONDecoder as AbstractJSONDecoder,
    AbstractJSONEncoder as AbstractJSONEncoder,
)
from .collections_abc import (
    BaseSortable as BaseSortable,
    SortableMixin as SortableMixin,
    Sortable as Sortable,
    BaseFilterable as BaseFilterable,
    FilterableMixin as FilterableMixin,
    Filterable as Filterable,
    BaseTransformable as BaseTransformable,
    TransformableMixin as TransformableMixin,
    Transformable as Transformable,
)
from . import _devtools as _devtools
from ._devtools import abc_logger as abc_logger

__all__: list[str]

__version__: str
__version_tuple__: tuple[int, int, int]
__int_version__: int
__author__: str
__license__: str
__status__: str
__title__: str
__description__: str

DevMode: bool
# """Development mode toggle switch."""

# ---------------------------------------------------------------------------
# abstractasyncmethod — defined in __init__.py for all Python versions
# ---------------------------------------------------------------------------

_F = TypeVar("_F", bound=Callable[..., Any])

def abstractasyncmethod(func: _F) -> _F: ...
