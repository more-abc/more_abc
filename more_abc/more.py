"""Core functions (And `types` module like) of the module are contained in this file."""

from abc import ABC, ABCMeta, abstractmethod

__all__ = ["ABCMixin",
           "ABCclassType",
           "ABCMetaclassType",
           "ABCException",
           "ABCWarning",
           "abstract_class"]

# All the ABC classes.
# ======================================================================
class ABCMixin(metaclass=ABCMeta):
    """
    A comprehensive ABC Mixin class that provides abstract method patterns
    and utility methods for subclasses.

    This mixin enforces implementation of core methods while providing
    common functionality that works with those abstract methods.
    """

    @abstractmethod
    def initialize(self):
        """Initialize the instance. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def validate(self):
        """Validate the instance state. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def to_dict(self):
        """Convert instance to dictionary. Must be implemented by subclasses."""
        pass

    def is_valid(self):
        """
        Check if the instance is valid.
        Concrete method that uses the abstract validate method.
        """
        try:
            return self.validate()
        except Exception:
            return False

    def get_info(self):
        """
        Get instance information including validation status.
        Concrete method that combines abstract methods.
        """
        return {
            "data": self.to_dict(),
            "is_valid": self.is_valid(),
            "class_name": self.__class__.__name__
        }

    def __repr__(self):
        """String representation using to_dict method."""
        return f"{self.__class__.__name__}({self.to_dict()})"
# ======================================================================

# ======================================================================
# Like `types` module.

# I just did a light wrapper around both of them.
ABCclassType = type(ABC)
ABCMetaclassType = type(ABCMeta)
# I tried to pass him an docstring and something 
# went wrong with the error reporting, but now it's gone. 
# It should be somewhat similar to the `types`` module.
# ======================================================================

# ======================================================================
def abstract_class(*method_names: str):
    """
    Class decorator that converts a regular class into an ABC and marks
    the specified method names as abstract methods.

    ~To facilitate understanding, I have made an exception 
    to add usage examples for this function.~
    
    Example
    -------
    >>> @abstract_class('run', 'stop')
    ... class Worker:
    ...     def run(self): ...
    ...     def stop(self): ...
    >>> class MyWorker(Worker):
    ...     def run(self): print("running")
    ...     def stop(self): print("stopped")
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
# ======================================================================

# ======================================================================
class ABCException(Exception, metaclass=ABCMeta):
    """General Exception for ABC Scenarios."""

    def __init__(self, cls=None):
        self.cls = cls
        super().__init__(self._get_message())

    @abstractmethod
    def _get_message(self):
        """Return the error message. Must be implemented by subclasses."""
        pass

class ABCWarning(Warning, metaclass=ABCMeta):
    """General Warning for ABC Scenarios."""

    def __init__(self, cls=None):
        self.cls = cls
        super().__init__(self._get_message())

    @abstractmethod
    def _get_message(self):
        """Return the warning message. Must be implemented by subclasses."""
        pass
# ======================================================================