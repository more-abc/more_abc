from abc import ABCMeta
from enum import Enum, EnumMeta

__all__ = ["ABCEnumMeta", "AbcEnum"]

class ABCEnumMeta(ABCMeta, EnumMeta): ...

class AbcEnum(Enum, metaclass=ABCEnumMeta): ...
