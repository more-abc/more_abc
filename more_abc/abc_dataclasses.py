"""This submodule is an extension of the ABC functionality within the `dataclasses` module."""

from dataclasses import dataclass
from abc import ABC, ABCMeta

def _ensure_abcmeta(cls):
    """Rebuild *cls* with ABCMeta as its metaclass if it doesn't already use one."""
    if isinstance(cls, ABCMeta):
        return cls
    bases = cls.__bases__
    # Replace bare `object` with ABC to avoid a metaclass conflict.
    new_bases = tuple(ABC if b is object else b for b in bases)
    if not any(isinstance(b, ABCMeta) for b in new_bases):
        new_bases = (ABC,) + new_bases
    ns = {k: v for k, v in cls.__dict__.items()
          if k not in ("__dict__", "__weakref__")}
    return ABCMeta(cls.__name__, new_bases, ns)



def abstractdataclass(cls=None, /, **kwargs):
    """A decorator that combines ``@dataclass`` with ABC abstract-method support.

    Accepts the same keyword arguments as :func:`dataclasses.dataclass`.
    The decorated class gains ``ABCMeta`` as its metaclass automatically, so
    you can declare :func:`~abc.abstractmethod` members without manually
    inheriting from :class:`~abc.ABC`.
    """
    def wrap(c):
        c = _ensure_abcmeta(c)
        return dataclass(c, **kwargs)

    if cls is None:
        return wrap
    return wrap(cls)
