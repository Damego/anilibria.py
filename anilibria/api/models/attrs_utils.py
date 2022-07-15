from typing import Union, Tuple
from functools import wraps
from logging import getLogger

import attrs


__all__ = [
    "MISSING",
    "DictSerializer",
    "define",
    "field",
    "convert",
    "convert_list",
    "convert_playlist",
]
log = getLogger("anilibria.attrs")


class MISSING:
    ...


@attrs.define(eq=False, init=False)
class DictSerializer:
    def __init__(self, **kwargs):
        passed_kwargs = {}
        attribs: Tuple[attrs.Attribute, ...] = self.__attrs_attrs__

        for attrib in attribs:
            metadata = attrib.metadata
            attr_name = attrib.name
            if anilibria_name := metadata.get("anilibria_name"):
                name = anilibria_name
            else:
                name = attr_name
            value = kwargs.get(name, MISSING)
            if value != MISSING:
                del kwargs[name]
            passed_kwargs[attr_name] = value

        for kwarg in kwargs:
            log.debug(
                f"Attribute `{kwarg}` is missing from the `{self.__class__.__name__}` data model!"
            )

        self.__attrs_init__(**passed_kwargs)


define_defaults = dict(kw_only=True, eq=False, init=False)


@wraps(attrs.define)
def define(**kwargs):
    return attrs.define(**kwargs, **define_defaults)


@wraps(attrs.field)
def field(anilibria_name: str = None, **kwargs):
    metadata = {}
    if anilibria_name is not None:
        metadata["anilibria_name"] = anilibria_name

    return attrs.field(metadata=metadata, **kwargs)


def convert(obj):
    def wrapper(kwargs):
        if kwargs == "MISSING" or kwargs is MISSING:
            return MISSING
        if kwargs is None:
            return None
        return obj(**kwargs)

    return wrapper


def convert_list(obj):
    def wrapper(list):
        if list == "MISSING" or list is MISSING:
            return MISSING
        if list is None:
            return []
        return [obj(**_) for _ in list]

    return wrapper


def convert_playlist(obj):
    def wrapper(playlist: Union[dict, list]):
        if playlist == "MISSING" or playlist is MISSING:
            return MISSING
        if isinstance(playlist, list):
            return [obj(**_) for _ in playlist]
        else:
            return {key: obj(**value) for key, value in playlist.items()}

    return wrapper
