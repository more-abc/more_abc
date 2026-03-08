import pytest
from abc import abstractmethod
from enum import Enum, EnumMeta, IntEnum, Flag, IntFlag

from more_abc import (
    ABCEnumMeta,
    ABCEnum,
    ABCFlag,
    ABCIntFlag,
    ABCIntEnum
)


# ---------------------------------------------------------------------------
# ABCEnumMeta
# ---------------------------------------------------------------------------

class TestABCEnumMeta:
    def test_is_subclass_of_EnumMeta(self):
        assert issubclass(ABCEnumMeta, EnumMeta)

    def test_ABCEnum_uses_ABCEnumMeta(self):
        assert type(ABCEnum) is ABCEnumMeta

    def test_ABCIntEnum_uses_ABCEnumMeta(self):
        assert type(ABCIntEnum) is ABCEnumMeta

    def test_ABCFlag_uses_ABCEnumMeta(self):
        assert type(ABCFlag) is ABCEnumMeta

    def test_ABCIntFlag_uses_ABCEnumMeta(self):
        assert type(ABCIntFlag) is ABCEnumMeta

    def test_concrete_subclass_uses_ABCEnumMeta(self):
        class Color(ABCEnum):
            RED = 1

        assert type(Color) is ABCEnumMeta


# ---------------------------------------------------------------------------
# ABCEnum — basic enum behaviour
# ---------------------------------------------------------------------------

class TestABCEnum:
    def test_basic_members(self):
        class Color(ABCEnum):
            RED = 1
            GREEN = 2
            BLUE = 3

        assert Color.RED.value == 1
        assert Color.GREEN.value == 2
        assert Color.BLUE.value == 3

    def test_member_name(self):
        class Color(ABCEnum):
            RED = 1

        assert Color.RED.name == "RED"

    def test_iteration(self):
        class Color(ABCEnum):
            RED = 1
            GREEN = 2

        assert list(Color) == [Color.RED, Color.GREEN]

    def test_isinstance_Enum(self):
        class Color(ABCEnum):
            RED = 1

        assert isinstance(Color.RED, Enum)

    def test_isinstance_ABCEnum(self):
        class Color(ABCEnum):
            RED = 1

        assert isinstance(Color.RED, ABCEnum)

    def test_abstractmethods_tracked(self):
        """ABCEnumMeta records abstract methods in __abstractmethods__.

        Note: unlike regular ABCs, EnumMeta creates members inside __new__,
        bypassing ABCMeta.__call__'s instantiation guard.  The contract is
        therefore enforced via __abstractmethods__ metadata, not TypeError.
        """
        class AbstractOp(ABCEnum):
            @abstractmethod
            def execute(self) -> object: ...

        assert "execute" in AbstractOp.__abstractmethods__

    def test_concrete_subclass_clears_abstractmethods(self):
        """A subclass that implements all abstract methods has an empty set."""
        class AbstractOp(ABCEnum):
            @abstractmethod
            def execute(self) -> object: ...

        class ConcreteOp(AbstractOp):
            ADD = 1

            def execute(self) -> object:
                return self.value

        assert not ConcreteOp.__abstractmethods__

    def test_abstract_method_implemented(self):
        class Op(ABCEnum):
            @abstractmethod
            def execute(self) -> object: ...

        class ConcreteOp(Op):
            ADD = 1
            SUB = 2

            def execute(self) -> object:
                return self.value

        assert ConcreteOp.ADD.execute() == 1
        assert ConcreteOp.SUB.execute() == 2

    def test_multiple_abstract_methods(self):
        class Descriptor(ABCEnum):
            @abstractmethod
            def label(self) -> str: ...

            @abstractmethod
            def description(self) -> str: ...

        class ConcreteDescriptor(Descriptor):
            ITEM = 1

            def label(self) -> str:
                return "item"

            def description(self) -> str:
                return "an item"

        assert ConcreteDescriptor.ITEM.label() == "item"
        assert ConcreteDescriptor.ITEM.description() == "an item"

    def test_is_subclass_of_Enum(self):
        assert issubclass(ABCEnum, Enum)


# ---------------------------------------------------------------------------
# ABCIntEnum
# ---------------------------------------------------------------------------

class TestABCIntEnum:
    def test_basic_members(self):
        class Status(ABCIntEnum):
            OK = 200
            NOT_FOUND = 404

        assert Status.OK == 200
        assert Status.NOT_FOUND == 404

    def test_integer_comparison(self):
        class Priority(ABCIntEnum):
            LOW = 1
            HIGH = 10

        assert Priority.HIGH > Priority.LOW
        assert Priority.LOW + 1 == 2

    def test_isinstance_int(self):
        class Status(ABCIntEnum):
            OK = 200

        assert isinstance(Status.OK, int)

    def test_isinstance_IntEnum(self):
        class Status(ABCIntEnum):
            OK = 200

        assert isinstance(Status.OK, IntEnum)

    def test_isinstance_ABCIntEnum(self):
        class Status(ABCIntEnum):
            OK = 200

        assert isinstance(Status.OK, ABCIntEnum)

    def test_is_subclass_of_IntEnum(self):
        assert issubclass(ABCIntEnum, IntEnum)

    def test_abstractmethods_tracked(self):
        class AbstractCode(ABCIntEnum):
            @abstractmethod
            def message(self) -> str: ...

        assert "message" in AbstractCode.__abstractmethods__

    def test_concrete_subclass_clears_abstractmethods(self):
        class AbstractCode(ABCIntEnum):
            @abstractmethod
            def message(self) -> str: ...

        class ConcreteCode(AbstractCode):
            OK = 200

            def message(self) -> str:
                return f"HTTP {self.value}"

        assert not ConcreteCode.__abstractmethods__

    def test_abstract_method_implemented(self):
        class Code(ABCIntEnum):
            @abstractmethod
            def message(self) -> str: ...

        class ConcreteCode(Code):
            OK = 200
            NOT_FOUND = 404

            def message(self) -> str:
                return f"HTTP {self.value}"

        assert ConcreteCode.OK.message() == "HTTP 200"
        assert ConcreteCode.NOT_FOUND.message() == "HTTP 404"

    def test_arithmetic(self):
        class Offset(ABCIntEnum):
            ZERO = 0
            ONE = 1

        assert Offset.ZERO + Offset.ONE == 1


