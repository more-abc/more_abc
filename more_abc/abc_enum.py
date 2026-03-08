"""This submodule is an extension of the ABC functionality within the `enum` module."""

from abc import ABCMeta
from enum import Enum, EnumMeta, IntEnum, Flag, IntFlag
from ._devtools import abc_logger

__all__ = ["ABCEnumMeta", "ABCEnum", "ABCIntEnum", "ABCFlag", "ABCIntFlag"]


# It's just a very simple wrap-up.
# I'm not sure if this can even be called "packaging" — it's merely the
# inheritance and encapsulation of a class.
class ABCEnumMeta(ABCMeta, EnumMeta):
    """Combined metaclass of :class:`~abc.ABCMeta` and :class:`~enum.EnumMeta`.

    Allows enum classes to declare abstract methods via
    :func:`~abc.abstractmethod`.  You rarely need to use this directly —
    prefer subclassing :class:`ABCEnum` instead.
    """
    def __new__(mcs, name, bases, namespace, **kwargs):
        abc_logger.debug("ABCEnumMeta.__new__: creating class %r", name)
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        abc_logger.debug("  -> %r created", cls)
        return cls


class ABCEnum(Enum, metaclass=ABCEnumMeta):
    """An :class:`~enum.Enum` base class that supports abstract methods.

    Subclass this instead of :class:`~enum.Enum` when you want to enforce
    that concrete enum subclasses implement certain methods.
    """
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("ABCEnum subclassed: %r", cls)


class ABCIntEnum(IntEnum, metaclass=ABCEnumMeta):
    """An :class:`~enum.IntEnum` base class that supports abstract methods.

    Members compare equal to their integer values, while still allowing
    abstract-method enforcement via :func:`~abc.abstractmethod`.
    """
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("ABCIntEnum subclassed: %r", cls)


class ABCFlag(Flag, metaclass=ABCEnumMeta):
    """A :class:`~enum.Flag` base class that supports abstract methods.

    Supports bitwise combination of members, while still allowing
    abstract-method enforcement via :func:`~abc.abstractmethod`.
    """
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("ABCFlag subclassed: %r", cls)


class ABCIntFlag(IntFlag, metaclass=ABCEnumMeta):
    """An :class:`~enum.IntFlag` base class that supports abstract methods.

    Members are integers and support bitwise operations, while still
    allowing abstract-method enforcement via :func:`~abc.abstractmethod`.
    """
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("ABCIntFlag subclassed: %r", cls)
