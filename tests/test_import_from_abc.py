from more_abc import ABC, ABCMeta, abstractmethod, get_cache_token, update_abstractmethods
from abc import (ABC as ABC1,
                 ABCMeta as ABCMeta1,
                 abstractmethod as abstractmethod1,
                 get_cache_token as get_cache_token1,
                 update_abstractmethods as update_abstractmethods1)

def test_import_ABC() -> None:
    assert ABC == ABC1

def test_import_ABCMeta() -> None:
    assert ABCMeta == ABCMeta1

def test_import_abstractmethod() -> None:
    assert abstractmethod == abstractmethod1

def test_import_get_cache_token() -> None:
    assert get_cache_token == get_cache_token1

def test_import_update_abstractmethods() -> None:
    assert update_abstractmethods == update_abstractmethods1