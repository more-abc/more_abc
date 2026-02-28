# more_abc

This module is an extension of the `abc` module, 
with many similar features added.

![License: MIT](https://img.shields.io/badge/GPL-3.0-%2396DA45?style=for-the-badge&logo=opensourceinitiative&logoColor=white)
![text](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![text](https://img.shields.io/badge/Status-Active-brightgreen)
[![PyPI Version](https://img.shields.io/pypi/v/more_abc.svg)](https://pypi.org/project/more_abc/)

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

`ABCEnumMeta` is the underlying combined metaclass (`ABCMeta + EnumMeta`) and is available for advanced use cases.

### ABCIntEnum

`ABCIntEnum` is an `IntEnum` base class that supports abstract methods. Members compare equal to their integer values.

```python
from abc import abstractmethod
from more_abc import ABCIntEnum

class Permission(ABCIntEnum):
    READ    = 1
    WRITE   = 2
    EXECUTE = 4

    @abstractmethod
    def label(self) -> str: ...

class FilePermission(Permission):
    READ    = 1
    WRITE   = 2
    EXECUTE = 4

    def label(self) -> str:
        return self.name.lower()

print(FilePermission.READ.label())   # "read"
print(FilePermission.READ > 0)       # True  (int comparison)
```

### ABCFlag

`ABCFlag` is a `Flag` base class that supports abstract methods. Members can be combined with bitwise operators.

```python
from abc import abstractmethod
from more_abc import ABCFlag

class Access(ABCFlag):
    READ    = 1
    WRITE   = 2
    EXECUTE = 4

    @abstractmethod
    def describe(self) -> str: ...

class FileAccess(Access):
    READ    = 1
    WRITE   = 2
    EXECUTE = 4

    def describe(self) -> str:
        return f"FileAccess({self.name})"

rw = FileAccess.READ | FileAccess.WRITE
print(rw)  # FileAccess.READ|WRITE
```

### ABCIntFlag

`ABCIntFlag` is an `IntFlag` base class that supports abstract methods. Combines integer semantics with bitwise flag operations.

```python
from abc import abstractmethod
from more_abc import ABCIntFlag

class Mode(ABCIntFlag):
    READ    = 0o4
    WRITE   = 0o2
    EXECUTE = 0o1

    @abstractmethod
    def to_octal(self) -> str: ...

class UnixMode(Mode):
    READ    = 0o4
    WRITE   = 0o2
    EXECUTE = 0o1

    def to_octal(self) -> str:
        return oct(self.value)

print(UnixMode.READ.to_octal())              # '0o4'
print((UnixMode.READ | UnixMode.WRITE) == 6) # True
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

### AbstractLogHandler

`AbstractLogHandler` is an abstract base for `logging.Handler`. Subclasses must implement `configure()` and `emit()`. The concrete `close()` method handles thread-safe resource cleanup automatically.

```python
import logging
from more_abc import AbstractLogHandler

class PrintHandler(AbstractLogHandler):
    def configure(self, config: dict) -> None:
        self._handler_config.update(config)

    def emit(self, record: logging.LogRecord) -> None:
        print(self.format(record))

handler = PrintHandler(level=logging.DEBUG)
handler.configure({"prefix": "[LOG]"})

logger = logging.getLogger("demo")
logger.addHandler(handler)
logger.warning("something happened")
```

### AbstractLogFormatter

`AbstractLogFormatter` is an abstract base for `logging.Formatter`. Subclasses must implement `format()`.

```python
import logging
from more_abc import AbstractLogFormatter

class UpperFormatter(AbstractLogFormatter):
    def format(self, record: logging.LogRecord) -> str:
        return f"[{record.levelname}] {record.getMessage().upper()}"

handler = logging.StreamHandler()
handler.setFormatter(UpperFormatter())
```

### AbstractLogFilter

`AbstractLogFilter` is an abstract base for `logging.Filter`. Subclasses must implement `filter()`, returning `True` to allow a record through or `False` to discard it.

```python
import logging
from more_abc import AbstractLogFilter

class ErrorOnlyFilter(AbstractLogFilter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno >= logging.ERROR

handler = logging.StreamHandler()
handler.addFilter(ErrorOnlyFilter())
```

### abc re-exports

`more_abc` re-exports all public symbols from the standard `abc` module, so you can use it as a single import for everything ABC-related.

```python
# Instead of:
from abc import ABC, ABCMeta, abstractmethod
from more_abc import ABCMixin, abstractdataclass

# You can do:
from more_abc import ABC, ABCMeta, abstractmethod, ABCMixin, abstractdataclass
```

Available re-exports: `ABC`, `ABCMeta`, `abstractmethod`, `abstractproperty`, `get_cache_token`.

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

### AbstractRawIO

`AbstractRawIO` is an abstract base for `io.RawIOBase`. Subclasses must implement `read()`, `readinto()`, and `write()`.

```python
from more_abc import AbstractRawIO

class MemoryRawIO(AbstractRawIO):
    def __init__(self, data: bytes):
        self._buf = bytearray(data)
        self._pos = 0

    def read(self, size=-1) -> bytes:
        if size == -1:
            chunk = bytes(self._buf[self._pos:])
            self._pos = len(self._buf)
        else:
            chunk = bytes(self._buf[self._pos:self._pos + size])
            self._pos += len(chunk)
        return chunk

    def readinto(self, b) -> int:
        data = self.read(len(b))
        n = len(data)
        b[:n] = data
        return n

    def write(self, b) -> int:
        self._buf[self._pos:self._pos + len(b)] = b
        self._pos += len(b)
        return len(b)
```

### AbstractBufferedIO

`AbstractBufferedIO` is an abstract base for `io.BufferedIOBase`. Subclasses must implement `read()`, `read1()`, and `write()`.

```python
from more_abc import AbstractBufferedIO

class SimpleBufferedIO(AbstractBufferedIO):
    def __init__(self, raw: bytes):
        self._buf = bytearray(raw)
        self._pos = 0

    def read(self, size=None) -> bytes:
        if size is None:
            chunk = bytes(self._buf[self._pos:])
            self._pos = len(self._buf)
        else:
            chunk = bytes(self._buf[self._pos:self._pos + size])
            self._pos += len(chunk)
        return chunk

    def read1(self, size=-1) -> bytes:
        return self.read(size)

    def write(self, b) -> int:
        self._buf += b
        return len(b)
```

### AbstractTextIO

`AbstractTextIO` is an abstract base for `io.TextIOBase`. Subclasses must implement `read()`, `readline()`, and `write()`.

```python
from more_abc import AbstractTextIO

class StringIO(AbstractTextIO):
    def __init__(self, text: str = ""):
        self._lines = text.splitlines(keepends=True)
        self._pos = 0

    def read(self, size=None) -> str:
        text = "".join(self._lines[self._pos:])
        self._pos = len(self._lines)
        return text if size is None else text[:size]

    def readline(self, size=-1) -> str:
        if self._pos >= len(self._lines):
            return ""
        line = self._lines[self._pos]
        self._pos += 1
        return line if size == -1 else line[:size]

    def write(self, s: str) -> int:
        self._lines.extend(s.splitlines(keepends=True))
        return len(s)
```

### AbstractJSONEncoder

`AbstractJSONEncoder` is an abstract base for `json.JSONEncoder`. Subclasses must implement `default()`, `encode()`, and `iterencode()`.

```python
from more_abc import AbstractJSONEncoder
from datetime import datetime

class DateTimeEncoder(AbstractJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

    def encode(self, o):
        return super().encode(o)

    def iterencode(self, o, _one_shot=False):
        return super().iterencode(o, _one_shot)

import json
data = {"timestamp": datetime(2024, 1, 15, 10, 30)}
result = json.dumps(data, cls=DateTimeEncoder)
print(result)  # {"timestamp": "2024-01-15T10:30:00"}
```

### AbstractJSONDecoder

`AbstractJSONDecoder` is an abstract base for `json.JSONDecoder`. Subclasses must implement `decode()` and `raw_decode()`.

```python
from more_abc import AbstractJSONDecoder
import json

class UpperCaseDecoder(AbstractJSONDecoder):
    def decode(self, s):
        obj = super().decode(s)
        if isinstance(obj, dict):
            return {k.upper(): v for k, v in obj.items()}
        return obj

    def raw_decode(self, s, idx=0):
        return super().raw_decode(s, idx)

data = '{"name": "alice", "age": 30}'
result = json.loads(data, cls=UpperCaseDecoder)
print(result)  # {'NAME': 'alice', 'AGE': 30}
```
