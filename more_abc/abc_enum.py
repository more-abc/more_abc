"""This submodule is an extension of the ABC functionality within the `enum` module."""

from abc import ABCMeta
from enum import Enum, EnumMeta

__all__ = ["ABCEnumMeta", "AbcEnum"]


class ABCEnumMeta(ABCMeta, EnumMeta):
    """Combined metaclass of :class:`~abc.ABCMeta` and :class:`~enum.EnumMeta`.

    Allows enum classes to declare abstract methods via
    :func:`~abc.abstractmethod`.  You rarely need to use this directly —
    prefer subclassing :class:`AbcEnum` instead.
    """


class AbcEnum(Enum, metaclass=ABCEnumMeta):
    """An :class:`~enum.Enum` base class that supports abstract methods.

    Subclass this instead of :class:`~enum.Enum` when you want to enforce
    that concrete enum subclasses implement certain methods.
    """
