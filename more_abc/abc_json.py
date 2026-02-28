"""This submodule is an extension of the ABC functionality within the `json` module."""

import abc
import json

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

    @abc.abstractmethod
    def default(self, o):
        """
        Return a serializable object for *o*.
        """
        raise NotImplementedError("Subclasses must implement default()")
    
    @abc.abstractmethod
    def encode(self, o):
        """
        Return a JSON string representation of *o*.
        """
        raise NotImplementedError("Subclasses must implement encode()")

    @abc.abstractmethod
    def iterencode(self, o, _one_shot=False):
        """
        Encode *o* and yield each string representation as available.
        """
        raise NotImplementedError("Subclasses must implement iterencode()")



class AbstractJSONDecoder(json.JSONDecoder, metaclass=abc.ABCMeta):
    """
    Abstract base class for JSON decoders, extending json.JSONDecoder.

    All custom JSON decoder implementations should subclass this to guarantee
    a consistent interface. Subclasses must implement `decode` and `raw_decode`.
    """

    @abc.abstractmethod
    def decode(self, s): # type: ignore
        """
        Return the Python representation of *s*.
        """
        raise NotImplementedError("Subclasses must implement decode()")

    @abc.abstractmethod
    def raw_decode(self, s, idx=0):
        """
        Decode a JSON document from *s* starting at index *idx*.
        """
        raise NotImplementedError("Subclasses must implement raw_decode()")
