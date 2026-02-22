# more_abc

This module is an extension of the `abc` module, 
with many similar features added.

![License: MIT](https://img.shields.io/badge/License-MIT-%2396DA45?style=for-the-badge&logo=opensourceinitiative&logoColor=white)
![](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![](https://img.shields.io/badge/Status-Active-brightgreen)

This module refers to PEP 3119.
See [new url](https://peps.python.org/pep-3119/) or [old url](https://legacy.python.org/dev/peps/pep-3119/)

## Installation

```bash
pip install git+https://github.com/aiwonderland/more_abc.git
```

## Usage

### ABCMixin

`ABCMixin` enforces implementation of `initialize`, `validate`, and `to_dict` on subclasses, and provides `is_valid()` and `get_info()` for free.

```python
from more_abc import ABCMixin

class User(ABCMixin):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.initialize()

    def initialize(self):
        self.active = True

    def validate(self) -> bool:
        return isinstance(self.name, str) and self.age >= 0

    def to_dict(self) -> dict:
        return {"name": self.name, "age": self.age, "active": self.active}

user = User("Alice", 30)
print(user.is_valid())   # True
print(user.get_info())   # {'data': {'name': 'Alice', 'age': 30, 'active': True}, 'is_valid': True, 'class_name': 'User'}
print(repr(user))        # User({'name': 'Alice', 'age': 30, 'active': True})
```

### ABCException

`ABCException` is an abstract base for custom exceptions. Subclasses must implement `_get_message()`.

```python
from more_abc import ABCException

class NotFoundError(ABCException):
    def _get_message(self) -> str:
        return f"Class {self.cls!r} was not found."

raise NotFoundError(cls="MyClass")
# NotFoundError: Class 'MyClass' was not found.
```

### ABCWarning

`ABCWarning` works the same way as `ABCException` but for warnings.

```python
import warnings
from more_abc import ABCWarning

class DeprecatedWarning(ABCWarning):
    def _get_message(self) -> str:
        return f"{self.cls!r} is deprecated and will be removed in a future version."

warnings.warn(DeprecatedWarning(cls="OldClass"))
# DeprecatedWarning: 'OldClass' is deprecated and will be removed in a future version.
```

### AbcEnum

`AbcEnum` is an `Enum` base class that supports abstract methods. Use it when you want to define an enum interface that concrete subclasses must implement.

```python
from abc import abstractmethod
from more_abc import AbcEnum

class Direction(AbcEnum):
    NORTH = "N"
    SOUTH = "S"
    EAST  = "E"
    WEST  = "W"

    @abstractmethod
    def opposite(self) -> "Direction": ...

# Direction.NORTH  →  TypeError: Can't instantiate abstract class Direction …

class CardinalDirection(Direction):
    NORTH = "N"
    SOUTH = "S"
    EAST  = "E"
    WEST  = "W"

    def opposite(self) -> "CardinalDirection":
        _opp = {"N": "S", "S": "N", "E": "W", "W": "E"}
        return CardinalDirection(_opp[self.value])

print(CardinalDirection.NORTH.opposite())  # CardinalDirection.SOUTH
```

`ABCEnumMeta` is the underlying combined metaclass (`ABCMeta + EnumMeta`) and is available for advanced use cases.

### abc_dataclass

`abc_dataclass` is a drop-in replacement for `@dataclass` that automatically gives the class `ABCMeta` as its metaclass, so you can use `@abstractmethod` without manually inheriting from `ABC`.

```python
from abc import abstractmethod
from more_abc import abc_dataclass

@abc_dataclass
class Shape:
    color: str

    @abstractmethod
    def area(self) -> float: ...

@abc_dataclass(frozen=True)
class Circle(Shape):
    radius: float

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

c = Circle(color="red", radius=5.0)
print(c.area())   # 78.53975
print(c)          # Circle(color='red', radius=5.0)
```

Attempting to instantiate an abstract class raises `TypeError` as expected:

```python
Shape(color="blue")  # TypeError: Can't instantiate abstract class Shape ...
```

### Type aliases

`ABCclassType` and `ABCMetaclassType` mirror the pattern from the `types` module.

```python
from more_abc import ABCclassType, ABCMetaclassType
from abc import ABC, ABCMeta

assert ABCclassType is type(ABC)       # True
assert ABCMetaclassType is type(ABCMeta)  # True

def accepts_abc_class(cls: ABCclassType):
    print(f"Got an ABC class: {cls}")

accepts_abc_class(ABC)
```

### abc re-exports

`more_abc` re-exports all public symbols from the standard `abc` module, so you can use it as a single import for everything ABC-related.

```python
# Instead of:
from abc import ABC, ABCMeta, abstractmethod
from more_abc import ABCMixin, abc_dataclass

# You can do:
from more_abc import ABC, ABCMeta, abstractmethod, ABCMixin, abc_dataclass
```

Available re-exports: `ABC`, `ABCMeta`, `abstractmethod`, `abstractproperty`, `get_cache_token`.

## CLI

`more_abc` ships a small command-line interface:

```bash
python -m more_abc            # show help
python -m more_abc --version  # print version
python -m more_abc --list     # list all public symbols
python -m more_abc --doc ABCMixin        # print docstring of ABCMixin
python -m more_abc --doc abstractmethod  # print docstring of abstractmethod
python -m more_abc -d AbcEnum            # short form
```

Example output of `--doc`:

```
$ python -m more_abc --doc ABCMixin
A comprehensive ABC Mixin class that provides abstract method patterns
and utility methods for subclasses.

This mixin enforces implementation of core methods while providing
common functionality that works with those abstract methods.
```

```
$ python -m more_abc --doc abstractmethod
A decorator indicating abstract methods.

Requires that the metaclass is ABCMeta or derived from it.  A
class that has a metaclass derived from ABCMeta cannot be
instantiated unless all of its abstract methods and abstract
properties are overridden.  The abstract methods can be called
using any of the normal 'super' call mechanisms.  abstractmethod()
may be used to declare abstract methods for properties and
descriptors.
...
```
