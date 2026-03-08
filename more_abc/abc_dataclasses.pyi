"""Type stubs for more_abc.abc_dataclasses."""

from typing import Callable, TypeVar, overload

__all__ = ["abstractdataclass"]

_T = TypeVar("_T")


@overload
def abstractdataclass(cls: type[_T], /) -> type[_T]: ...
@overload
def abstractdataclass(
    cls: None = None,
    /,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    match_args: bool = True,
    kw_only: bool = False,
    slots: bool = False,
    weakref_slot: bool = False,
) -> Callable[[type[_T]], type[_T]]: ...
