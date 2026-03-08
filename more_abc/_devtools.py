"""Tools that use in development mode."""

import logging

__all__ = [
    "get_abstract_methods",
    "is_abstract_class",
    "check_implementation",
    "missing_methods",
    "abstract_tree",
    "abc_logger",
    "SeeLogging",
    "ADM",
    "ADM_STANDARD",
    "ADM_DEBUG",
    "ADM_RELEASE",
    "set_adm",
]

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.CRITICAL)

abc_logger = _logger
"""
The module-level for ``more_abc.devtools``.

Its name is ``"more_abc.devtools"``, matching the Python package hierarchy,
so it can be configured independently of other loggers::

    logging.getLogger("more_abc.devtools").setLevel(logging.DEBUG)

By default the level is ``CRITICAL`` (silent). Set :data:`SeeLogging` to
``True`` to switch it to ``DEBUG``.
"""

SeeLogging = False
"""
Logging **toggle switch** for development tools.

If ``True``, the module logger (``more_abc.devtools``) is set to
``DEBUG`` level, so every call to the devtools functions is recorded.

If ``False`` (default), the logger level is ``CRITICAL``, effectively
silencing all output.
"""

if not isinstance(SeeLogging, bool):
    SeeLogging = False

if SeeLogging == True:
    abc_logger.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------
# ADM — Advanced Development Mode level constants
# ---------------------------------------------------------------------------

ADM_STANDARD      = 1
"""Standard Mode — normal operation, all logging silenced (``CRITICAL``)."""

ADM_DEBUG         = 2
"""Debug Mode    — verbose debug output enabled (``DEBUG``)."""

ADM_RELEASE       = 3
"""Release Mode  — production-like, only warnings and above (``WARNING``)."""

# Mapping from ADM level to Python logging level
_ADM_LOG_LEVELS = {
    ADM_STANDARD: logging.CRITICAL,
    ADM_DEBUG:    logging.DEBUG,
    ADM_RELEASE:  logging.WARNING,
}


class _ADMLevel(int):
    """Advanced Development Mode (ADM) level.

    An int subclass so ADM.__doc__ returns this text at runtime.
    Behaves identically to a plain int in every other respect.

    Controls how verbosely the more_abc.devtools logger reports activity.
    Use one of the ADM_* integer constants, or call set_adm() to change
    the level at runtime.
    """
    # Value  Constant      Logger level
    # -----  ------------  ------------
    # 1      ADM_STANDARD  CRITICAL
    # 2      ADM_DEBUG     DEBUG
    # 3      ADM_RELEASE   WARNING

    # NOTE: SeeLogging=True takes priority — the logger stays at DEBUG
    # regardless of the ADM level.
    
    __slots__ = ()


ADM = _ADMLevel(ADM_STANDARD)

if not isinstance(ADM, int) or int(ADM) not in _ADM_LOG_LEVELS:
    ADM = _ADMLevel(ADM_STANDARD)

# Apply ADM-based log level only when SeeLogging hasn't already forced DEBUG.
if not SeeLogging and ADM != ADM_STANDARD:
    abc_logger.setLevel(_ADM_LOG_LEVELS[int(ADM)])

def get_abstract_methods(cls):
    """
    Return the frozenset of abstract method names defined on *cls*.

    Works with any class, not just ABCMeta subclasses — returns an
    empty frozenset for concrete classes.

    Example::

        >>> from abc import ABC, abstractmethod
        >>> from more_abc import get_abstract_methods
        >>> class Base(ABC):
        ...     @abstractmethod
        ...     def run(self): ...
        >>> get_abstract_methods(Base)
        frozenset({'run'})
    """
    abc_logger.debug("get_abstract_methods(%r)", cls)
    result = frozenset(getattr(cls, "__abstractmethods__", frozenset()))
    abc_logger.debug("  -> %s", result)
    return result


