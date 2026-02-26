from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Type

__all__ = ["ABCMixin",
           "ABCclassType",
           "ABCMetaclassType",
           "ABCException",
           "ABCWarning",
           "abstract_class",
           "abstractproperty"]

class ABCMixin(metaclass=ABCMeta):
    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def validate(self) -> Any: ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    def is_valid(self) -> bool: ...

    def get_info(self) -> dict[str, Any]: ...

    def __repr__(self) -> str: ...

ABCclassType: type[ABCMeta]
ABCMetaclassType: type[type]

class ABCException(Exception, metaclass=ABCMeta):
    cls: Any
    def __init__(self, cls: Any = ...) -> None: ...
    @abstractmethod
    def _get_message(self) -> str: ...

class ABCWarning(Warning, metaclass=ABCMeta):
    cls: Any
    def __init__(self, cls: Any = ...) -> None: ...
    @abstractmethod
    def _get_message(self) -> str: ...

def abstract_class(*method_names: str) -> Callable[[Type[Any]], Type[Any]]: ...

def abstractproperty(read_only: bool = ...) -> Callable[[Callable[..., Any]], property]: ...
