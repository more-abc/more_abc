"""This submodule is an extension of the ABC **decoratorality**."""

from abc import abstractmethod, ABCMeta

__all__ = [
    "abstract_class",
    "abstractproperty"
]

#  To facilitate understanding, I have made an exception 
# to add usage examples for this function.

# Example:
# @abstract_class('run', 'stop')
# class Worker:
#     def run(self): ...
#     def stop(self): ...

# class MyWorker(Worker):
#     def run(self): 
#         print("running")
#     def stop(self): 
#         print("stopped")

def abstract_class(*method_names):
    """
    Class decorator that converts a regular class into an ABC and marks
    the specified method names as abstract methods.
    """
    def decorator(cls):
        namespace = {}
        for key, value in vars(cls).items():
            if key in ('__dict__', '__weakref__'):
                continue
            if key in method_names and callable(value):
                namespace[key] = abstractmethod(value)
            else:
                namespace[key] = value

        for name in method_names:
            if name not in namespace:
                def _stub(self):
                    pass
                _stub.__name__ = name
                _stub.__qualname__ = f"{cls.__qualname__}.{name}"
                namespace[name] = abstractmethod(_stub)

        new_cls = ABCMeta(cls.__name__, cls.__bases__, namespace)
        new_cls.__qualname__ = cls.__qualname__
        new_cls.__module__ = cls.__module__
        return new_cls

    return decorator

def abstractproperty(read_only=True):
    """
    Enhanced replacement for the deprecated ``abc.abstractproperty``.

    Defines an abstract property on an ABC. Subclasses must provide a
    concrete ``@property`` implementation. When *read_only* is ``False``,
    subclasses must also implement a setter.
    """
    def decorator(func):
        prop = property(abstract_func := abstractmethod(func))
        prop.__is_abstract_property__ = True  # type: ignore[attr-defined]
        prop.__abstract_read_only__ = read_only  # type: ignore[attr-defined]

        if not read_only:
            original_setter = prop.setter

            def setter(fset):
                abstract_fset = abstractmethod(fset)
                return original_setter(abstract_fset)

            prop = prop.__class__(
                prop.fget,
                prop.fset,
                prop.fdel,
                prop.__doc__,
            )
            prop.setter = setter  # type: ignore[method-assign]

        return prop

    return decorator
