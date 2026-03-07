"""This submodule is an extension of the ABC functionality within the `dataclasses` module."""

from dataclasses import dataclass
from abc import ABC, ABCMeta
from .devtools import abc_logger

def _ensure_abcmeta(cls):
    """Rebuild *cls* with ABCMeta as its metaclass if it doesn't already use one."""
    abc_logger.debug("_ensure_abcmeta(%r)", cls)
    if isinstance(cls, ABCMeta):
        abc_logger.debug("  %r already uses ABCMeta, skipping", cls)
        return cls
    bases = cls.__bases__
    # Replace bare `object` with ABC to avoid a metaclass conflict.
    new_bases = tuple(ABC if b is object else b for b in bases)
    if not any(isinstance(b, ABCMeta) for b in new_bases):
        new_bases = (ABC,) + new_bases
    ns = {k: v for k, v in cls.__dict__.items()
          if k not in ("__dict__", "__weakref__")}
    result = ABCMeta(cls.__name__, new_bases, ns)
    abc_logger.debug("  rebuilt %r with ABCMeta, new bases: %s", cls.__name__, new_bases)
    return result


def abstractdataclass(cls=None, /, *, init=True, repr=True, eq=True, order=False,
              unsafe_hash=False, frozen=False, match_args=True,
              kw_only=False, slots=False, weakref_slot=False):
    """A decorator that combines ``@dataclass`` with ABC abstract-method support.

    Accepts the same keyword arguments as :func:`dataclasses.dataclass`.
    The decorated class gains ``ABCMeta`` as its metaclass automatically, so
    you can declare :func:`~abc.abstractmethod` members without manually
    inheriting from :class:`~abc.ABC`.
    """
    def wrap(c):
        abc_logger.debug("abstractdataclass.wrap(%r)", c)
        c = _ensure_abcmeta(c)
        result = dataclass(c,
                        init=init,
                        repr=repr,
                        eq=eq,
                        order=order,
                        unsafe_hash=unsafe_hash,
                        frozen=frozen,
                        match_args=match_args,
                        kw_only=kw_only,
                        slots=slots,
                        weakref_slot=weakref_slot) # type: ignore
        abc_logger.debug("  -> %r", result)
        return result

    if cls is None:
        abc_logger.debug("abstractdataclass() called with keyword args, returning wrap")
        return wrap
    abc_logger.debug("abstractdataclass(%r) called directly", cls)
    return wrap(cls)
