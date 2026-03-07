import sys
import abc
from abc import (ABC as ABC,
                 ABCMeta as ABCMeta,
                 abstractmethod as abstractmethod,
                 get_cache_token as get_cache_token,
                 update_abstractmethods as update_abstractmethods)
from .more import (ABCMixin,
                   ABCclassType,
                   ABCMetaclassType,
                   ABCException,
                   ABCWarning)
from .decorator import abstract_class, abstractproperty
from .abc_dataclasses import abstractdataclass
from .abc_enum import ABCEnumMeta, ABCEnum, ABCIntEnum, ABCFlag, ABCIntFlag
from .abc_loogging import AbstractLogFilter, AbstractLogFormatter, AbstractLogHandler
from .abc_io import AbstractBufferedIO, AbstractRawIO, AbstractTextIO
from .abc_json import AbstractJSONDecoder, AbstractJSONEncoder
from .collections_abc import (BaseSortable, 
                              SortableMixin, 
                              Sortable,
                              BaseFilterable, 
                              FilterableMixin, 
                              Filterable,
                              BaseTransformable, 
                              TransformableMixin,
                              Transformable)

__all__ = ["ABCMixin",
           "ABCclassType",
           "ABCMetaclassType",
           "ABCException",
           "ABCWarning",
           "abstract_class",
           "abstractproperty",
           "abstractdataclass",
           "ABCEnumMeta",
           "ABCEnum",
           "ABCIntEnum",
           "ABCFlag",
           "ABCIntFlag",
           "AbstractLogFilter",
           "AbstractLogFormatter",
           "AbstractLogHandler",
           "AbstractRawIO",
           "AbstractBufferedIO",
           "AbstractTextIO",
           "AbstractJSONEncoder",
           "AbstractJSONDecoder",
           # collections_abc
           "BaseSortable", 
           "SortableMixin", 
           "Sortable",
           "BaseFilterable", 
           "FilterableMixin", 
           "Filterable",
           "BaseTransformable", 
           "TransformableMixin", 
           "Transformable",
           # re-exported from abc
           "ABC",
           "ABCMeta",
           "abstractmethod",
           "get_cache_token",
           "update_abstractmethods",
            # re-exported from old typing_extensions
           "abstractasyncmethod",
           "DevMode"] 

__author__: str
__license__: str
__status__: str
__title__: str
__description__: str
__version__: str
DevMode: bool

if sys.version_info >= (3, 4):
    ABC = abc.ABC
    get_cache_token = abc.get_cache_token
else:
    class ABC(metaclass=ABCMeta):
        """
        Helper class that provides a standard way to create an ABC using
        inheritance.
        """
        __slots__ = ()

    def get_cache_token():
        """
        Returns the current ABC cache token.

        token is an opaque object (supporting equality testing) identifying the
        current version of the ABC cache for virtual subclasses. The token changes
        with every call to ``register()`` on any ABC.
        """
        return abc.ABCMeta._abc_invalidation_counter
    
if sys.version_info >= (3, 10):
    update_abstractmethods = abc.update_abstractmethods
else:
    def update_abstractmethods(cls):
        """
        Recalculate the set of abstract methods of an abstract class.
        If a class has had one of its abstract methods implemented after the
        class was created, the method will not be considered implemented until
        this function is called. Alternatively, if a new abstract method has been
        added to the class, it will only be considered an abstract method of the
        class after this function is called.

        This function should be called before any use is made of the class,
        usually in class decorators that add methods to the subject class.

        Returns cls, to allow usage as a class decorator.

        If cls is not an instance of ABCMeta, does nothing.
        """
        if not hasattr(cls, '__abstractmethods__'):
            return cls

        abstracts = set()
        for scls in cls.__bases__:
            for name in getattr(scls, '__abstractmethods__', ()):
                value = getattr(cls, name, None)
                if getattr(value, "__isabstractmethod__", False):
                    abstracts.add(name)

        for name, value in cls.__dict__.items():
            if getattr(value, "__isabstractmethod__", False):
                abstracts.add(name)
        cls.__abstractmethods__ = frozenset(abstracts)
        return cls

if sys.version_info >= (3, 10):
    def abstractasyncmethod(func):
        """    
        A decorator indicating an abstract async method.

        Works like `abc.abstractmethod`, but for async methods.
        """
        return abc.abstractmethod(func)
else:
    def abstractasyncmethod(func):
        """        
        A decorator indicating an abstract async method.

        Works like `abc.abstractmethod`, but for async methods.
        """
        if func is None:
            return abstractasyncmethod  # Support @abstractasyncmethod (no args)
        
        func = abstractmethod(func)

        setattr(func, "__is_async_abstract__", True)

        if func.__doc__ is None:
            func.__doc__ = "Async abstract method (must implement with async def)"
        
        return func