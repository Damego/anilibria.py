from typing import List, Optional

from attrs import define, field

from .enums import StatusCode, TitleType, SeasonCode
from ..attrs_utils import convert_list, convert, convert_playlist


__all__ = [
    "Names",
    "Status",
    "Poster",
    "Posters",
    "Type",
    "Team",
    "Season",
    "Blocked",
    "Series",
    "HLS",
    "SerieSkips",
    "Serie",
    "Player",
    "Quality",
    "TorrentFile",
    "TorrentMetaData",
    "Torrent",
    "Torrents",
    "Title",
]


@define
class Names:
    """
    Содержит в себе названия тайтла на русском, английском и альтернативном языках
    """

    ru: str = field(default=None)
    en: str = field(default=None)
    alternative: Optional[str] = field(default=None)


@define
class Status:
    """
    Содержит в себе текущий статус тайтла
    """

    string: Optional[str] = field(default=None)
    code: Optional[StatusCode] = field(converter=StatusCode, default=None)


@define
class Poster:
    """
    Модель постера.
    """

    url: Optional[str] = field(default=None)
    raw_base64_file: Optional[str] = field(default=None)


@define
class Posters:
    """
    Модель, которая содержит в себе постеры разных размеров.
    """

    small: Optional[Poster] = field(converter=convert(Poster), default=None)
    medium: Optional[Poster] = field(converter=convert(Poster), default=None)
    original: Optional[Poster] = field(converter=convert(Poster), default=None)


@define
class Type:
    """
    Модель с информацией о типе тайтла.
    """

    full_string: Optional[str] = field(default=None)
    code: Optional[TitleType] = field(converter=TitleType, default=None)
    string: Optional[str] = field(default=None)
    series: Optional[int] = field(default=None)
    length: Optional[str] = field(default=None)


@define
class Team:
    """
    Модель с участниками, которые принимали участие в переводе тайтла.
    """

    voice: Optional[List[str]] = field(factory=list)
    translator: Optional[List[str]] = field(factory=list)
    editing: Optional[List[str]] = field(factory=list)
    decor: Optional[List[str]] = field(factory=list)
    timing: Optional[List[str]] = field(factory=list)


@define
class Season:
    """
    Модель с информацией о сезоне тайтла.
    """

    string: Optional[str] = field(default=None)
    code: Optional[SeasonCode] = field(converter=SeasonCode, default=None)
    year: Optional[int] = field(default=None)
    week_day: Optional[int] = field(default=None)


@define
class Blocked:
    """
    Модель с информацией о статусе блокировки тайтла.
    """

    blocked: Optional[bool] = field(default=None)
    bakanim: Optional[bool] = field(default=None)


@define
class Series:
    """
    Модель, которая содержит информацию о
    """

    first: Optional[int] = field(default=None)
    last: Optional[int] = field(default=None)
    string: Optional[str] = field(default=None)


@define
class HLS:
    """
    Модель с ссылками на разные разрешения серий.
    """

    fhd: Optional[str] = field(default=None)
    hd: Optional[str] = field(default=None)
    sd: Optional[str] = field(default=None)


@define
class SerieSkips:
    """
    Модель с таймкодами для пропуска опенинга и эндинга.
    """

    opening: Optional[List[str]] = field(factory=list)
    ending: Optional[List[str]] = field(factory=list)


@define
class Serie:
    """
    Модель с информацией о серии.
    """

    serie: Optional[int] = field(default=None)
    created_timestamp: Optional[int] = field(default=None)
    hls: Optional[HLS] = field(converter=convert(HLS), default=None)
    preview: Optional[str] = field(default=None)  # Not documented in the docs
    skips: Optional[SerieSkips] = field(
        converter=convert(SerieSkips), default=None
    )  # Not documented in the docs


@define
class Player:
    """
    Модель с информацией о плеере. Содержит все серии.

    .. note::
       Изначально playlist должно был быть типа Dict[str, Serie],
       так как ключ выступает в роли номера серии, но номер серии дают в самом Serie,
       поэтому решено убрать ключи, оставив только список с сериями.
    """

    alternative_player: Optional[str] = field(default=None)
    host: Optional[str] = field(default=None)
    series: Optional[Series] = field(converter=convert(Series), default=None)
    playlist: Optional[List[Serie]] = field(converter=convert_playlist(Serie), factory=list)


@define
class Quality:
    """
    Модель с информацией о качестве тайтла.
    """

    string: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    resolution: Optional[int] = field(default=None)
    encoder: Optional[str] = field(default=None)
    lq_audio: Optional[bool] = field(default=None)


@define
class TorrentFile:
    file: str
    size: int
    offset: int


@define
class TorrentMetaData:
    hash: str = field()
    name: str = field()
    announce: List[str] = field(converter=list)
    created_timestamp: int = field()
    files_list: List[TorrentFile] = field(converter=convert_list(TorrentFile))


@define
class Torrent:
    """
    Модель с информацией о торренте
    """

    torrent_id: Optional[int] = field(default=None)
    series: Optional[Series] = field(converter=convert(Series), default=None)
    quality: Optional[Quality] = field(converter=convert(Quality), default=None)
    leechers: Optional[int] = field(default=None)
    seeders: Optional[int] = field(default=None)
    downloads: Optional[int] = field(default=None)
    total_size: Optional[int] = field(default=None)
    url: Optional[str] = field(default=None)
    uploaded_timestamp: Optional[int] = field(default=None)
    metadata: Optional[TorrentMetaData] = field(converter=convert(TorrentMetaData), default=None)
    raw_base64_file: Optional[str] = field(default=None)
    hash: Optional[str] = field(default=None)


@define
class Torrents:
    """
    Модель со списком торрентов и информации о сериях.
    """

    series: Optional[Series] = field(converter=convert(Series), default=None)
    list: Optional[List[Torrent]] = field(converter=convert_list(Torrent), factory=list)


@define
class Title:
    """
    Модель тайтла
    """

    id: Optional[int] = field(default=None)
    code: Optional[str] = field(default=None)
    names: Optional[Names] = field(converter=convert(Names), default=None)
    announce: Optional[str] = field(default=None)
    status: Optional[Status] = field(converter=convert(Status), default=None)
    posters: Optional[Posters] = field(converter=convert(Posters), default=None)
    updated: Optional[int] = field(default=None)
    last_change: Optional[int] = field(default=None)
    type: Optional[Type] = field(converter=convert(Type), default=None)
    genres: Optional[List[str]] = field(factory=list)
    team: Optional[Team] = field(converter=convert(Team), default=None)
    season: Optional[Season] = field(converter=convert(Season), default=None)
    description: Optional[str] = field(default=None)
    in_favorites: Optional[int] = field(default=None)
    blocked: Optional[Blocked] = field(converter=convert(Blocked), default=None)
    player: Optional[Player] = field(converter=convert(Player), default=None)
    torrents: Optional[Torrents] = field(converter=convert(Torrents), default=None)

    @property
    def url(self):
        return f"https://anilibria.tv/release/{self.code}.html"