# ---------------------------------------------------------------------------
# ABCFlag
# ---------------------------------------------------------------------------

class TestABCFlag:
    def test_basic_members(self):
        class Perm(ABCFlag):
            READ = 1
            WRITE = 2
            EXEC = 4

        assert Perm.READ.value == 1

    def test_bitwise_or(self):
        class Perm(ABCFlag):
            READ = 1
            WRITE = 2

        combined = Perm.READ | Perm.WRITE
        assert Perm.READ in combined
        assert Perm.WRITE in combined

    def test_bitwise_and(self):
        class Perm(ABCFlag):
            READ = 1
            WRITE = 2
            EXEC = 4

        rw = Perm.READ | Perm.WRITE
        assert (rw & Perm.READ) == Perm.READ
        assert (rw & Perm.EXEC).value == 0

    def test_isinstance_Flag(self):
        class Perm(ABCFlag):
            READ = 1

        assert isinstance(Perm.READ, Flag)

    def test_isinstance_ABCFlag(self):
        class Perm(ABCFlag):
            READ = 1

        assert isinstance(Perm.READ, ABCFlag)

    def test_is_subclass_of_Flag(self):
        assert issubclass(ABCFlag, Flag)

    def test_abstractmethods_tracked(self):
        class AbstractPerm(ABCFlag):
            @abstractmethod
            def describe(self) -> str: ...

        assert "describe" in AbstractPerm.__abstractmethods__

    def test_concrete_subclass_clears_abstractmethods(self):
        class AbstractPerm(ABCFlag):
            @abstractmethod
            def describe(self) -> str: ...

        class ConcretePerm(AbstractPerm):
            READ = 1

            def describe(self) -> str:
                return self.name or ""

        assert not ConcretePerm.__abstractmethods__

    def test_abstract_method_implemented(self):
        class Perm(ABCFlag):
            @abstractmethod
            def describe(self) -> str: ...

        class ConcretePerm(Perm):
            READ = 1
            WRITE = 2

            def describe(self) -> str:
                return self.name or ""

        assert ConcretePerm.READ.describe() == "READ"
        assert ConcretePerm.WRITE.describe() == "WRITE"


# ---------------------------------------------------------------------------
# ABCIntFlag
# ---------------------------------------------------------------------------

class TestABCIntFlag:
    def test_basic_members(self):
        class Access(ABCIntFlag):
            NONE = 0
            READ = 1
            WRITE = 2
            EXEC = 4

        assert Access.READ == 1
        assert Access.WRITE == 2

    def test_isinstance_int(self):
        class Access(ABCIntFlag):
            READ = 1

        assert isinstance(Access.READ, int)

    def test_isinstance_IntFlag(self):
        class Access(ABCIntFlag):
            READ = 1

        assert isinstance(Access.READ, IntFlag)

    def test_isinstance_ABCIntFlag(self):
        class Access(ABCIntFlag):
            READ = 1

        assert isinstance(Access.READ, ABCIntFlag)

    def test_is_subclass_of_IntFlag(self):
        assert issubclass(ABCIntFlag, IntFlag)

    def test_bitwise_or(self):
        class Access(ABCIntFlag):
            READ = 1
            WRITE = 2

        combined = Access.READ | Access.WRITE
        assert combined == 3

    def test_bitwise_and(self):
        class Access(ABCIntFlag):
            READ = 1
            WRITE = 2
            EXEC = 4

        rw = Access.READ | Access.WRITE
        assert rw & Access.READ == Access.READ
        assert rw & Access.EXEC == 0

    def test_abstractmethods_tracked(self):
        class AbstractAccess(ABCIntFlag):
            @abstractmethod
            def label(self) -> str: ...

        assert "label" in AbstractAccess.__abstractmethods__

    def test_concrete_subclass_clears_abstractmethods(self):
        class AbstractAccess(ABCIntFlag):
            @abstractmethod
            def label(self) -> str: ...

        class ConcreteAccess(AbstractAccess):
            READ = 1

            def label(self) -> str:
                return f"access:{self.value}"

        assert not ConcreteAccess.__abstractmethods__

    def test_abstract_method_implemented(self):
        class Access(ABCIntFlag):
            @abstractmethod
            def label(self) -> str: ...

        class ConcreteAccess(Access):
            NONE = 0
            READ = 1
            WRITE = 2

            def label(self) -> str:
                return f"access:{self.value}"

        assert ConcreteAccess.READ.label() == "access:1"
        assert ConcreteAccess.WRITE.label() == "access:2"

    def test_integer_arithmetic(self):
        class Bits(ABCIntFlag):
            A = 1
            B = 2

        assert Bits.A + Bits.B == 3
