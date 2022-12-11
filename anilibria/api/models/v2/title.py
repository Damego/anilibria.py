from .enums import StatusCode, TitleCodeType, SeasonCode
from ..attrs_utils import define


__all__ = [
    "TitleNames",
    "TitleStatus",
    "Poster",
    "Posters",
    "TitleType",
    "TitleTeam",
    "Season",
    "Blocked",
    "Series",
    "HLS",
    "SerieSkips",
    "Serie",
    "RutubeSerie",
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
class TitleStatus:
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
class TitleType:
    """
    Объект с информацией о типе тайтла.
    """

    full_string: str
    "Полная информация о типе в виде строки"
    code: TitleCodeType
    "Код типа"
    string: str
    "Тип тайтла в виде строки"
    series: int
    "Количество серий"
    length: str
    "Длина серии"


@define()
class TitleTeam:
    """
    Объект с участниками, которые принимали участие в переводе тайтла.
    """

    voice: list[str]
    "Участники, работавшие над озвучкой"
    translator: list[str]
    "Участники, работавшие над переводом"
    editing: list[str]
    "Участники, работавшие над субтитрами"
    decor: list[str]
    "Участники, работавшие над оформлением"
    timing: list[str]
    "Участники, работавшие над таймингом"


@define()
class Season:
    """
    Объект с информацией о сезоне тайтла.
    """

    string: str
    "Название сезона"
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
    playlist: dict[str, Serie] | list[Serie]
    "Список релизов"
    rutube_playlist: dict[str, RutubeSerie] | list[RutubeSerie]
    "Список релизов на rutube"


@define()
class Quality:
    """
    Объект, содержащий информацию о разрешении, кодировщике и типе релиза
    """

    string: str | None
    "Полная информация о качестве"
    type: str | None  # TODO: Enum!
    "Тип релиза"
    resolution: str | None
    "Разрешение серии"
    encoder: str | None
    "Название кодировщика"
    lq_audio: bool | None
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

    hash: str | None
    "Хеш торрент файла"
    name: str | None
    "Имя тайтла в торрент файле"
    announce: list[str] | None
    "Список трекеров"
    created_timestamp: int | None
    "Время создания торрента в UNIX timestamp"
    files_list: list[TorrentFile] | None
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
    "Информация о разрешении, кодировщике и типе релиза"
    leechers: int
    "Количество личей"
    seeders: int
    "Количество сидов"
    downloads: int
    "Количество загрузок"
    total_size: int
    "Размер файлов в торренте в байтах"
    url: str
    "Ссылка на торрент без домена"
    uploaded_timestamp: int
    "Время загрузки домена в формате UNIX timestamp"
    metadata: TorrentMetaData | None
    "Метаданные торрент файла"
    raw_base64_file: str | None
    "Торрент файл в формате base64"
    hash: str
    "Хэш торрент файла"


@define()
class Torrents:
    """
    Модель со списком торрентов и информации о сериях.
    """

    series: Series
    "Серии, содержащиеся в файле"
    list: list[Torrent]
    "Список с информацией о торрент файлах"




@define()
class Title:
    """
    Объект тайтла
    """

    id: int
    "ID тайтла"
    code: str
    "Код тайтла"
    names: TitleNames
    "Названия тайтла"
    announce: str
    "Объявление для тайтла"
    status: TitleStatus
    "Статус тайтла"
    posters: Posters
    "Информация о постерах"
    updated: int
    "Время последнего обновления тайтла в формате UNIX timestamp"
    last_change: int
    "Время последнего изменения тайтла в формате UNIX timestamp"
    type: TitleType
    "Информация о типе тайтла"
    genres: list[str]
    "Список жанров тайтла"
    team: TitleTeam
    "Члены команды, работавшие над тайтлом"
    season: Season
    "Информация о сезоне"
    description: str
    "Описание тайтла"
    in_favorites: int
    "Сколько раз тайтл добавили в избранное"
    blocked: Blocked
    "Информация о блокировке тайтла"
    player: Player
    "Информация о плеере"
    torrents: Torrents
    "Информация о торрентах"

    @property
    def url(self) -> str:
        """
        Возвращает полную ссылку на тайтл
        """
        return f"https://anilibria.tv/release/{self.code}.html"
