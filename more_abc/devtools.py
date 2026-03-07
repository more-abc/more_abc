"""Tools that use in development mode."""

import logging

__all__ = [
    "get_abstract_methods",
    "is_abstract_class",
    "check_implementation",
    "missing_methods",
    "abstract_tree",
    "abc_logger",
    "SeeLogging"
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

def get_abstract_methods(cls):

    """
    Return the frozenset of abstract method names defined on *cls*.

    Works with any class, not just ABCMeta subclasses — returns an
    empty frozenset for concrete classes.

    Example::

        >>> from abc import ABC, abstractmethod
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
