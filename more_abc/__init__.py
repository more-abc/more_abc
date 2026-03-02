# Copyright (C) 2026 Evan Yang <quantbit@126.com>

# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007

# Copyright (C) [2026] [aiwonderland/more-abc]

# This module refers to PEP 3119.
# See https://peps.python.org/pep-3119/ or https://legacy.python.org/dev/peps/pep-3119/

"""
This module is an extension of the `abc` and `collections.abc` module,
with many similar features added.

Public symbols
--------------
From this package:
    ABCMixin              -- ABC mixin with abstract initialize/validate/to_dict
    ABCclassType          -- type alias: type(ABC)
    ABCMetaclassType      -- type alias: type(ABCMeta)
    ABCException          -- abstract base for custom exceptions
    ABCWarning            -- abstract base for custom warnings
    abstract_class        -- decorator that turns a class into an ABC with specified abstract methods
    abstractproperty      -- decorator that defines an abstract property (read-only or read-write)
    abstractdataclass     -- @dataclass + ABCMeta combined decorator
    
    ABCEnumMeta           -- combined ABCMeta + EnumMeta metaclass
    ABCEnum               -- Enum base class with abstract-method support
    ABCIntEnum            -- IntEnum base class with abstract-method support
    ABCFlag               -- Flag base class with abstract-method support
    ABCIntFlag            -- IntFlag base class with abstract-method support

    AbstractLogHandler    -- abstract base for logging.Handler
    AbstractLogFormatter  -- abstract base for logging.Formatter
    AbstractLogFilter     -- abstract base for logging.Filter

    AbstractRawIO         -- abstract base for io.RawIOBase
    AbstractBufferedIO    -- abstract base for io.BufferedIOBase
    AbstractTextIO        -- abstract base for io.TextIOBase

    AbstractJSONDecoder   -- abstract base for json.JSONDecoder
    AbstractJSONEncoder   -- abstract base for json.JSONEncoder

    BaseSortable          -- minimal abstract interface for sortable containers
    SortableMixin         -- concrete sort()/sorted() helpers
    Sortable              -- final ABC combining BaseSortable + SortableMixin
    BaseFilterable        -- minimal abstract interface for filterable containers
    FilterableMixin       -- concrete filter()/reject() helpers
    Filterable            -- final ABC combining BaseFilterable + FilterableMixin
    BaseTransformable     -- minimal abstract interface for transformable containers
    TransformableMixin    -- concrete map() helper
    Transformable         -- final ABC combining BaseTransformable + TransformableMixin

Re-exported from `abc` module:
    ABC, ABCMeta, abstractmethod, get_cache_token, update_abstractmethods
from `typing_extensions` module (version < 4.0):
    abstractasyncmethod

"""

import sys
import abc
from abc import (ABC,
                 ABCMeta,
                 abstractmethod,
                 get_cache_token, 
                 update_abstractmethods)  # A new thing

# Do you know why there are still many other extensions 
# in my code even though there is clearly a `more.py` file?
from .more import (ABCMixin,
                   ABCclassType,
                   ABCMetaclassType,
                   ABCException,
                   ABCWarning,
                   abstract_class,
                   abstractproperty)  # New one
from .abc_dataclasses import abstractdataclass

# It is unclear whether the code contained 
# in this file overlaps with that of other developers.
from .abc_enum import (ABCEnumMeta, 
                       ABCEnum, 
                       ABCIntEnum, 
                       ABCFlag, 
                       ABCIntFlag)
from .abc_loogging import (AbstractLogFilter, 
                           AbstractLogFormatter, 
                           AbstractLogHandler)
from .abc_io import (AbstractBufferedIO, 
                     AbstractRawIO, 
                     AbstractTextIO)
from .abc_json import (AbstractJSONDecoder,
                       AbstractJSONEncoder)
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
           "abstractasyncmethod"]

__version__ = "2.2.2"
__author__ = "Evan Yang <quantbit@126.com>"
__license__ = "GPL-3.0"
# Can be development / stable / deprecated
__status__ = "stable"

__title__ = "more_abc"
# more_abc™
__description__ = "extension of the `abc` and `collections.abc` module"


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
    abstractasyncmethod = abc.abstractmethod
    abstractasyncmethod.__doc__ = f"""
    A decorator indicating an abstract async method.

    Works like `abc.abstractmethod`, but for async methods.
"""
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