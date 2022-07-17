from typing import List, Optional, Dict, Union

from .enums import StatusCode, TitleType, SeasonCode
from ..attrs_utils import convert_list, convert, convert_playlist, define, field, DictSerializer


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


@define()
class Names(DictSerializer):
    """
    Содержит в себе названия тайтла на русском, английском и альтернативном языках
    """

    ru: str = field(default=None)
    en: str = field(default=None)
    alternative: Optional[str] = field(default=None)


@define()
class Status(DictSerializer):
    """
    Содержит в себе текущий статус тайтла
    """

    string: Optional[str] = field(default=None)
    code: Optional[StatusCode] = field(converter=StatusCode.from_value, default=None)


@define()
class Poster(DictSerializer):
    """
    Модель постера.
    """

    url: Optional[str] = field(default=None)
    raw_base64_file: Optional[str] = field(default=None)

    @property
    def full_url(self):
        return f"https://anilibria.tv{self.url}"


@define()
class Posters(DictSerializer):
    """
    Модель, которая содержит в себе постеры разных размеров.
    """

    small: Optional[Poster] = field(converter=convert(Poster), default=None)
    medium: Optional[Poster] = field(converter=convert(Poster), default=None)
    original: Optional[Poster] = field(converter=convert(Poster), default=None)


@define()
class Type(DictSerializer):
    """
    Модель с информацией о типе тайтла.
    """

    full_string: Optional[str] = field(default=None)
    code: Optional[TitleType] = field(converter=TitleType.from_value, default=None)
    string: Optional[str] = field(default=None)
    series: Optional[int] = field(default=None)
    length: Optional[str] = field(default=None)


@define()
class Team(DictSerializer):
    """
    Модель с участниками, которые принимали участие в переводе тайтла.
    """

    voice: Optional[List[str]] = field(factory=list)
    translator: Optional[List[str]] = field(factory=list)
    editing: Optional[List[str]] = field(factory=list)
    decor: Optional[List[str]] = field(factory=list)
    timing: Optional[List[str]] = field(factory=list)


@define()
class Season(DictSerializer):
    """
    Модель с информацией о сезоне тайтла.
    """

    string: Optional[str] = field(default=None)
    code: Optional[SeasonCode] = field(converter=SeasonCode.from_value, default=None)
    year: Optional[int] = field(default=None)
    week_day: Optional[int] = field(default=None)


@define()
class Blocked(DictSerializer):
    """
    Модель с информацией о статусе блокировки тайтла.
    """

    blocked: Optional[bool] = field(default=None)
    bakanim: Optional[bool] = field(default=None)


@define()
class Series(DictSerializer):
    """
    Модель, которая содержит информацию о
    """

    first: Optional[int] = field(default=None)
    last: Optional[int] = field(default=None)
    string: Optional[str] = field(default=None)


@define()
class HLS(DictSerializer):
    """
    Модель с ссылками на разные разрешения серий.
    """

    fhd: Optional[str] = field(default=None)
    hd: Optional[str] = field(default=None)
    sd: Optional[str] = field(default=None)


@define()
class SerieSkips(DictSerializer):
    """
    Модель с таймкодами для пропуска опенинга и эндинга.
    """

    opening: Optional[List[str]] = field(factory=list)
    ending: Optional[List[str]] = field(factory=list)


@define()
class Serie(DictSerializer):
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


@define()
class Player(DictSerializer):
    """
    Модель с информацией о плеере и сериях.
    """

    alternative_player: Optional[str] = field(default=None)
    host: Optional[str] = field(default=None)
    series: Optional[Series] = field(converter=convert(Series), default=None)
    playlist: Optional[Union[List[Serie], Dict[str, Serie]]] = field(
        converter=convert_playlist(Serie), factory=list
    )


@define()
class Quality(DictSerializer):
    """
    Модель с информацией о качестве тайтла.
    """

    string: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    resolution: Optional[int] = field(default=None)
    encoder: Optional[str] = field(default=None)
    lq_audio: Optional[bool] = field(default=None)


@define()
class TorrentFile(DictSerializer):
    file: str
    size: int
    offset: int


@define()
class TorrentMetaData(DictSerializer):
    hash: str = field()
    name: str = field()
    announce: List[str] = field(converter=list)
    created_timestamp: int = field()
    files_list: List[TorrentFile] = field(converter=convert_list(TorrentFile))


@define()
class Torrent(DictSerializer):
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


@define()
class Torrents(DictSerializer):
    """
    Модель со списком торрентов и информации о сериях.
    """

    series: Optional[Series] = field(converter=convert(Series), default=None)
    list: Optional[List[Torrent]] = field(converter=convert_list(Torrent), factory=list)


@define()
class Title(DictSerializer):
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
