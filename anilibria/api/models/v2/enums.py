from enum import Enum


__all__ = [
    "AttrEnum",
    "StrEnum",
    "IntEnum",
    "StatusCode",
    "TitleType",
    "SeasonCode",
    "RSSType",
    "DescriptionType",
    "Include",
    "PlayListType",
]


class AttrEnum(Enum):
    @classmethod
    def from_value(cls, value):
        """
        Similar to Enum(value) but if value not found then returns value
        """
        try:
            return cls(value)
        except ValueError:
            return value


class StrEnum(str, AttrEnum):
    """
    ``enum.IntEnum``, но для строк и возвращает ``None``, если значение не найдено
    """

    ...


class IntEnum(int, AttrEnum):
    """
    Похож на ``enum.IntEnum``, но возвращает ``None``, если значение не найдено
    """

    ...


class StatusCode(IntEnum):
    """
    Представляет текущий статус тайтла
    """

    AT_WORK = 1
    FINISHED = 2
    HIDDEN = 3
    NO_ONGOING = 4


class TitleType(IntEnum):
    """
    Представляет тип тайтла
    """

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

    EMPTY = 0
    WINTER = 1
    SPRING = 2
    SUMMER = 3
    AUTUMN = 4
    FALL = 4


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


class PlayListType(StrEnum):
    """
    Представляет тип плейлиста
    """

    ARRAY = "array"
    LIST = "array"
    OBJECT = "object"
    DICT = "object"
