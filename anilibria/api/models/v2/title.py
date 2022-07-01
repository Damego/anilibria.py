from typing import List, Dict, Union
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Poster:
    """
    Модель постера.
    """
    url: str
    raw_base64_file: None


@dataclass(slots=True)
class Posters:
    """
    Модель, которая содержит в себе постеры разных размеров.
    """
    small: Poster
    medium: Poster
    original: Poster

    def __post_init__(self):
        self.small = Poster(**self.small)  # type: ignore
        self.medium = Poster(**self.medium)  # type: ignore
        self.original = Poster(**self.original)  # type: ignore


@dataclass(slots=True, frozen=True)
class Type:
    """
    Модель с информацией о типе тайтла.
    """
    full_string: str
    code: int
    string: str
    series: int
    length: str


@dataclass(slots=True, frozen=True)
class Team:
    """
    Модель с участниками, которые принимали участие в переводе тайтла.
    """
    voice: List[str]
    translator: List[str]
    editing: List[str]
    decor: List[str]
    timing: List[str]


@dataclass(slots=True, frozen=True)
class Season:
    """
    Модель с информацией о сезоне тайтла.
    """
    string: str
    code: int
    year: int
    week_day: int


@dataclass(slots=True, frozen=True)
class Blocked:
    """
    Модель с информацией о статусе блокировки тайтла.
    """
    blocked: bool
    bakanim: bool


@dataclass(slots=True, frozen=True)
class Series:
    """
    Модель, которая содержит информацию о
    """
    first: int
    last: int
    string: str


@dataclass(slots=True, frozen=True)
class HLS:
    """
    Модель с ссылками на разные разрешения серий.
    """
    fhd: str
    hs: str
    sd: str


@dataclass(slots=True, frozen=True)
class SerieSkips:
    """
    Модель с таймкодами для пропуска опенинга и эндинга.
    """
    opening: List[int]
    ending: List[int]


@dataclass(slots=True)
class Serie:
    """
    Модель с информацией о серии.
    """
    serie: int
    created_timestamp: int
    hls: HLS
    preview: None  # Not documented in the docs
    skips: SerieSkips  # Not documented in the docs

    def __post__init__(self):
        self.hls = HLS(**self.hls)  # type: ignore
        self.skips = SerieSkips(**self.skips)  # type: ignore


@dataclass(slots=True)
class Player:
    """
    Модель с информацией о плеере. Содержит все серии.

    .. note::
       Изначально playlist должно был быть типа Dict[str, Serie],
       так как ключ выступает в роли номера серии, но номер серии дают в самом Serie,
       поэтому решено убрать ключи, оставив только список с сериями.
    """
    alternative_player: str
    host: str
    series: Series
    playlist: List[Serie]

    def __post_init__(self):
        self.series: Series = Series(**self.series)  # type: ignore
        self.playlist: List[Serie] = [Serie(**serie) for serie in self.playlist.values()]  # type: ignore


@dataclass(slots=True, frozen=True)
class Quality:
    """
    Модель с информацией о качестве тайтла.
    """
    string: str
    type: str
    resolution: int
    encoder: str
    lq_audio: bool


@dataclass(slots=True, frozen=True)
class Torrent:
    """
    Модель с информацией о торренте
    """
    torrent_id: int
    series: Series
    quality: Quality
    leechers: int
    seeders: int
    downloads: int
    total_size: int
    url: str
    uploaded_timestamp: int
    metadata: None
    raw_base64_file: None
    hash: str
        
    def __post_init__(self):
        self.quality = Quality(**self.quality)  # type: ignore


@dataclass(slots=True)
class Torrents:
    """
    Модель со списком торрентов и информации о сериях.
    """
    series: Series
    list: List[Torrent]

    def __post_init__(self):
        self.series = Series(**self.series)  # type: ignore
        self.list = [Torrent(**torrent) for torrent in self.list]  # type: ignore


@dataclass(slots=True)
class Title:
    """
    Модель тайтла
    """
    id: int
    code: str
    names: Dict[str, Union[str, None]]
    announce: str
    status: Dict[str, Union[str, int]]
    posters: Posters
    updated: int
    last_change: int
    type: Type
    genres: List[str]
    team: Team
    season: Season
    description: str
    in_favorites: int
    blocked: Blocked
    player: Player
    torrents: Torrents

    def __post_init__(self):
        self.posters = Posters(**self.posters)  # type: ignore
        self.type = Type(**self.type)  # type: ignore
        self.team = Team(**self.team)  # type: ignore
        self.season = Season(**self.season)  # type: ignore
        self.blocked = Blocked(**self.blocked)  # type: ignore
        self.player = Player(**self.player)  # type: ignore
        self.torrents = Torrents(**self.torrents)  # type: ignore
