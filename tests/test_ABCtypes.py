from more_abc import ABCclassType, ABCMetaclassType

def test_ABCclassType() -> None:
    assert type(ABCclassType) == type

def test_ABCMetaclassType() -> None:
    assert type(ABCMetaclassType) == type