from enum import Enum

from .typings import MISSING

__all__ = ("dict_filter_none", "dict_filter_missing", "prepare_payload")


def dict_filter_none(**kwargs) -> dict:
    return {key: value for key, value in kwargs.items() if value is not None}


def dict_filter_missing(data: dict = None, /, **kwargs):
    _data: dict = data or kwargs

    return {key: value for key, value in _data.items() if value is not MISSING}


def prepare_payload(data: dict):
    for key, value in data.items():
        if isinstance(value, list):
            data[key] = ",".join(str(_) for _ in value)
        elif isinstance(value, Enum):
            data[key] = value.value
