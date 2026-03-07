"""
Abstract Base Classes (ABCs) for collections, according to PEP 3119.
This submodule is an extension of the ABC functionality within the `collections.abc` module.
"""

import abc
from .devtools import abc_logger

__all__ = [
    "BaseSortable", "SortableMixin", "Sortable",
    "BaseFilterable", "FilterableMixin", "Filterable",
    "BaseTransformable", "TransformableMixin", "Transformable",
]

class BaseSortable(metaclass=abc.ABCMeta):
    """
    Minimal interface for sortable containers (similar to `collections.abc.BaseIterable`),
    Only defines core abstract methods with no concrete implementations whatsoever
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("BaseSortable subclassed: %r", cls)

    @abc.abstractmethod
    def __sort__(self, reverse=False):
        """
        Core abstract methods (in the style of magic methods, consistent with `__iter__`/`__getitem__`)
        Requires subclasses to implement sorting logic and modify the container itself
        """
        abc_logger.debug("%r.__sort__(reverse=%r) called", self.__class__.__name__, reverse)
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement __sort__()"
        )

class SortableMixin:
    """
    Sorting Mixin (containing only general-purpose methods, no abstract methods)
    Implements common sorting-related methods based on `__sort__`
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("SortableMixin subclassed: %r", cls)

    def sort(self, reverse=False):
        """User-friendly methods exposed externally"""
        abc_logger.debug("%r.sort(reverse=%r) called", self.__class__.__name__, reverse)
        self.__sort__(reverse=reverse) # type: ignore

    def sorted(self, reverse=False):
        """Returns a new sorted container"""
        abc_logger.debug("%r.sorted(reverse=%r) called", self.__class__.__name__, reverse)
        new_container = self.__copy__()
        new_container.sort(reverse=reverse)
        return new_container

    @abc.abstractmethod
    def __copy__(self):
        """A Mixin may also declare abstract methods and require subclasses to implement them."""
        abc_logger.debug("%r.__copy__() called", self.__class__.__name__)
        raise NotImplementedError

class Sortable(BaseSortable, SortableMixin):
    """
    Final exposed ABC for sortable containers
    Inherits the minimal interface + Mixin, featuring both mandatory constraints and general-purpose methods
    """

    @classmethod
    def __subclasshook__(cls, C):
        abc_logger.debug("Sortable.__subclasshook__(%r)", C)
        if cls is Sortable:
            if any("__sort__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


class BaseFilterable(metaclass=abc.ABCMeta):
    """
    Minimal interface for containers that support predicate-based filtering.

    Only defines the core abstract method with no concrete implementations.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("BaseFilterable subclassed: %r", cls)

    @abc.abstractmethod
    def __filter__(self, predicate):
        """
        Return a new container keeping only elements for which predicate(elem) is True.
        """
        abc_logger.debug("%r.__filter__(predicate=%r) called", self.__class__.__name__, predicate)
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement __filter__()"
        )


class FilterableMixin:
    """Filtering mixin with concrete helpers built on top of `__filter__`.

    Contains only general-purpose methods; no abstract methods of its own.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("FilterableMixin subclassed: %r", cls)

    def filter(self, predicate):
        """Return a new container with elements satisfying predicate."""
        abc_logger.debug("%r.filter(predicate=%r) called", self.__class__.__name__, predicate)
        return self.__filter__(predicate)  # type: ignore

    def reject(self, predicate):
        """Return a new container with elements *not* satisfying predicate."""
        abc_logger.debug("%r.reject(predicate=%r) called", self.__class__.__name__, predicate)
        return self.__filter__(lambda x: not predicate(x))  # type: ignore


class Filterable(BaseFilterable, FilterableMixin):
    """Final exposed ABC for filterable containers.

    Combines the minimal interface and the mixin, providing both mandatory
    constraints and general-purpose helpers.
    """

    @classmethod
    def __subclasshook__(cls, C):
        abc_logger.debug("Filterable.__subclasshook__(%r)", C)
        if cls is Filterable:
            if any("__filter__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


class BaseTransformable(metaclass=abc.ABCMeta):
    """
    Minimal interface for containers that support element-wise transformation.

    Only defines the core abstract method with no concrete implementations.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("BaseTransformable subclassed: %r", cls)

    @abc.abstractmethod
    def __transform__(self, func):
        """
        Return a new container with func applied to every element.
        """
        abc_logger.debug("%r.__transform__(func=%r) called", self.__class__.__name__, func)
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement __transform__()"
        )


class TransformableMixin:
    """Transformation mixin with concrete helpers built on top of `__transform__`.

    Contains only general-purpose methods; no abstract methods of its own.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("TransformableMixin subclassed: %r", cls)

    def map(self, func):
        """Return a new container with func applied to every element."""
        abc_logger.debug("%r.map(func=%r) called", self.__class__.__name__, func)
        return self.__transform__(func)  # type: ignore


class Transformable(BaseTransformable, TransformableMixin):
    """
    Final exposed ABC for transformable containers.

    Combines the minimal interface and the mixin, providing both mandatory
    constraints and general-purpose helpers.
    """

    @classmethod
    def __subclasshook__(cls, C):
        abc_logger.debug("Transformable.__subclasshook__(%r)", C)
        if cls is Transformable:
            if any("__transform__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented