"""Type stubs for more_abc.abc_enum."""

from abc import ABCMeta
from enum import Enum, EnumMeta, IntEnum, Flag, IntFlag

__all__ = ["ABCEnumMeta", "ABCEnum", "ABCIntEnum", "ABCFlag", "ABCIntFlag"]


class ABCEnumMeta(ABCMeta, EnumMeta):
    """Combined metaclass of :class:`~abc.ABCMeta` and
    :class:`~enum.EnumMeta`."""
    ...


class ABCEnum(Enum, metaclass=ABCEnumMeta):
    """An :class:`~enum.Enum` base class that supports abstract methods."""
    ...


class ABCIntEnum(IntEnum, metaclass=ABCEnumMeta):
    """An :class:`~enum.IntEnum` base class that supports abstract methods."""
    ...


class ABCFlag(Flag, metaclass=ABCEnumMeta):
    """A :class:`~enum.Flag` base class that supports abstract methods."""
    ...


class ABCIntFlag(IntFlag, metaclass=ABCEnumMeta):
    """An :class:`~enum.IntFlag` base class that supports abstract methods."""
    ...
