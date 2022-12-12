from typing import Type

from cattrs import register_structure_hook, structure

from .title import Serie, RutubeSerie


def _playlist_hook(data: dict | list, type_: Type[Serie | RutubeSerie]):
    if isinstance(data, list):
        return [structure(_, type_) for _ in data]
    if isinstance(data, dict):
        return {k: structure(v, type_) for k, v in data.items()}


def _series_hook(data: dict | list, type_: type):
    return _playlist_hook(data, Serie)


def _rutube_series_hook(data: dict | list, type_: type):
    return _playlist_hook(data, RutubeSerie)


register_structure_hook(dict[str, Serie] | list[Serie], _series_hook)
register_structure_hook(dict[str, RutubeSerie] | list[RutubeSerie], _rutube_series_hook)
