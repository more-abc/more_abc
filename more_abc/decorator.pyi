from typing import Type, Any, Callable

__all__ = [
    "abstract_class",
    "abstractproperty"
]

def abstract_class(*method_names: str) -> Callable[[Type[Any]], Type[Any]]: ...

def abstractproperty(read_only: bool = ...) -> Callable[[Callable[..., Any]], property]: ...