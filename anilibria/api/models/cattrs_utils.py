from typing import List, Type

from cattrs import Converter

from .title import Episode, RutubeEpisode

__all__ = ("converter",)

converter = Converter()


def _playlist_hook(data: dict | list, type_: Type[Episode | RutubeEpisode]):
    if isinstance(data, list):
        return [converter.structure(_, type_) for _ in data]
    if isinstance(data, dict):
        return {k: converter.structure(v, type_) for k, v in data.items()}


def _series_hook(data: dict | list, type_: type):
    return _playlist_hook(data, Episode)


def _rutube_series_hook(data: dict | list, type_: type):
    return _playlist_hook(data, RutubeEpisode)


converter.register_structure_hook(dict[str, Episode] | List[Episode], _series_hook)
converter.register_structure_hook(
    dict[str, RutubeEpisode] | List[RutubeEpisode], _rutube_series_hook
)
