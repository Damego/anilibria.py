from typing import List, Dict, Union, Optional
from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class Names:
    """
    Содержит в себе названия тайтла на русском, английском и альтернативном языках
    """
    ru: Optional[str] = field(default=None)
    en: Optional[str] = field(default=None)
    alternative: Optional[str] = field(default=None)


@dataclass(slots=True, frozen=True)
class Status:
    """
    Содержит в себе текущий статус тайтла
    """
    string: Optional[str] = field(default=None)
    code: Optional[int] = field(default=None)


@dataclass(slots=True, frozen=True)
class Poster:
    """
    Модель постера.
    """
    url: Optional[str] = field(default=None)
    raw_base64_file: Optional[str] = field(default=None)


@dataclass(slots=True)
class Posters:
    """
    Модель, которая содержит в себе постеры разных размеров.
    """
    small: Optional[Poster] = field(default_factory=dict)
    medium: Optional[Poster] = field(default_factory=dict)
    original: Optional[Poster] = field(default_factory=dict)

    def __post_init__(self):
        self.small = Poster(**self.small) # type: ignore
        self.medium = Poster(**self.medium) # type: ignore
        self.original = Poster(**self.original)  # type: ignore


@dataclass(slots=True, frozen=True)
class Type:
    """
    Модель с информацией о типе тайтла.
    """
    full_string: Optional[str] = field(default=None)
    code: Optional[int] = field(default=None)
    string: Optional[str] = field(default=None)
    series: Optional[int] = field(default=None)
    length: Optional[str] = field(default=None)


@dataclass(slots=True, frozen=True)
class Team:
    """
    Модель с участниками, которые принимали участие в переводе тайтла.
    """
    voice: Optional[List[str]] = field(default_factory=list)
    translator: Optional[List[str]] = field(default_factory=list)
    editing: Optional[List[str]] = field(default_factory=list)
    decor: Optional[List[str]] = field(default_factory=list)
    timing: Optional[List[str]] = field(default_factory=list)


@dataclass(slots=True, frozen=True)
class Season:
    """
    Модель с информацией о сезоне тайтла.
    """
    string: Optional[str] = field(default=None)
    code: Optional[int] = field(default=None)
    year: Optional[int] = field(default=None)
    week_day: Optional[int] = field(default=None)


@dataclass(slots=True, frozen=True)
class Blocked:
    """
    Модель с информацией о статусе блокировки тайтла.
    """
    blocked: Optional[bool] = field(default=None)
    bakanim: Optional[bool] = field(default=None)


@dataclass(slots=True, frozen=True)
class Series:
    """
    Модель, которая содержит информацию о
    """
    first: Optional[int] = field(default=None)
    last: Optional[int] = field(default=None)
    string: Optional[str] = field(default=None)


@dataclass(slots=True, frozen=True)
class HLS:
    """
    Модель с ссылками на разные разрешения серий.
    """
    fhd: Optional[str] = field(default=None)
    hd: Optional[str] = field(default=None)
    sd: Optional[str] = field(default=None)


@dataclass(slots=True, frozen=True)
class SerieSkips:
    """
    Модель с таймкодами для пропуска опенинга и эндинга.
    """
    opening: Optional[List[str]] = field(default_factory=list)
    ending: Optional[List[str]] = field(default_factory=list)


@dataclass(slots=True)
class Serie:
    """
    Модель с информацией о серии.
    """
    serie: Optional[int] = field(default=None)
    created_timestamp: Optional[int] = field(default=None)
    hls: Optional[HLS] = field(default_factory=dict)
    preview: Optional[str] = field(default=None)  # Not documented in the docs
    skips: Optional[SerieSkips] = field(default_factory=dict) # Not documented in the docs

    def __post_init__(self):
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
    alternative_player: Optional[str] = field(default=None)
    host: Optional[str] = field(default=None)
    series: Optional[Series] = field(default_factory=dict)
    playlist: Optional[List[Serie]] = field(default_factory=list)

    def __post_init__(self):
        self.series: Series = Series(**self.series)  # type: ignore
        self.playlist: List[Serie] = [Serie(**serie) for serie in self.playlist.values()]  # type: ignore


@dataclass(slots=True, frozen=True)
class Quality:
    """
    Модель с информацией о качестве тайтла.
    """
    string: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    resolution: Optional[int] = field(default=None)
    encoder: Optional[str] = field(default=None)
    lq_audio: Optional[bool] = field(default=None)


@dataclass(slots=True)
class Torrent:
    """
    Модель с информацией о торренте
    """
    torrent_id: Optional[int] = field(default=None)
    series: Optional[Series] = field(default_factory=dict)
    quality: Optional[Quality] = field(default_factory=dict)
    leechers: Optional[int] = field(default=None)
    seeders: Optional[int] = field(default=None)
    downloads: Optional[int] = field(default=None)
    total_size: Optional[int] = field(default=None)
    url: Optional[str] = field(default=None)
    uploaded_timestamp: Optional[int] = field(default=None)
    metadata: Optional[str] = field(default=None)
    raw_base64_file: Optional[str] = field(default=None)
    hash: Optional[str] = field(default=None)
        
    def __post_init__(self):
        self.quality = Quality(**self.quality)  # type: ignore


@dataclass(slots=True)
class Torrents:
    """
    Модель со списком торрентов и информации о сериях.
    """
    series: Optional[Series] = field(default_factory=dict)
    list: Optional[List[Torrent]] = field(default_factory=list)

    def __post_init__(self):
        self.series = Series(**self.series)  # type: ignore
        self.list = [Torrent(**torrent) for torrent in self.list]  # type: ignore


@dataclass(slots=True)
class Title:
    """
    Модель тайтла
    """
    id: Optional[int] = field(default=None)
    code: Optional[str] = field(default=None)
    names: Optional[Names] = field(default_factory=dict)
    announce: Optional[str] = field(default=None)
    status: Optional[Status] = field(default_factory=dict)
    posters: Optional[Posters] = field(default_factory=dict)
    updated: Optional[int] = field(default=None)
    last_change: Optional[int] = field(default=None)
    type: Optional[Type] = field(default_factory=dict)
    genres: Optional[List[str]] = field(default_factory=list)
    team: Optional[Team] = field(default_factory=dict)
    season: Optional[Season] = field(default_factory=dict)
    description: Optional[str] = field(default=None)
    in_favorites: Optional[int] = field(default=None)
    blocked: Optional[Blocked] = field(default_factory=dict)
    player: Optional[Player] = field(default_factory=dict)
    torrents: Optional[Torrents] = field(default_factory=dict)

    def __post_init__(self):
        self.names = Names(**self.names)  # type: ignore
        self.status = Status(**self.status)  # type: ignore
        self.posters = Posters(**self.posters)  # type: ignore
        self.type = Type(**self.type)  # type: ignore
        self.team = Team(**self.team)  # type: ignore
        self.season = Season(**self.season)  # type: ignore
        self.blocked = Blocked(**self.blocked)  # type: ignore
        self.player = Player(**self.player)  # type: ignore
        self.torrents = Torrents(**self.torrents)  # type: ignore

    @property
    def url(self):
        return f"https://anilibria.tv/release/{self.code}.html"
