"""Type stubs for more_abc.collections_abc."""

from abc import ABCMeta, abstractmethod
from typing import Any, Callable, TypeVar

__all__ = [
    "BaseSortable", "SortableMixin", "Sortable",
    "BaseFilterable", "FilterableMixin", "Filterable",
    "BaseTransformable", "TransformableMixin", "Transformable",
]

_SelfSortable = TypeVar("_SelfSortable", bound="SortableMixin")
_SelfFilterable = TypeVar("_SelfFilterable", bound="FilterableMixin")
_SelfTransformable = TypeVar("_SelfTransformable", bound="TransformableMixin")


class BaseSortable(metaclass=ABCMeta):
    """Minimal abstract interface for sortable containers."""

    @abstractmethod
    def __sort__(self, reverse: bool = False) -> None:
        """Sort the container in-place."""
        ...


class SortableMixin:
    """Concrete :meth:`sort` / :meth:`sorted` helpers built on
    :meth:`__sort__`."""

    def sort(self, reverse: bool = False) -> None:
        """Sort the container in-place."""
        ...

    def sorted(
        self: _SelfSortable,
        reverse: bool = False,
    ) -> _SelfSortable:
        """Return a new sorted container of the same type."""
        ...

    @abstractmethod
    def __copy__(self: _SelfSortable) -> _SelfSortable:
        """Return a shallow copy of the container."""
        ...


class Sortable(BaseSortable, SortableMixin):
    """Final exposed ABC for sortable containers."""

    @classmethod
    def __subclasshook__(cls, C: type) -> bool: ...


class BaseFilterable(metaclass=ABCMeta):
    """Minimal abstract interface for filterable containers."""

    @abstractmethod
    def __filter__(
        self: _SelfFilterable, # type: ignore
        predicate: Callable[[Any], bool],
    ) -> _SelfFilterable:
        """Return a new container keeping only elements where
        ``predicate(elem)`` is ``True``."""
        ...


class FilterableMixin:
    """Concrete :meth:`filter` / :meth:`reject` helpers built on
    :meth:`__filter__`."""

    def filter(
        self: _SelfFilterable,
        predicate: Callable[[Any], bool],
    ) -> _SelfFilterable:
        """Return a new container with elements satisfying *predicate*."""
        ...

    def reject(
        self: _SelfFilterable,
        predicate: Callable[[Any], bool],
    ) -> _SelfFilterable:
        """Return a new container with elements *not* satisfying
        *predicate*."""
        ...


class Filterable(BaseFilterable, FilterableMixin):
    """Final exposed ABC for filterable containers."""

    @classmethod
    def __subclasshook__(cls, C: type) -> bool: ...


class BaseTransformable(metaclass=ABCMeta):
    """Minimal abstract interface for transformable containers."""

    @abstractmethod
    def __transform__(
        self: _SelfTransformable, # type: ignore
        func: Callable[[Any], Any],
    ) -> _SelfTransformable:
        """Return a new container with *func* applied to every element."""
        ...


class TransformableMixin:
    """Concrete :meth:`map` helper built on :meth:`__transform__`."""

    def map(
        self: _SelfTransformable,
        func: Callable[[Any], Any],
    ) -> _SelfTransformable:
        """Return a new container with *func* applied to every element."""
        ...


class Transformable(BaseTransformable, TransformableMixin):
    """Final exposed ABC for transformable containers."""

    @classmethod
    def __subclasshook__(cls, C: type) -> bool: ...
