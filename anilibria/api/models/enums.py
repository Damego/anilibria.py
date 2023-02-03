from enum import Enum
from typing import Any, Type

__all__ = (
    "StrEnum",
    "IntEnum",
    "StatusCode",
    "TitleCodeType",
    "SeasonCode",
    "RSSType",
    "DescriptionType",
    "Include",
    "PlaylistType",
)


def _cursed_enum(cls: Type[Enum], obj: type, value: Any) -> Enum:
    new = obj.__new__(cls)  # type: ignore
    new._name_ = f"UNKNOWN: {value}"
    new._value_ = value

    return cls._value2member_map_.setdefault(value, new)


class IntEnum(int, Enum):
    """Enum where members must be ints"""

    @classmethod
    def _missing_(cls, value: int) -> Enum:
        return _cursed_enum(cls, int, value)


class StrEnum(str, Enum):
    """Enum where members must be strings"""

    @classmethod
    def _missing_(cls, value: str) -> Enum:
        return _cursed_enum(cls, str, value)

    def __str__(self):
        return self.value


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
