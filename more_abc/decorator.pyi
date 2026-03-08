"""Type stubs for more_abc.decorator."""

from functools import _CacheInfo
from typing import Any, Callable, ParamSpec, Protocol, TypeVar

__all__ = [
    "abstract_class",
    "abstractproperty",
    "abstract_lru_cache",
]

_ClsT = TypeVar("_ClsT")
_P = ParamSpec("_P")
_T = TypeVar("_T")


def abstract_class(*method_names: str) -> Callable[[type[_ClsT]], type[_ClsT]]:
    """Class decorator that converts a regular class into an ABC and marks
    the specified method names as abstract methods."""
    ...


def abstractproperty(
    read_only: bool = True,
) -> Callable[[Callable[..., Any]], property]:
    """Enhanced replacement for the deprecated ``abc.abstractproperty``.

    When *read_only* is ``False`` subclasses must also implement a setter.
    """
    ...


class _LRUCachedAbstractMethod(Protocol[_P, _T]):
    """Return type of :func:`abstract_lru_cache`-decorated methods."""

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T: ...
    def cache_info(self) -> _CacheInfo: ...
    def cache_clear(self) -> None: ...


def abstract_lru_cache(
    maxsize: int | None = 128,
    typed: bool = False,
) -> Callable[[Callable[_P, _T]], _LRUCachedAbstractMethod[_P, _T]]:
    """Decorator that combines :func:`functools.lru_cache` with
    :func:`~abc.abstractmethod`."""
    ...
