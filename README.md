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
