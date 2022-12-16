from typing import Type

from cattrs import Converter

from .title import Serie, RutubeSerie

__all__ = ["converter"]

converter = Converter()


def _playlist_hook(data: dict | list, type_: Type[Serie | RutubeSerie]):
    if isinstance(data, list):
        return [converter.structure(_, type_) for _ in data]
    if isinstance(data, dict):
        return {k: converter.structure(v, type_) for k, v in data.items()}


def _series_hook(data: dict | list, type_: type):
    return _playlist_hook(data, Serie)


def _rutube_series_hook(data: dict | list, type_: type):
    return _playlist_hook(data, RutubeSerie)


converter.register_structure_hook(dict[str, Serie] | list[Serie], _series_hook)
converter.register_structure_hook(dict[str, RutubeSerie] | list[RutubeSerie], _rutube_series_hook)
