from typing import List

from .attrs_utils import define
from .enums import SeasonCode, StatusCode, TitleCodeType

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
    "RutubeEpisode",
    "Player",
    "Quality",
    "TorrentFile",
    "TorrentMetaData",
    "Torrent",
    "Torrents",
    "Title",
    "Franchise",
    "FranchiseRelease",
    "TitleFranchise",
)


@define()
class TitleNames:
    """
    Объект, содержащий названия тайтла на различных языках.
    """

    ru: str | None = None
    "Название тайтла на русском языке"
    en: str | None = None
    "Название тайтла на английском языке"
    alternative: str | None = None
    "Название тайтла на альтернативном языке"


@define()
class TitleStatus:
    """
    Объект статуса тайтла
    """

    string: str | None = None
    "Представление статуса в виде строки"
    code: StatusCode | None = None
    "Код статуса"


@define()
class Poster:
    """
    Объект с моделью постера
    """

    url: str | None = None
    "Относительная ссылка на постер"
    raw_base64_file: str | None = None
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

    small: Poster | None = None
    "Постер маленького размера"
    medium: Poster | None = None
    "Постер среднего размера"
    original: Poster | None = None
    "Постер оригинального размера"


@define()
class TitleType:
    """
    Объект с информацией о типе тайтла.
    """

    full_string: str | None = None
    "Полная информация о типе в виде строки"
    code: TitleCodeType | None = None
    "Код типа"
    string: str | None = None
    "Тип тайтла в виде строки"
    episodes: int | None = None
    "Количество серий"
    length: str | None = None
    "Длина серии"


@define()
class TitleTeam:
    """
    Объект с участниками, которые принимали участие в переводе тайтла.
    """

    voice: List[str] | None = None
    "Участники, работавшие над озвучкой"
    translator: List[str] | None = None
    "Участники, работавшие над переводом"
    editing: List[str] | None = None
    "Участники, работавшие над субтитрами"
    decor: List[str] | None = None
    "Участники, работавшие над оформлением"
    timing: List[str] | None = None
    "Участники, работавшие над таймингом"


@define()
class Season:
    """
    Объект с информацией о сезоне тайтла.
    """

    string: str | None = None
    "Название сезона"
    code: SeasonCode | None = None
    "Код сезона"
    year: int | None = None
    "Год выпуска"
    week_day: int | None = None
    "День недели"


@define()
class Blocked:
    """
    Объект с информацией о статусе блокировки тайтла.
    """

    blocked: bool | None = False
    "Тайтл заблокирован на территории РФ"
    bakanim: bool | None = False
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

    fhd: str | None = None
    "Ссылка на видео в Full HD качестве"
    hd: str | None = None
    "Ссылка на видео в HD качестве"
    sd: str | None = None
    "Ссылка на видео в SD качестве"


@define()
class SerieSkips:
    """
    Объект с таймкодами для пропуска опенинга и эндинга.
    """

    opening: List[str] | None = None
    "Таймкоды для опенинга"
    ending: List[str] | None = None
    "Таймкоды для эндинга"


@define()
class Episode:
    """
    Объект, содержащий информацию о серии.
    """

    episode: int | None = None
    "Номер серии"
    created_timestamp: int | None = None
    "Время создания/изменения в формате UNIX timestamp"
    hls: HLS | None = None
    "Ссылки на серию"
    preview: str | None = None
    "Ссылка на превью серии"
    skips: SerieSkips | None = None
    "Таймкоды на пропуски"
    uuid: str
    "UUID эпизода"

    # TODO: Добавить свойство 'created_at' с datetime


@define()
class RutubeEpisode:
    """
    Объект с информацией о серии в rutube
    """

    created_timestamp: int | None = None
    "Время создания/изменения в формате UNIX timestamp"
    rutube_id: str | None = None  # TODO: Возможно ли из айди собрать ссылку?
    "ID серии"
    episode: int | None = None
    "Номер серии"


@define()
class Player:
    """
    Объект с информацией о плеере и сериях.
    """

    alternative_player: str | None = None
    "Ссылка на альтернативный плеер"
    host: str | None = None
    "Имена предпочитаемых серверов для построения ссылок на поток и скачивание"
    episodes: Episodes | None = None
    "Количество вышедших серий"
    list: dict[str, Episode] | List[Episode] = None
    "Список релизов"
    rutube: dict[str, RutubeEpisode] | List[RutubeEpisode] = None
    "Список релизов на rutube"


