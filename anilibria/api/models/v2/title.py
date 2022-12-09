from .enums import StatusCode, TitleType, SeasonCode
from ..attrs_utils import define


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
class TitleNames:
    """
    Объект, содержащий названия тайтла на различных языках.
    """

    ru: str
    "Название тайтла на русском языке"
    en: str
    "Название тайтла на английском языке"
    alternative: str | None
    "Название тайтла на альтернативном языке"


@define()
class Status:
    """
    Объект статуса тайтла
    """

    string: str | None
    "Представление статуса в виде строки"
    code: StatusCode | None
    "Код статуса"


@define()
class Poster:
    """
    Объект с моделью постера
    """

    url: str | None
    "Относительная ссылка на постер"
    raw_base64_file: str | None
    "Закодированный в base64 постер"

    @property
    def full_url(self) -> str | None:
        """
        Возвращает полную ссылку на постер
        """
        if self.url is not None:
            return f"https://anilibria.tv{self.url}"


@define()
class Posters:
    """
    Объект с разными размерами постера
    """

    small: Poster
    "Постер маленького размера"
    medium: Poster
    "Постер среднего размера"
    original: Poster
    "Постер оригинального размера"


@define()
class Type:
    """
    Объект с информацией о типе тайтла.
    """

    full_string: str
    code: TitleType
    string: str
    series: int
    length: str


@define()
class Team:
    """
    Объект с участниками, которые принимали участие в переводе тайтла.
    """

    voice: list[str]
    "Участники, работавших над озвучкой"
    translator: list[str]
    "Участники, работавших над переводом"
    editing: list[str]
    "Участники, работавших над субтитрами"
    decor: list[str]
    "Участники, работавших над оформлением"
    timing: list[str]
    "Участники, работавшие над таймингом"


@define()
class Season:
    """
    Объект с информацией о сезоне тайтла.
    """

    string: str
    "Полное название сезона"
    code: SeasonCode
    "Код сезона"
    year: int
    "Год выпуска"
    week_day: int
    "День недели"


@define()
class Blocked:
    """
    Объект с информацией о статусе блокировки тайтла.
    """

    blocked: bool
    "Тайтл заблокирован на территории РФ"
    bakanim: bool
    "Тайлтл заблокирован из-за жалобы Wakanim"


@define()
class Series:
    """
    Объект с информацией о количестве серий
    """

    first: int
    "Номер первой серии"
    last: int
    "Номер последней серии"
    string: str
    "Представление количества серий в виде строки"


@define()
class HLS:
    """
    Объект, содержащий ссылки на серии в различных качествах.

    ..warning
        Ссылки являются относительными и не содержат домена!
    """

    fhd: str
    "Ссылка на видео в Full HD качестве"
    hd: str
    "Ссылка на видео в HD качестве"
    sd: str
    "Ссылка на видео в SD качестве"


@define()
class SerieSkips:
    """
    Объект с таймкодами для пропуска опенинга и эндинга.
    """

    opening: list[str]
    "Таймкоды для опенинга"
    ending: list[str]
    "Таймкоды для эндинга"


@define()
class Serie:
    """
    Объект, содержащий информацию о серии.
    """

    serie: int
    "Номер серии"
    created_timestamp: int
    "Время создания/изменения в формате UNIX timestamp"
    hls: HLS
    "Ссылки на серию"
    preview: str
    "Ссылка на превью серии"
    skips: SerieSkips
    "Таймкоды на пропуски"

    # TODO: Добавить свойство 'created_at' с datetime


@define()
class RutubeSerie:
    """
    Объект с информацией о серии в rutube
    """

    created_timestamp: int
    "Время создания/изменения в формате UNIX timestamp"
    rutube_id: str  # TODO: Возможно ли из айди собрать ссылку?
    "ID серии"
    serie: int
    "Номер серии"


@define()
class Player:
    """
    Объект с информацией о плеере и сериях.
    """

    alternative_player: str
    "Ссылка на альтернативный плеер"
    host: str
    "Имена предпочитаемых серверов для построения ссылок на поток и скачивание"
    series: Series
    "Количество вышедших серий"
    playlist: list[Serie] | dict[str, Serie]  # TODO: yeet
    "Список релизов"
    rutube_playlist: list[RutubeSerie] |  dict[str, RutubeSerie]  # TODO: yeet
    "Список релизов на rutube"


@define()
class Quality:
    """
    Объект, содержащий информацию о разрешении, кодировщике и типе релиза
    """

    string: str
    "Полная информация о качестве"
    type: str  # TODO: Enum!
    "Тип релиза"
    resolution: int
    "Разрешение серии"
    encoder: str
    "Название кодировщика"
    lq_audio: bool
    "Используется ли аудио дорожка с пониженным битрейтом"


@define()
class TorrentFile:
    """
    Объект с информацией о торрент файле
    """

    file: str
    "Имя файла"
    size: int
    "Размер файла в байтах"
    offset: int
    "Смещение в байтах относительно предыдущего файла"


@define()
class TorrentMetaData:
    """
    Объект с метадатой о торренте
    """

    hash: str
    "Хеш торрент файла"
    name: str
    "Имя тайтла в торрент файле"
    announce: list[str]
    "Список трекеров"
    created_timestamp: int
    "Время создания торрента в UNIX timestamp"
    files_list: list[TorrentFile]
    "Список файлов в торренте"


@define()
class Torrent:
    """
    Объект с информацией о торренте
    """

    torrent_id: int
    "ID торрент файла"
    series: Series
    "Серии, содержащиеся в файле"
    quality: Quality
    "Информаци о разрешении, кодировщике и типе релиза"
    leechers: int
    "Количество личей"
    seeders: int
    "Количество сидов"
    downloads: int  # TODO: IM HERE
    total_size: int
    url: str
    uploaded_timestamp: int
    metadata: TorrentMetaData
    raw_base64_file: str
    hash: str


@define()
class Torrents:
    """
    Модель со списком торрентов и информации о сериях.
    """

    series: Series
    list: list[Torrent]


@define()
class Title:
    """
    Модель тайтла
    """

    id: int
    code: str
    names: TitleNames
    announce: str
    status: Status
    posters: Posters
    updated: int
    last_change: int
    type: Type
    genres: list[str]
    team: Team
    season: Season
    description: str
    in_favorites: int
    blocked: Blocked
    player: Player
    torrents: Torrents

    @property
    def url(self):
        return f"https://anilibria.tv/release/{self.code}.html"
