"""This submodule is an extension of the ABC functionality within the `json` module."""

import abc
import json
from ._devtools import abc_logger

__all__ = [
    "AbstractJSONEncoder",
    "AbstractJSONDecoder",
]


class AbstractJSONEncoder(json.JSONEncoder, metaclass=abc.ABCMeta):
    """
    Abstract base class for JSON encoders, extending json.JSONEncoder.

    All custom JSON encoder implementations should subclass this to guarantee
    a consistent interface. Subclasses must implement `default`, `encode` and `iterencode`.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("AbstractJSONEncoder subclassed: %r", cls)

    @abc.abstractmethod
    def default(self, o):
        """
        Return a serializable object for *o*.
        """
        abc_logger.debug("%r.default(o=%r) called", self.__class__.__name__, o)
        raise NotImplementedError("Subclasses must implement default()")

    @abc.abstractmethod
    def encode(self, o):
        """
        Return a JSON string representation of *o*.
        """
        abc_logger.debug("%r.encode(o=%r) called", self.__class__.__name__, o)
        raise NotImplementedError("Subclasses must implement encode()")

    @abc.abstractmethod
    def iterencode(self, o, _one_shot=False):
        """
        Encode *o* and yield each string representation as available.
        """
        abc_logger.debug("%r.iterencode(o=%r, _one_shot=%r) called",
                         self.__class__.__name__, o, _one_shot)
        raise NotImplementedError("Subclasses must implement iterencode()")


class AbstractJSONDecoder(json.JSONDecoder, metaclass=abc.ABCMeta):
    """
    Abstract base class for JSON decoders, extending json.JSONDecoder.

    All custom JSON decoder implementations should subclass this to guarantee
    a consistent interface. Subclasses must implement `decode` and `raw_decode`.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        abc_logger.debug("AbstractJSONDecoder subclassed: %r", cls)

    @abc.abstractmethod
    def decode(self, s): # type: ignore
        """
        Return the Python representation of *s*.
        """
        abc_logger.debug("%r.decode(s=%r) called", self.__class__.__name__, s)
        raise NotImplementedError("Subclasses must implement decode()")

    @abc.abstractmethod
    def raw_decode(self, s, idx=0):
        """
        Decode a JSON document from *s* starting at index *idx*.
        """
        abc_logger.debug("%r.raw_decode(s=%r, idx=%r) called",
                         self.__class__.__name__, s, idx)
        raise NotImplementedError("Subclasses must implement raw_decode()")
