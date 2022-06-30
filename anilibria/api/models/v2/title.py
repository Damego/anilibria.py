from typing import List, Dict, Union
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Poster:
    url: str
    raw_base64_file: None  # What?


@dataclass(slots=True)
class Posters:
    small: Poster
    medium: Poster
    original: Poster

    def __init__(self, *, small: dict, medium: dict, original: dict):
        self.small = Poster(**small)
        self.medium = Poster(**medium)
        self.original = Poster(**original)


@dataclass(slots=True, frozen=True)
class Type:
    full_string: str
    code: int
    string: str
    series: int
    length: str


@dataclass(slots=True, frozen=True)
class Team:
    voice: List[str]
    translator: List[str]
    editing: List[str]
    decor: List[str]
    timing: List[str]


@dataclass(slots=True, frozen=True)
class Season:
    string: str
    code: int
    year: int
    week_day: int


@dataclass(slots=True, frozen=True)
class Blocked:
    blocked: bool
    bakanim: bool


@dataclass(slots=True, frozen=True)
class Series:
    first: int
    last: int
    string: str


@dataclass(slots=True, frozen=True)
class HLS:
    fhd: str
    hs: str
    sd: str


@dataclass(slots=True, frozen=True)
class SerieSkips:
    opening: List[int]
    ending: List[int]


@dataclass(slots=True)
class Serie:
    serie: int
    created_timestamp: int
    hls: HLS
    preview: None  # Not documented in the docs
    skips: SerieSkips  # Not documented in the docs

    def __post__init__(self):
        self.skips = SerieSkips(**self.skips)


@dataclass(slots=True)
class Player:
    alternative_player: str
    host: str
    series: Series
    playlist: List[Serie]
    # изначально тут должно быть Dict[str, Serie],
    # но ключ выступает в роли номера серии, который тоже дают в Serie,
    # поэтому я решил убрать ключи, оставив список с сериями.

    def __post_init__(self):
        self.playlist: List[Serie] = [
            Serie(**serie) for serie in self.playlist.values()
        ]


@dataclass(slots=True, frozen=True)
class Quality:
    string: str
    type: str
    resolution: int
    encoder: str
    lq_audio: bool


@dataclass(slots=True, frozen=True)
class Torrent:
    torrent_id: int
    series: Series
    quality: Quality
    leechers: int
    seeders: int
    downloads: int
    total_size: int
    url: str
    uploaded_timestamp: int
    metadata: None  # What?
    raw_base64_file: None  # What?
    hash: str


@dataclass(slots=True)
class Torrents:
    series: Series
    list: List[Torrent]

    def __init__(self, series: dict, list: List[dict]) -> None:
        self.series = Series(**series)
        self.list = [Torrent(**torrent) for torrent in list]


@dataclass(slots=True)
class Title:
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
        self.posters = Posters(**self.posters)
        self.type = Type(**self.type)
        self.team = Team(**self.team)
        self.season = Season(**self.season)
        self.blocked = Blocked(**self.blocked)
        self.player = Player(**self.player)
        self.torrents = Torrents(**self.torrents)
