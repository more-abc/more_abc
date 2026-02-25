# Copyright (C) 2026 Evan Yang <quantbit@126.com>

# This module refers to PEP 3119.
# See https://peps.python.org/pep-3119/ or https://legacy.python.org/dev/peps/pep-3119/
"""
This module is an extension of the `abc` module,
with many similar features added.

Public symbols
--------------
From this package:
    ABCMixin              -- ABC mixin with abstract initialize/validate/to_dict
    ABCclassType          -- type alias: type(ABC)
    ABCMetaclassType      -- type alias: type(ABCMeta)
    ABCException          -- abstract base for custom exceptions
    ABCWarning            -- abstract base for custom warnings
    abc_dataclass         -- @dataclass + ABCMeta combined decorator
    
    ABCEnumMeta           -- combined ABCMeta + EnumMeta metaclass
    AbcEnum               -- Enum base class with abstract-method support
    AbcIntEnum            -- IntEnum base class with abstract-method support
    AbcFlag               -- Flag base class with abstract-method support
    AbcIntFlag            -- IntFlag base class with abstract-method support

    AbstractLogHandler    -- abstract base for logging.Handler
    AbstractLogFormatter  -- abstract base for logging.Formatter
    AbstractLogFilter     -- abstract base for logging.Filter

    AbstractRawIO         -- abstract base for io.RawIOBase
    AbstractBufferedIO    -- abstract base for io.BufferedIOBase
    AbstractTextIO        -- abstract base for io.TextIOBase

    BaseSortable          -- minimal abstract interface for sortable containers
    SortableMixin         -- concrete sort()/sorted() helpers
    Sortable              -- final ABC combining BaseSortable + SortableMixin
    BaseFilterable        -- minimal abstract interface for filterable containers
    FilterableMixin       -- concrete filter()/reject() helpers
    Filterable            -- final ABC combining BaseFilterable + FilterableMixin
    BaseTransformable     -- minimal abstract interface for transformable containers
    TransformableMixin    -- concrete map() helper
    Transformable         -- final ABC combining BaseTransformable + TransformableMixin

Re-exported from :mod:`abc`:
    ABC, ABCMeta, abstractmethod, abstractproperty, get_cache_token
"""

import sys
import abc
from abc import (ABC,
                 ABCMeta,
                 abstractmethod,
                 abstractproperty,
                 get_cache_token)

from .more import (ABCMixin,
                   ABCclassType,
                   ABCMetaclassType,
                   ABCException,
                   ABCWarning)
from .abc_dataclasses import abc_dataclass
from .abc_enum import ABCEnumMeta, AbcEnum, AbcIntEnum, AbcFlag, AbcIntFlag
from .abc_loogging import AbstractLogFilter, AbstractLogFormatter, AbstractLogHandler
from .abc_io import AbstractBufferedIO, AbstractRawIO, AbstractTextIO
from .collections_abc import (BaseSortable, SortableMixin, Sortable,
                               BaseFilterable, FilterableMixin, Filterable,
                               BaseTransformable, TransformableMixin, Transformable)
# from ._read_last_version import _check_mod_version

__all__ = ["ABCMixin",
           "ABCclassType",
           "ABCMetaclassType",
           "ABCException",
           "ABCWarning",
           "abc_dataclass",
           "ABCEnumMeta",
           "AbcEnum",
           "AbcIntEnum",
           "AbcFlag",
           "AbcIntFlag",
           "AbstractLogFilter",
           "AbstractLogFormatter",
           "AbstractLogHandler",
            "AbstractRawIO",
            "AbstractBufferedIO",
            "AbstractTextIO",
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
           "abstractproperty",
           "get_cache_token",
            # version of `more_abc` module
           "version"]

__version__ = "2.0.5"
__author__ = "Evan Yang <quantbit@126.com>"
__license__ = "MIT"
# Can be development / stable / deprecated
__status__ = "stable"

version = __version__
"""version of `more_abc` module."""

# Wrapper of the abc module that is compatible with Python
PY_VERSION = sys.version_info[:2]

class ABCCompat(object):
    """Compatibility shim that mirrors all public symbols from :mod:`abc`.

    All non-underscore attributes of the standard :mod:`abc` module are copied
    onto this class, then injected into the ``more_abc`` namespace via
    ``sys.modules``.  This lets users import everything ABC-related from a
    single package.
    """

for attr in dir(abc):
    if not attr.startswith('_'):
        setattr(ABCCompat, attr, getattr(abc, attr))

if PY_VERSION >= (3, 4):
    ABCCompat.ABC = abc.ABC # type: ignore
else:
    ABCCompat.ABC = abc.ABC # type: ignore

sys.modules[__name__].__dict__.update(ABCCompat.__dict__)

# _check_mod_version()