# """Type stubs for more_abc.devtools."""

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

# ---------------------------------------------------------------------------
# Module-level data
# ---------------------------------------------------------------------------

abc_logger: logging.Logger

SeeLogging: bool

# ADM mode-level constants
ADM_STANDARD: int
ADM_DEBUG:    int
ADM_RELEASE:  int


class _ADMLevel(int):
    """Advanced Development Mode (ADM) level.

    Controls how verbosely the more_abc.devtools logger reports activity.
    Use one of the ADM_* integer constants, or call set_adm() to change
    the level at runtime.
    """
    # Value  Constant      Logger level
    # -----  ------------  ------------
    # 1      ADM_STANDARD  CRITICAL
    # 2      ADM_DEBUG     DEBUG
    # 3      ADM_RELEASE   WARNING

    # NOTE: SeeLogging=True takes priority -- the logger stays at DEBUG
    # regardless of the ADM level.

    __slots__ = ()


ADM: _ADMLevel

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def get_abstract_methods(cls: type) -> frozenset[str]:
    """Return the frozenset of abstract method names defined on *cls*."""
    ...

def is_abstract_class(cls: type) -> bool:
    """Return True if *cls* still has unimplemented abstract methods."""
    ...

def check_implementation(
    subclass: type,
    base: type,
) -> dict[str, frozenset[str]]:
    """Inspect how thoroughly *subclass* implements the abstract interface of *base*.

    Returns a dict with keys "implemented", "missing", "extra".
    """
    ...

def missing_methods(subclass: type, base: type) -> frozenset[str]:
    """Return abstract method names from *base* not yet implemented by *subclass*."""
    ...

def abstract_tree(cls: type, *, _indent: int = 0) -> None:
    """Print the MRO of *cls* annotated with each class's abstract methods."""
    ...

def set_adm(mode: int) -> None:
    """Set the Advanced Development Mode level at runtime."""
    ...
