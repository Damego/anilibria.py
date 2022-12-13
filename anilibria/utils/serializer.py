__all__ = ["dict_filter_none"]


def dict_filter_none(**kwargs) -> dict:
    return {key: value for key, value in kwargs.items() if value is not None}
