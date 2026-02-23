from typing import Callable, TypeVar, overload

__all__ = ["abc_dataclass"]

_T = TypeVar("_T")

def _ensure_abcmeta(cls: type) -> type: ...

@overload
def abc_dataclass(cls: type[_T], /) -> type[_T]: ...
@overload
def abc_dataclass(
    cls: None = ...,
    /,
    *,
    init: bool = ...,
    repr: bool = ...,
    eq: bool = ...,
    order: bool = ...,
    unsafe_hash: bool = ...,
    frozen: bool = ...,
    match_args: bool = ...,
    kw_only: bool = ...,
    slots: bool = ...,
    weakref_slot: bool = ...,
) -> Callable[[type[_T]], type[_T]]: ...
