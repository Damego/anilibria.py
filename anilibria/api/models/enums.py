from enum import Enum
from typing import TypeVar

T = TypeVar("T")

__all__ = [
    "StrEnum",
    "IntEnum",
    "StatusCode",
    "TitleCodeType",
    "SeasonCode",
    "RSSType",
    "DescriptionType",
    "Include",
    "PlaylistType",
]


class StrEnum(str, Enum):
    @classmethod
    def _missing_(cls, value: str):
        new = str.__new__(cls)
        new._name_ = f"UNKNOWN-ENUM-{value}"
        new._value_ = value

        return cls._value2member_map_.setdefault(value, new)

    def __str__(self):
        return str(self.value)


class IntEnum(int, Enum):
    @classmethod
    def _missing_(cls, value: int):
        new = int.__new__(cls)
        new._name_ = f"UNKNOWN-ENUM-{value}"
        new._value_ = value

        return cls._value2member_map_.setdefault(value, new)

    def __int__(self) -> int:
        return int(self.value)


class StatusCode(IntEnum):
    AT_WORK = 1
    "В работе"
    FINISHED = 2
    "Закончен"
    HIDDEN = 3
    "Скрыт"
    NO_ONGOING = 4
    "Неонгоинг"


class TitleCodeType(IntEnum):
    FILM = 0
    TV = 1
    OVA = 2
    ONA = 3
    SPECIAL = 4
    WEB = 5


class SeasonCode(IntEnum):
    """
    Представляет код сезона
    """

    UNKNOWN = 0
    "Неизвестный сезон"
    WINTER = 1
    "Зимний сезон"
    SPRING = 2
    "Весенний сезон"
    SUMMER = 3
    "Летний сезон"
    AUTUMN = FALL = 4
    "Осенний сезон"


class RSSType(StrEnum):
    """
    Представляет тип ответа на ``client.get_rss()``
    """

    RSS = "rss"
    ATOM = "atom"
    JSON = "json"


class DescriptionType(StrEnum):
    """
    Представляет тип описания тайтла
    """

    HTML = "html"
    PLAIN = "plain"
    NO_VIEW_ORDER = "no_view_order"


class Include(StrEnum):
    """
    Представляет запрашиваемый контент, который недоступен по умолчанию
    """

    RAW_POSTER = "raw_poster"
    RAW_TORRENT = "raw_torrent"
    TORRENT_META = "torrent_meta"


class PlaylistType(StrEnum):
    """
    Представляет тип плейлиста
    """

    ARRAY = LIST = "array"
    "Плейлист в виде списка"
    OBJECT = DICT = "object"
    "Плейлист в виде словаря"


class QualityType(StrEnum):
    WEBRip = "WEBRip"
