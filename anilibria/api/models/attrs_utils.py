from typing import Union, Tuple
from functools import wraps
from logging import getLogger

import attrs


__all__ = ["DictSerializer", "define", "field", "convert", "convert_list", "convert_playlist"]
log = getLogger("anilibria.attrs")


@attrs.define(eq=False, init=False)
class DictSerializer:
    def __init__(self, **kwargs):
        passed_kwargs: dict = {}
        attribs: Tuple[attrs.Attribute, ...] = self.__attrs_attrs__

        for kwarg in kwargs:
            if kwarg not in self.__slots__:
                log.debug(f"Attribute `{kwarg}` is missing from the `{self.__class__.__name__}` data model!")

        for attrib in attribs:
            metadata = attrib.metadata
            attr_name = attrib.name
            if anilibria_name := metadata.get("anilibria_name"):
                passed_kwargs[attr_name] = kwargs.get(anilibria_name)
            else:
                passed_kwargs[attr_name] = kwargs.get(attr_name)

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
        if kwargs is None:
            return None
        return obj(**kwargs)

    return wrapper


def convert_list(obj):
    def wrapper(list):
        if list is None:
            return []
        return [obj(**_) for _ in list]

    return wrapper


def convert_playlist(obj):
    def wrapper(playlist: Union[dict, list]):
        if isinstance(playlist, list):
            return [obj(**_) for _ in playlist]
        else:
            return {key: obj(**value) for key, value in playlist.items()}

    return wrapper