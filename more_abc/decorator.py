"""This submodule is an extension of the ABC **decoratorality**."""

from abc import abstractmethod, ABCMeta
from functools import lru_cache, wraps
from ._devtools import abc_logger

__all__ = [
    "abstract_class",
    "abstractproperty",
    "abstract_lru_cache"
]

#  To facilitate understanding, I have made an exception
# to add usage examples for this function.

# Example:
# @abstract_class('run', 'stop')
# class Worker:
#     def run(self): ...
#     def stop(self): ...

# class MyWorker(Worker):
#     def run(self):
#         print("running")
#     def stop(self):
#         print("stopped")

def abstract_class(*method_names):
    """
    Class decorator that converts a regular class into an ABC and marks
    the specified method names as abstract methods.
    """
    if not method_names:
        abc_logger.warning(
            "abstract_class() called with no method names — "
            "the resulting ABC will have no abstract methods"
        )
    else:
        abc_logger.debug("abstract_class%r", method_names)

    def decorator(cls):
        abc_logger.debug("abstract_class: decorating %r", cls)
        namespace = {}
        for key, value in vars(cls).items():
            if key in ('__dict__', '__weakref__'):
                continue
            if key in method_names and callable(value):
                namespace[key] = abstractmethod(value)
                abc_logger.debug("  marked %r as abstractmethod", key)
            else:
                namespace[key] = value

        for name in method_names:
            if name not in namespace:
                abc_logger.warning(
                    "abstract_class: %r has no method %r — "
                    "injecting an empty stub as abstractmethod",
                    cls.__name__, name,
                )
                def _stub(self):
                    pass
                _stub.__name__ = name
                _stub.__qualname__ = f"{cls.__qualname__}.{name}"
                namespace[name] = abstractmethod(_stub)

        try:
            new_cls = ABCMeta(cls.__name__, cls.__bases__, namespace)
            new_cls.__qualname__ = cls.__qualname__
            new_cls.__module__ = cls.__module__
        except Exception as exc:
            abc_logger.critical(
                "abstract_class: failed to construct ABCMeta for %r: %s",
                cls.__name__, exc, exc_info=True,
            )
            raise

        abc_logger.info(
            "abstract_class: %r converted to ABC  (abstract methods: %r)",
            cls.__name__, list(method_names),
        )
        return new_cls

    return decorator

def abstractproperty(read_only=True):
    """
    Enhanced replacement for the deprecated ``abc.abstractproperty``.

    Defines an abstract property on an ABC. Subclasses must provide a
    concrete ``@property`` implementation. When *read_only* is ``False``,
    subclasses must also implement a setter.
    """
    abc_logger.debug("abstractproperty(read_only=%r)", read_only)
    if not read_only:
        abc_logger.warning(
            "abstractproperty(read_only=False): subclasses must implement "
            "both a getter and a setter"
        )

    def decorator(func):
        abc_logger.debug("abstractproperty: wrapping %r", func)
        prop = property(abstract_func := abstractmethod(func))
        prop.__is_abstract_property__ = True  # type: ignore[attr-defined]
        prop.__abstract_read_only__ = read_only  # type: ignore[attr-defined]

        if not read_only:
            original_setter = prop.setter

            def setter(fset):
                abstract_fset = abstractmethod(fset)
                return original_setter(abstract_fset)

            prop = prop.__class__(
                prop.fget,
                prop.fset,
                prop.fdel,
                prop.__doc__,
            )
            prop.setter = setter  # type: ignore[method-assign]

        abc_logger.info(
            "abstractproperty: created %s abstract property %r",
            "read-only" if read_only else "read-write",
            func.__qualname__,
        )
        return prop

    return decorator

def abstract_lru_cache(maxsize=128, typed=False):
    """Decorator that combines :func:`functools.lru_cache` with :func:`~abc.abstractmethod`.

    The decorated method is marked abstract, so subclasses must override it.
    The overriding implementation is **not** automatically cached — the cache
    is attached to this descriptor and is shared across all callers that hit
    the same argument signature.

    Exposes :attr:`cache_info` and :attr:`cache_clear` on the returned
    wrapper, forwarded directly from the underlying
    :func:`~functools.lru_cache` object.
    """
    abc_logger.debug("abstract_lru_cache(maxsize=%r, typed=%r)", maxsize, typed)
    if maxsize is None:
        abc_logger.warning(
            "abstract_lru_cache: maxsize=None — "
            "cache is unbounded and may grow without limit"
        )
    if typed:
        abc_logger.info(
            "abstract_lru_cache: typed=True — "
            "arguments of different types are cached separately"
        )

    def decorator(func):
        abc_logger.debug("abstract_lru_cache: wrapping %r", func)
        try:
            cached_func = lru_cache(maxsize=maxsize, typed=typed)(func)
        except Exception as exc:
            abc_logger.error(
                "abstract_lru_cache: lru_cache() failed for %r: %s",
                func, exc, exc_info=True,
            )
            raise

        abstract_cached_func = abstractmethod(cached_func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return abstract_cached_func(*args, **kwargs)

        wrapper.cache_info = cached_func.cache_info # type: ignore
        wrapper.cache_clear = cached_func.cache_clear # type: ignore

        abc_logger.info(
            "abstract_lru_cache: wrapped %r  (maxsize=%r, typed=%r)",
            func.__qualname__, maxsize, typed,
        )
        return wrapper
    return decorator
