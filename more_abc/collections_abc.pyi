# """Type stubs for `more_abc.collections_abc``."""

# The original docstring got overwritten by this thing.

from abc import ABCMeta
from typing import Any, Callable, TypeVar

__all__ = [
    "BaseSortable", "SortableMixin", "Sortable",
    "BaseFilterable", "FilterableMixin", "Filterable",
    "BaseTransformable", "TransformableMixin", "Transformable",
]

_T = TypeVar("_T")


class BaseSortable(metaclass=ABCMeta):
    """Minimal abstract interface for sortable containers."""
    def __sort__(self, reverse: bool = ...) -> None: ...


class SortableMixin:
    """Concrete sort()/sorted() helpers built on __sort__."""
    def sort(self, reverse: bool = ...) -> None: ...
    def sorted(self, reverse: bool = ...) -> "SortableMixin": ...
    def __copy__(self) -> "SortableMixin": ...


class Sortable(BaseSortable, SortableMixin):
    """Final ABC for sortable containers."""
    @classmethod
    def __subclasshook__(cls, C: type) -> bool: ...


class BaseFilterable(metaclass=ABCMeta):
    """Minimal abstract interface for filterable containers."""
    def __filter__(self, predicate: Callable[[Any], bool]) -> "BaseFilterable": ...


class FilterableMixin:
    """Concrete filter()/reject() helpers built on __filter__."""
    def filter(self, predicate: Callable[[Any], bool]) -> "FilterableMixin": ...
    def reject(self, predicate: Callable[[Any], bool]) -> "FilterableMixin": ...


class Filterable(BaseFilterable, FilterableMixin):
    """Final ABC for filterable containers."""
    @classmethod
    def __subclasshook__(cls, C: type) -> bool: ...


class BaseTransformable(metaclass=ABCMeta):
    """Minimal abstract interface for transformable containers."""
    def __transform__(self, func: Callable[[Any], Any]) -> "BaseTransformable": ...


class TransformableMixin:
    """Concrete map() helper built on __transform__."""
    def map(self, func: Callable[[Any], Any]) -> "TransformableMixin": ...


class Transformable(BaseTransformable, TransformableMixin):
    """Final ABC for transformable containers."""
    @classmethod
    def __subclasshook__(cls, C: type) -> bool: ...