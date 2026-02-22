# Copyright (C) 2026 Evan Yang <quantbit@126.com>

# MIT License

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This module refers to PEP 3119.
# See https://peps.python.org/pep-3119/ or https://legacy.python.org/dev/peps/pep-3119/
"""
This module is an extension of the `abc` module,
with many similar features added.

Public symbols
--------------
From this package:
    ABCMixin          -- ABC mixin with abstract initialize/validate/to_dict
    ABCclassType      -- type alias: type(ABC)
    ABCMetaclassType  -- type alias: type(ABCMeta)
    ABCException      -- abstract base for custom exceptions
    ABCWarning        -- abstract base for custom warnings
    abc_dataclass     -- @dataclass + ABCMeta combined decorator
    ABCEnumMeta       -- combined ABCMeta + EnumMeta metaclass
    AbcEnum           -- Enum base class with abstract-method support

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
from .abc_enum import ABCEnumMeta, AbcEnum

__all__ = ["ABCMixin",
           "ABCclassType",
           "ABCMetaclassType",
           "ABCException",
           "ABCWarning",
           "abc_dataclass",
           "ABCEnumMeta",
           "AbcEnum",
           # re-exported from abc
           "ABC",
           "ABCMeta",
           "abstractmethod",
           "abstractproperty",
           "get_cache_token",
           "version"]

__version__ = "0.2.4"
version = __version__

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
