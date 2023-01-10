from typing import List

from .enums import StatusCode, TitleCodeType, SeasonCode
from .attrs_utils import define


__all__ = (
    "TitleNames",
    "TitleStatus",
    "Poster",
    "Posters",
    "TitleType",
    "TitleTeam",
    "Season",
    "Blocked",
    "Episodes",
    "HLS",
    "SerieSkips",
    "Episode",
    "RutubeSerie",
    "Player",
    "Quality",
    "TorrentFile",
    "TorrentMetaData",
    "Torrent",
    "Torrents",
    "Title",
)


@define()
class TitleNames:
    """
    Объект, содержащий названия тайтла на различных языках.
    """

    ru: str = None
    "Название тайтла на русском языке"
    en: str = None
    "Название тайтла на английском языке"
    alternative: str = None
    "Название тайтла на альтернативном языке"


@define()
class TitleStatus:
    """
    Объект статуса тайтла
    """

    string: str = None
    "Представление статуса в виде строки"
    code: StatusCode = None
    "Код статуса"


@define()
class Poster:
    """
    Объект с моделью постера
    """

    url: str = None
    "Относительная ссылка на постер"
    raw_base64_file: str = None
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

    small: Poster = None
    "Постер маленького размера"
    medium: Poster = None
    "Постер среднего размера"
    original: Poster = None
    "Постер оригинального размера"


@define()
class TitleType:
    """
    Объект с информацией о типе тайтла.
    """

    full_string: str = None
    "Полная информация о типе в виде строки"
    code: TitleCodeType = None
    "Код типа"
    string: str = None
    "Тип тайтла в виде строки"
    episodes: int = None
    "Количество серий"
    length: str = None
    "Длина серии"


@define()
class TitleTeam:
    """
    Объект с участниками, которые принимали участие в переводе тайтла.
    """

    voice: List[str] = None
    "Участники, работавшие над озвучкой"
    translator: List[str] = None
    "Участники, работавшие над переводом"
    editing: List[str] = None
    "Участники, работавшие над субтитрами"
    decor: List[str] = None
    "Участники, работавшие над оформлением"
    timing: List[str] = None
    "Участники, работавшие над таймингом"


@define()
class Season:
    """
    Объект с информацией о сезоне тайтла.
    """

    string: str = None
    "Название сезона"
    code: SeasonCode = None
    "Код сезона"
    year: int = None
    "Год выпуска"
    week_day: int = None
    "День недели"


@define()
class Blocked:
    """
    Объект с информацией о статусе блокировки тайтла.
    """

    blocked: bool = False
    "Тайтл заблокирован на территории РФ"
    bakanim: bool = False
    "Тайлтл заблокирован из-за жалобы Wakanim"


@define()
class Episodes:
    """
    Объект с информацией о количестве серий
    """

    first: int | None = None
    "Номер первой серии"
    last: int | None = None
    "Номер последней серии"
    string: str | None = None
    "Представление количества серий в виде строки"


@define()
class HLS:
    """
    Объект, содержащий ссылки на серии в различных качествах.

    ..warning
        Ссылки являются относительными и не содержат домена!
    """

    fhd: str = None
    "Ссылка на видео в Full HD качестве"
    hd: str = None
    "Ссылка на видео в HD качестве"
    sd: str = None
    "Ссылка на видео в SD качестве"


@define()
class SerieSkips:
    """
    Объект с таймкодами для пропуска опенинга и эндинга.
    """

    opening: List[str] = None
    "Таймкоды для опенинга"
    ending: List[str] = None
    "Таймкоды для эндинга"


@define()
class Episode:
    """
    Объект, содержащий информацию о серии.
    """

    episode: int = None
    "Номер серии"
    created_timestamp: int = None
    "Время создания/изменения в формате UNIX timestamp"
    hls: HLS = None
    "Ссылки на серию"
    preview: str = None
    "Ссылка на превью серии"
    skips: SerieSkips = None
    "Таймкоды на пропуски"

    # TODO: Добавить свойство 'created_at' с datetime


@define()
class RutubeSerie:
    """
    Объект с информацией о серии в rutube
    """

    created_timestamp: int = None
    "Время создания/изменения в формате UNIX timestamp"
    rutube_id: str = None  # TODO: Возможно ли из айди собрать ссылку?
    "ID серии"
    episode: int = None
    "Номер серии"


