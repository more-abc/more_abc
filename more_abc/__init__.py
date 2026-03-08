# Copyright (C) 2026 Evan Yang <quantbit@126.com>

# GNU GENERAL PUBLIC LICENSE (Version 3)

# This module refers to PEP 3119.
# See https://peps.python.org/pep-3119/ or https://legacy.python.org/dev/peps/pep-3119/

"""
more_abc — an extension of the :mod:`abc` and :mod:`collections.abc` modules.

Provides abstract base classes, decorators, and utilities for defining
clean abstract interfaces in Python.

Core helpers:
    ABCMixin              -- ABC mixin with abstract `initialize` / `validate` / `to_dict` / `is_valid` / `get_info`

    ABCclassType          -- type alias of ABC

    ABCMetaclassType      -- type alias of ABCMeta

    ABCException          -- abstract base for custom exceptions

    ABCWarning            -- abstract base for custom warnings


Decorators:
    abstract_class        -- class decorator: turns a plain class into an ABC with named abstract methods

    abstractproperty      -- decorator: defines a read-only or read-write abstract property

    abstract_lru_cache    -- decorator: combines `@lru_cache` with `@abstractmethod`

    abstractdataclass     -- decorator: combines `@dataclass` with `ABCMeta`


Enum ABCs:
    ABCEnumMeta           -- combined ABCMeta + EnumMeta metaclass

    ABCEnum               -- Enum base class with abstract-method support

    ABCIntEnum            -- IntEnum base class with abstract-method support

    ABCFlag               -- Flag base class with abstract-method support

    ABCIntFlag            -- IntFlag base class with abstract-method support

Logging ABCs:
    AbstractLogHandler    -- abstract base for `logging.Handler`

    AbstractLogFormatter  -- abstract base for `logging.Formatter`

    AbstractLogFilter     -- abstract base for `logging.Filter`

I/O ABCs:
    AbstractRawIO         -- abstract base for `io.RawIOBase`

    AbstractBufferedIO    -- abstract base for `io.BufferedIOBase`

    AbstractTextIO        -- abstract base for `io.TextIOBase`

JSON ABCs:
    AbstractJSONEncoder   -- abstract base for `json.JSONEncoder`

    AbstractJSONDecoder   -- abstract base for `json.JSONDecoder`

Collections ABCs:
    BaseSortable          -- minimal abstract interface: `__sort__`

    SortableMixin         -- concrete helpers: `sort()`, `sorted()`

    Sortable              -- final ABC = BaseSortable + SortableMixin

    BaseFilterable        -- minimal abstract interface: `__filter__`

    FilterableMixin       -- concrete helpers: `filter()`, `reject()`

    Filterable            -- final ABC = BaseFilterable + FilterableMixin

    BaseTransformable     -- minimal abstract interface: `__transform__`

    TransformableMixin    -- concrete helper: `map()`

    Transformable         -- final ABC = BaseTransformable + TransformableMixin

Re-exported from `abc` module:
    ABC, ABCMeta, abstractmethod, get_cache_token, update_abstractmethods

Defined here (compatible with all supported Python versions):
    abstractasyncmethod   -- `@abstractmethod` for `async def` methods
"""

import sys
import abc
from abc import (ABC,
                 ABCMeta,
                 abstractmethod,
                 get_cache_token, 
                 update_abstractmethods)

# Do you know why there are still many other extensions 
# in my code even though there is clearly a `more.py` file?
from .more import (ABCMixin,
                   ABCclassType,
                   ABCMetaclassType,
                   ABCException,
                   ABCWarning)  
from .decorator import (abstract_class, abstractproperty, abstract_lru_cache)
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
from . import _devtools
from ._devtools import abc_logger

abc_logger.debug("more_abc.__init__: starting import")

if sys.version_info >= (3, 14):
    import annotationlib

_DevMode_func = _devtools.__all__

__all__ = ["ABCMixin",
           "ABCclassType",
           "ABCMetaclassType",
           "ABCException",
           "ABCWarning",
           "abstract_class",
           "abstractproperty",
           "abstract_lru_cache",
           "abstractasyncmethod",
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
           # Development mode toggle switch   
           "DevMode"]

__version__ = "2.2.9"
__version_tuple__ = (2, 2, 9)
__int_version__ = 46
__author__ = "Evan Yang <quantbit@126.com>"
__license__ = "GPL-3.0"
# Can be development / stable / deprecated
__status__ = "stable"

__title__ = "more_abc"
# more_abc™
__description__ = "extension of the `abc` and `collections.abc` module"

DevMode = False
"""
Development mode **toggle switch**.

If True, you can use and import the function 
that only can use in development mode.
"""
if not isinstance(DevMode, bool):
    DevMode = False

if DevMode == True:
    abc_logger.debug("DevMode is enabled")
    __all__.append(_DevMode_func) # type: ignore
else:
    abc_logger.debug("DevMode is disabled")

if sys.version_info >= (3, 4):
    ABC = abc.ABC
    get_cache_token = abc.get_cache_token
    abc_logger.debug("ABC, get_cache_token: using stdlib (Python >= 3.4)")
else:
    abc_logger.debug("ABC, get_cache_token: using compat shim (Python < 3.4)")
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
        abc_logger.debug("get_cache_token() called (compat shim)")
        result = abc.ABCMeta._abc_invalidation_counter
        abc_logger.debug("  -> %r", result)
        return result
    
if sys.version_info >= (3, 10):
    update_abstractmethods = abc.update_abstractmethods
    abc_logger.debug("update_abstractmethods: using stdlib (Python >= 3.10)")
else:
    abc_logger.debug("update_abstractmethods: using compat shim (Python < 3.10)")
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
        abc_logger.debug("update_abstractmethods(%r)", cls)
        if not hasattr(cls, '__abstractmethods__'):
            abc_logger.debug("  %r has no __abstractmethods__, skipping", cls)
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
        abc_logger.debug("  %r updated __abstractmethods__: %s", cls, cls.__abstractmethods__)
        return cls

if sys.version_info >= (3, 10):
    abc_logger.debug("abstractasyncmethod: using stdlib wrapper (Python >= 3.10)")
    def abstractasyncmethod(func):
        """
        A decorator indicating an abstract async method.

        Works like `abc.abstractmethod`, but for async methods.
        """
        abc_logger.debug("abstractasyncmethod(%r)", func)
        result = abc.abstractmethod(func)
        abc_logger.debug("  -> %r", result)
        return result
else:
    abc_logger.debug("abstractasyncmethod: using compat shim (Python < 3.10)")
    def abstractasyncmethod(func):
        """
        A decorator indicating an abstract async method.

        Works like `abc.abstractmethod`, but for async methods.
        """
        abc_logger.debug("abstractasyncmethod(%r) [compat shim]", func)
        if func is None:
            return abstractasyncmethod  # Support @abstractasyncmethod (no args)

        func = abstractmethod(func)

        setattr(func, "__is_async_abstract__", True)

        if func.__doc__ is None:
            func.__doc__ = "Async abstract method (must implement with async def)"

        abc_logger.debug("  -> %r", func)
        return func