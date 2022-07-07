from enum import Enum, IntEnum


__all__ = ["StrEnum", "StatusCode", "TitleType", "SeasonCode", "RSSType", "DescriptionType", "Include", "PlayListType"]


class StrEnum(str, Enum):
    ...


class StatusCode(IntEnum):
    AT_WORK = 1
    FINISHED = 2
    HIDDEN = 3
    NO_ONGOING = 4


class TitleType(IntEnum):
    FILM = 0
    TV = 1
    OVA = 2
    ONA = 3
    SPECIAL = 4


class SeasonCode(IntEnum):
    EMPTY = 0
    WINTER = 1
    SPRING = 2
    SUMMER = 3
    AUTUMN = 4
    FALL = 4


class RSSType(StrEnum):
    RSS = "rss"
    ATOM = "atom"
    JSON = "json"


class DescriptionType(StrEnum):
    HTML = "html"
    PLAIN = "plain"
    NO_VIEW_ORDER = "no_view_order"


class Include(StrEnum):
    RAW_POSTER = "raw_poster"
    RAW_TORRENT = "raw_torrent"
    TORRENT_META = "torrent_meta"


class PlayListType(StrEnum):
    ARRAY = "array"
    LIST = "array"
    OBJECT = "object"
    DICT = "object"