@define()
class Player:
    """
    Объект с информацией о плеере и сериях.
    """

    alternative_player: str = None
    "Ссылка на альтернативный плеер"
    host: str = None
    "Имена предпочитаемых серверов для построения ссылок на поток и скачивание"
    episodes: Episodes = None
    "Количество вышедших серий"
    list: dict[str, Episode] | List[Episode] = None
    "Список релизов"
    rutube_playlist: dict[str, RutubeSerie] | List[RutubeSerie] = None
    "Список релизов на rutube"


@define()
class Quality:
    """
    Объект, содержащий информацию о разрешении, кодировщике и типе релиза
    """

    string: str = None
    "Полная информация о качестве"
    type: str = None  # TODO: Enum!
    "Тип релиза"
    resolution: str = None
    "Разрешение серии"
    encoder: str = None
    "Название кодировщика"
    lq_audio: bool = None
    "Используется ли аудио дорожка с пониженным битрейтом"


@define()
class TorrentFile:
    """
    Объект с информацией о торрент файле
    """

    file: str = None
    "Имя файла"
    size: int = None
    "Размер файла в байтах"
    offset: int = None
    "Смещение в байтах относительно предыдущего файла"


@define()
class TorrentMetaData:
    """
    Объект с метадатой о торренте
    """

    hash: str = None
    "Хеш торрент файла"
    name: str = None
    "Имя тайтла в торрент файле"
    announce: List[str] = None
    "Список трекеров"
    created_timestamp: int = None
    "Время создания торрента в UNIX timestamp"
    files_list: List[TorrentFile] = None
    "Список файлов в торренте"


@define()
class Torrent:
    """
    Объект с информацией о торренте
    """

    torrent_id: int = None
    "ID торрент файла"
    episodes: Episodes = None
    "Серии, содержащиеся в файле"
    quality: Quality = None
    "Информация о разрешении, кодировщике и типе релиза"
    leechers: int = None
    "Количество личей"
    seeders: int = None
    "Количество сидов"
    downloads: int = None
    "Количество загрузок"
    total_size: int = None
    "Размер файлов в торренте в байтах"
    url: str = None
    "Ссылка на торрент без домена"
    uploaded_timestamp: int = None
    "Время загрузки домена в формате UNIX timestamp"
    metadata: TorrentMetaData | None = None
    "Метаданные торрент файла"
    raw_base64_file: str = None
    "Торрент файл в формате base64"
    hash: str = None
    "Хэш торрент файла"


@define()
class Torrents:
    """
    Модель со списком торрентов и информации о сериях.
    """

    episodes: Episodes = None
    "Серии, содержащиеся в файле"
    list: List[Torrent] = None
    "Список с информацией о торрент файлах"


@define()
class TitleDescription:
    """
    Объект с описанием тайтла
    """
    html: str = None
    "Описание тайтла в виде html"
    no_view_order: str = None
    "Описание тайтла в виде текста без дополнительного форматирования и порядка просмотра"
    plain: str = None
    "Описание тайтла без дополнительного форматирования"


@define()
class Title:
    """
    Объект тайтла
    """

    id: int = None
    "ID тайтла"
    code: str = None
    "Код тайтла"
    names: TitleNames = None
    "Названия тайтла"
    announce: str = None
    "Объявление для тайтла"
    status: TitleStatus = None
    "Статус тайтла"
    posters: Posters = None
    "Информация о постерах"
    updated: int = None
    "Время последнего обновления тайтла в формате UNIX timestamp"
    last_change: int = None
    "Время последнего изменения тайтла в формате UNIX timestamp"
    type: TitleType = None
    "Информация о типе тайтла"
    genres: List[str] = None
    "Список жанров тайтла"
    team: TitleTeam = None
    "Члены команды, работавшие над тайтлом"
    season: Season = None
    "Информация о сезоне"
    description: str = None
    "Описание тайтла"
    in_favorites: int = None
    "Сколько раз тайтл добавили в избранное"
    blocked: Blocked = None
    "Информация о блокировке тайтла"
    player: Player = None
    "Информация о плеере"
    torrents: Torrents = None
    "Информация о торрентах"

    @property
    def url(self) -> str:
        """
        Возвращает полную ссылку на тайтл
        """
        return f"https://anilibria.tv/release/{self.code}.html"
