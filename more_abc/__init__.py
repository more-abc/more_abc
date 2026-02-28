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
    ABC, ABCMeta, abstractmethod, get_cache_token
"""

import sys
import abc
from abc import (ABC,
                 ABCMeta,
                 abstractmethod,
                 get_cache_token)  # `get_cache_token`? What it this?

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
            # version of `more_abc` module
           "version"]

__version__ = "2.1.10"
__author__ = "Evan Yang <quantbit@126.com>"
__license__ = "GPL-3.0"
# Can be development / stable / deprecated
__status__ = "stable"

__title__ = "more_abc"
# more_abc™
__description__ = "extension of the `abc` and `collections.abc` module"

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