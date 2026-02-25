"""This submodule is an extension of the ABC functionality within the `enum` module."""

from abc import ABCMeta
from enum import Enum, EnumMeta, IntEnum, Flag, IntFlag

__all__ = ["ABCEnumMeta", "AbcEnum", "AbcIntEnum", "AbcFlag", "AbcIntFlag"]


class ABCEnumMeta(ABCMeta, EnumMeta):
    """Combined metaclass of :class:`~abc.ABCMeta` and :class:`~enum.EnumMeta`.

    Allows enum classes to declare abstract methods via
    :func:`~abc.abstractmethod`.  You rarely need to use this directly —
    prefer subclassing :class:`AbcEnum` instead.
    """
    pass


class AbcEnum(Enum, metaclass=ABCEnumMeta):
    """An :class:`~enum.Enum` base class that supports abstract methods.

    Subclass this instead of :class:`~enum.Enum` when you want to enforce
    that concrete enum subclasses implement certain methods.
    """
    pass


class AbcIntEnum(IntEnum, metaclass=ABCEnumMeta):
    """An :class:`~enum.IntEnum` base class that supports abstract methods.

    Members compare equal to their integer values, while still allowing
    abstract-method enforcement via :func:`~abc.abstractmethod`.
    """
    pass


class AbcFlag(Flag, metaclass=ABCEnumMeta):
    """A :class:`~enum.Flag` base class that supports abstract methods.

    Supports bitwise combination of members, while still allowing
    abstract-method enforcement via :func:`~abc.abstractmethod`.
    """
    pass


class AbcIntFlag(IntFlag, metaclass=ABCEnumMeta):
    """An :class:`~enum.IntFlag` base class that supports abstract methods.

    Members are integers and support bitwise operations, while still
    allowing abstract-method enforcement via :func:`~abc.abstractmethod`.
    """
    pass