@define()
class Quality:
    """
    Объект, содержащий информацию о разрешении, кодировщике и типе релиза
    """

    string: str | None = None
    "Полная информация о качестве"
    type: str | None = None  # TODO: Enum!
    "Тип релиза"
    resolution: str | None = None
    "Разрешение серии"
    encoder: str | None = None
    "Название кодировщика"
    lq_audio: bool | None = None
    "Используется ли аудио дорожка с пониженным битрейтом"


@define()
class TorrentFile:
    """
    Объект с информацией о торрент файле
    """

    file: str | None = None
    "Имя файла"
    size: int | None = None
    "Размер файла в байтах"
    offset: int | None = None
    "Смещение в байтах относительно предыдущего файла"


@define()
class TorrentMetaData:
    """
    Объект с метадатой о торренте
    """

    hash: str | None = None
    "Хеш торрент файла"
    name: str | None = None
    "Имя тайтла в торрент файле"
    announce: List[str] | None = None
    "Список трекеров"
    created_timestamp: int | None = None
    "Время создания торрента в UNIX timestamp"
    files_list: List[TorrentFile] | None = None
    "Список файлов в торренте"


@define()
class Torrent:
    """
    Объект с информацией о торренте
    """

    torrent_id: int | None = None
    "ID торрент файла"
    episodes: Episodes | None = None
    "Серии, содержащиеся в файле"
    quality: Quality | None = None
    "Информация о разрешении, кодировщике и типе релиза"
    leechers: int | None = None
    "Количество личей"
    seeders: int | None = None
    "Количество сидов"
    downloads: int | None = None
    "Количество загрузок"
    total_size: int | None = None
    "Размер файлов в торренте в байтах"
    url: str | None = None
    "Ссылка на торрент без домена"
    uploaded_timestamp: int | None = None
    "Время загрузки домена в формате UNIX timestamp"
    metadata: TorrentMetaData | None = None
    "Метаданные торрент файла"
    raw_base64_file: str | None = None
    "Торрент файл в формате base64"
    hash: str | None = None
    "Хэш торрент файла"
    magnet: str | None = None
    "Магнитная ссылка для скачивания торрента"


@define()
class Torrents:
    """
    Модель со списком торрентов и информации о сериях.
    """

    episodes: Episodes | None = None
    "Серии, содержащиеся в файле"
    list: List[Torrent] | None = None
    "Список с информацией о торрент файлах"


@define()
class TitleDescription:
    """
    Объект с описанием тайтла
    """

    html: str | None = None
    "Описание тайтла в виде html"
    no_view_order: str | None = None
    "Описание тайтла в виде текста без дополнительного форматирования и порядка просмотра"
    plain: str | None = None
    "Описание тайтла без дополнительного форматирования"


@define()
class Franchise:
    id: str
    "UUID франшизы"
    name: str
    "Название франшизы"


@define()
class FranchiseRelease:
    id: int
    "ID тайтла"
    code: str
    "Код тайтла"
    names: TitleNames
    "Названия тайтла"
    ordinal: int
    "Порядковый номер в списке"


@define()
class TitleFranchise:
    franchise: Franchise
    "Объект с информацией о франшизе"
    releases: list[FranchiseRelease]
    "Список релизов франшизы"


@define()
class Title:
    """
    Объект тайтла
    """

    id: int | None = None
    "ID тайтла"
    code: str | None = None
    "Код тайтла"
    names: TitleNames | None = None
    "Названия тайтла"
    announce: str | None = None
    "Объявление для тайтла"
    status: TitleStatus | None = None
    "Статус тайтла"
    posters: Posters | None = None
    "Информация о постерах"
    updated: int | None = None
    "Время последнего обновления тайтла в формате UNIX timestamp"
    last_change: int | None = None
    "Время последнего изменения тайтла в формате UNIX timestamp"
    type: TitleType | None = None
    "Информация о типе тайтла"
    genres: List[str] | None = None
    "Список жанров тайтла"
    team: TitleTeam | None = None
    "Члены команды, работавшие над тайтлом"
    season: Season | None = None
    "Информация о сезоне"
    description: str | None = None
    "Описание тайтла"
    in_favorites: int | None = None
    "Сколько раз тайтл добавили в избранное"
    blocked: Blocked | None = None
    "Информация о блокировке тайтла"
    player: Player | None = None
    "Информация о плеере"
    torrents: Torrents | None = None
    "Информация о торрентах"
    franchises: list[TitleFranchise] | None = None
    "Список франшиз"

    @property
    def url(self) -> str:
        """
        Возвращает полную ссылку на тайтл
        """
        return f"https://anilibria.tv/release/{self.code}.html"
