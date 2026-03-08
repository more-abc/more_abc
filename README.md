# more_abc

This module is an extension of the `abc` module, 
with many similar features added.

![text](https://img.shields.io/badge/GPL-3.0-%2396DA45?style=for-the-badge&logo=opensourceinitiative&logoColor=white)
![text](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![text](https://img.shields.io/badge/Status-Active-brightgreen)
[![text](https://img.shields.io/pypi/v/more_abc.svg)](https://pypi.org/project/more_abc/)

In addition, there are many similar functions. For details, please refer to the **official documentation** of this module.
(It hasn’t been launched yet.)

## Installation

```bash
pip install more-abc
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

`ABCException` is an abstract base for custom exceptions. Subclasses must implement `get_message()`.

```python
from more_abc import ABCException

class NotFoundError(ABCException):
    def get_message(self) -> str:
        return f"Class {self.cls!r} was not found."

raise NotFoundError(cls="MyClass")
# NotFoundError: Class 'MyClass' was not found.
```

### ABCEnum

`ABCEnum` is an `Enum` base class that supports abstract methods. Use it when you want to define an enum interface that concrete subclasses must implement.

```python
from abc import abstractmethod
from more_abc import ABCEnum

class Direction(ABCEnum):
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

### abstract_class

`abstract_class` is a decorator that converts any regular class into an ABC and marks the specified method names as abstract, without requiring manual `ABCMeta` or `ABC` inheritance.

```python
from more_abc import abstract_class

@abstract_class('run', 'stop')
class Worker:
    def run(self): ...
    def stop(self): ...

class MyWorker(Worker):
    def run(self):
        print("running")

    def stop(self):
        print("stopped")

w = MyWorker()
w.run()   # running
w.stop()  # stopped
```

Attempting to instantiate without implementing all abstract methods raises `TypeError`:

```python
class BadWorker(Worker):
    def run(self):
        print("running")
# missing stop()

BadWorker()  # TypeError: Can't instantiate abstract class BadWorker without an implementation for abstract method 'stop'
```

Methods listed in `abstract_class` that don't exist on the decorated class are automatically added as abstract stubs:

```python
@abstract_class('process', 'cleanup')
class Pipeline:
    pass  # neither method defined — both become abstract stubs

class MyPipeline(Pipeline):
    def process(self): ...
    def cleanup(self): ...
```

### abstractdataclass

`abstractdataclass` is a drop-in replacement for `@dataclass` that automatically gives the class `ABCMeta` as its metaclass, so you can use `@abstractmethod` without manually inheriting from `ABC`.

```python
from abc import abstractmethod
from more_abc import abstractdataclass

@abstractdataclass
class Shape:
    color: str

    @abstractmethod
    def area(self) -> float: ...

@abstractdataclass(frozen=True)
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

### Sortable / Filterable / Transformable

`more_abc.collections_abc` provides three ABC families for custom collection types, each following the same `Base* / *Mixin / *` pattern.

**Sortable** — in-place sorting via `__sort__`:

```python
from more_abc import Sortable

class NumberList(Sortable):
    def __init__(self, data: list):
        self._data = list(data)

    def __sort__(self, reverse=False):
        self._data.sort(reverse=reverse)

    def __copy__(self):
        return NumberList(self._data)

nl = NumberList([3, 1, 2])
nl.sort()                    # in-place: [1, 2, 3]
asc = nl.sorted(reverse=True)  # new copy: [3, 2, 1]
```

**Filterable** — predicate filtering via `__filter__`:

```python
from more_abc import Filterable

class NumberList(Filterable):
    def __init__(self, data: list):
        self._data = list(data)

    def __filter__(self, predicate):
        return NumberList([x for x in self._data if predicate(x)])

nl = NumberList([1, 2, 3, 4, 5])
evens = nl.filter(lambda x: x % 2 == 0)   # [2, 4]
odds  = nl.reject(lambda x: x % 2 == 0)   # [1, 3, 5]
```

**Transformable** — element-wise mapping via `__transform__`:

```python
from more_abc import Transformable

class NumberList(Transformable):
    def __init__(self, data: list):
        self._data = list(data)

    def __transform__(self, func):
        return NumberList([func(x) for x in self._data])

nl = NumberList([1, 2, 3])
doubled = nl.map(lambda x: x * 2)  # [2, 4, 6]
```

`BaseSortable`, `SortableMixin`, `BaseFilterable`, `FilterableMixin`, `BaseTransformable`, and `TransformableMixin` are also exported for advanced composition.
