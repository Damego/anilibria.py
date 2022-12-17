from typing import ClassVar, TypeVar

__all__ = ("T", "MISSING", "Absent")

T = TypeVar("T")


class _Missing:
    _instance: ClassVar["_Missing"] = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __eq__(self, other):
        return self.__class__ is other.__class__

    def __repr__(self):
        return "<anilibria.MISSING>"

    def __hash__(self):
        return 0

    def __bool__(self):
        return False


MISSING = _Missing()
Absent = T | _Missing
