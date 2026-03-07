"""Core functions (And `types` module like) of the module are contained in this file."""

#                              __
#   __ _  ___  _______   ___ _/ /  ____
#  /  ' \/ _ \/ __/ -_) / _ `/ _ \/ __/
# /_/_/_/\___/_/  \__/__\_,_/_.__/\__/
#                   /___/

from abc import ABC, ABCMeta, abstractmethod
from .devtools import abc_logger

__all__ = ["ABCMixin",
           "ABCclassType",
           "ABCMetaclassType",
           "ABCException",
           "ABCWarning"]

# All the ABC classes.
# ======================================================================
class ABCMixin(metaclass=ABCMeta):
    """
    A comprehensive ABC Mixin class that provides abstract method patterns
    and utility methods for subclasses.

    This mixin enforces implementation of core methods while providing
    common functionality that works with those abstract methods.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("ABCMixin subclassed: %r", cls)

    @abstractmethod
    def initialize(self):
        """Initialize the instance. Must be implemented by subclasses."""
        abc_logger.debug("%r.initialize() called", self.__class__.__name__)

    @abstractmethod
    def validate(self):
        """Validate the instance state. Must be implemented by subclasses."""
        abc_logger.debug("%r.validate() called", self.__class__.__name__)

    @abstractmethod
    def to_dict(self):
        """Convert instance to dictionary. Must be implemented by subclasses."""
        abc_logger.debug("%r.to_dict() called", self.__class__.__name__)

    def is_valid(self):
        """
        Check if the instance is valid.
        Concrete method that uses the abstract validate method.
        """
        abc_logger.debug("%r.is_valid() called", self.__class__.__name__)
        try:
            result = self.validate()
            abc_logger.debug("  -> %r", result)
            return result
        except Exception as e:
            abc_logger.debug("  validate() raised %r, returning False", e)
            return False

    def get_info(self):
        """
        Get instance information including validation status.
        Concrete method that combines abstract methods.
        """
        abc_logger.debug("%r.get_info() called", self.__class__.__name__)
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
# It should be somewhat similar to the `types` module.

# ======================================================================
class ABCException(Exception, metaclass=ABCMeta):
    """General Exception for ABC Scenarios."""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("ABCException subclassed: %r", cls)

    def __init__(self, cls=None):
        abc_logger.debug("%r.__init__(cls=%r)", self.__class__.__name__, cls)
        self.cls = cls
        super().__init__(self.get_message())

    @abstractmethod
    def get_message(self):
        """Return the error message. Must be implemented by subclasses."""
        abc_logger.debug("%r.get_message() called", self.__class__.__name__)

class ABCWarning(Warning, metaclass=ABCMeta):
    """General Warning for ABC Scenarios."""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("ABCWarning subclassed: %r", cls)

    def __init__(self, cls=None):
        abc_logger.debug("%r.__init__(cls=%r)", self.__class__.__name__, cls)
        self.cls = cls
        super().__init__(self.get_message())

    @abstractmethod
    def get_message(self):
        """Return the warning message. Must be implemented by subclasses."""
        abc_logger.debug("%r.get_message() called", self.__class__.__name__)
# ======================================================================