def is_abstract_class(cls):
    """
    Return ``True`` if *cls* still has unimplemented abstract methods.

    A class is considered abstract when it has at least one name in
    ``__abstractmethods__``.

    Example::

        >>> from abc import ABC, abstractmethod
        >>> from more_abc import is_abstract_class
        >>> class Base(ABC):
        ...     @abstractmethod
        ...     def run(self): ...
        >>> is_abstract_class(Base)
        True
        >>> class Impl(Base):
        ...     def run(self): pass
        >>> is_abstract_class(Impl)
        False
    """
    abc_logger.debug("is_abstract_class(%r)", cls)
    result = bool(getattr(cls, "__abstractmethods__", None))
    abc_logger.debug("  -> %s", result)
    return result


def check_implementation(subclass, base):
    """
    Inspect how thoroughly *subclass* implements the abstract interface of
    *base*.

    Returns a dict with three keys:

    * ``"implemented"``  - methods that *subclass* has provided.
    * ``"missing"``      - abstract methods still not implemented.
    * ``"extra"``        - concrete methods on *subclass* that are **not**
      abstract in *base* (informational only).

    Example::

        >>> from more_abc import check_implementation
        >>> check_implementation(Impl, Base)
        {'implemented': frozenset({'run'}), 'missing': frozenset(), 'extra': ...}
    """
    abc_logger.debug("check_implementation(%r, %r)", subclass, base)
    base_abstracts = get_abstract_methods(base)
    sub_abstracts = get_abstract_methods(subclass)

    implemented = base_abstracts - sub_abstracts
    missing = base_abstracts & sub_abstracts

    sub_concrete = {
        name
        for name, val in vars(subclass).items()
        if callable(val) and not name.startswith("__")
    }
    extra = sub_concrete - base_abstracts

    if missing:
        abc_logger.warning(
            "%r missing %d method(s) from %r: %s",
            subclass.__name__, len(missing), base.__name__, missing,
        )
    else:
        abc_logger.debug("  %r fully implements %r", subclass.__name__, base.__name__)

    return {
        "implemented": frozenset(implemented),
        "missing":     frozenset(missing),
        "extra":       frozenset(extra),
    }


def missing_methods(subclass, base):
    """
    Return the set of abstract method names from *base* that *subclass*
    has **not** yet implemented.

    This is a convenience shorthand for
    ``check_implementation(subclass, base)["missing"]``.

    Example::

        >>> from more_abc import missing_methods
        >>> missing_methods(Impl, Base)
        frozenset()
    """
    abc_logger.debug("missing_methods(%r, %r)", subclass, base)
    return check_implementation(subclass, base)["missing"]


def abstract_tree(cls, *, _indent=0):
    """
    Print the MRO of *cls* annotated with each class's abstract methods.

    Useful for quickly spotting where abstract requirements originate in a
    deep inheritance hierarchy.

    Example output::

        MyClass  [abstract: set()]
          Base   [abstract: {'run', 'stop'}]
            ABC  [abstract: set()]
    """
    if _indent == 0:
        abc_logger.debug("abstract_tree(%r)", cls)
    abstract = get_abstract_methods(cls)
    prefix   = "  " * _indent
    print(f"{prefix}{cls.__name__}  [abstract: {set(abstract)}]")
    for base in cls.__bases__:
        if base is object:
            continue
        abstract_tree(base, _indent=_indent + 1)


def set_adm(mode):
    """Set the Advanced Development Mode level at runtime.

    Adjusts the ``more_abc.devtools`` logger level according to *mode*
    unless :data:`SeeLogging` is ``True`` (in which case the logger
    stays at ``DEBUG`` regardless).

    Example::

        >>> from more_abc.devtools import set_adm, ADM_DEBUG
        >>> set_adm(ADM_DEBUG)  # Enable verbose debug output at runtime
    """
    global ADM
    if mode not in _ADM_LOG_LEVELS:
        mode = ADM_STANDARD
    ADM = _ADMLevel(mode)          # preserve __doc__ after reassignment
    if not SeeLogging:
        abc_logger.setLevel(_ADM_LOG_LEVELS[mode])
    abc_logger.debug(
        "set_adm(%r): logger level -> %s", mode,
        logging.getLevelName(abc_logger.level),
    )
