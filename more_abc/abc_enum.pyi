from abc import ABCMeta
from enum import Enum, EnumMeta, IntEnum, Flag, IntFlag
from typing import Any

__all__ = ["ABCEnumMeta", "ABCEnum", "ABCIntEnum", "ABCFlag", "ABCIntFlag"]

class ABCEnumMeta(ABCMeta, EnumMeta): ...

class ABCEnum(Enum, metaclass=ABCEnumMeta):
    def __new__(cls, value: Any) -> ABCEnum: ...

class ABCIntEnum(IntEnum, metaclass=ABCEnumMeta):
    def __new__(cls, value: int) -> ABCIntEnum: ...

class ABCFlag(Flag, metaclass=ABCEnumMeta):
    def __new__(cls, value: int) -> ABCFlag: ...

class ABCIntFlag(IntFlag, metaclass=ABCEnumMeta):
    def __new__(cls, value: int) -> ABCIntFlag: ...
