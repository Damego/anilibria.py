from asyncio import get_event_loop, get_running_loop, new_event_loop
from typing import List, Union, Optional
from logging import getLogger
from sys import version_info

from aiohttp import WSMessage, ClientWebSocketResponse, WSMsgType
from aiohttp.http import WS_CLOSED_MESSAGE

from .events import TitleUpdateEvent, PlayListUpdateEvent, EncodeEvent, EventType, TorrentUpdateEvent
from ..http import HTTPClient
from ..dispatch import EventDispatcher


log = getLogger("anilibria.gateway")
URL = "ws://api.anilibria.tv/v2/ws/"


class WebSocketClient:
    """
    Клиент для управления вебсокетом.
    """
    def __init__(self, proxy: str = None):
        try:
            self._loop = get_event_loop() if version_info < (3, 10) else get_running_loop()
        except RuntimeError:
            self._loop = new_event_loop()
        self._http = HTTPClient(proxy)
        self._listener = EventDispatcher()
        self.proxy: str = proxy
        self._client: ClientWebSocketResponse = None
        self._closed: bool = False
        self._subscribes: List[dict] = None
        self.api_version: str = None

    async def run(self):
        """
        Запускает вебсокет.
        """
        await self.__connect()

    async def __connect(self):
        """
        Устанавливает соединение с вебсокетом.

        .. warning::
           Не пытайтесь самостоятельно использовать этот метод!
        """
        async with self._http.request.session.ws_connect(URL) as self._client:
            log.debug("Connected to websocket")
            self._closed = self._client._closed
            if self._closed:
                await self.__connect()

            while not self._closed:
                data = await self.__receive_packet_data()
                if data is None:
                    continue
                if self._client is None or data == WS_CLOSED_MESSAGE:
                    await self.__connect()
                    break

                await self.__dispatch_events(data)

    async def __receive_packet_data(self) -> Optional[Union[dict, WSMessage]]:
        """
        Принимает пакет данных и возвращает словарь с данными или пустое значение

        .. warning::
           Не пытайтесь самостоятельно использовать этот метод!

        :return:
        """
        packet: WSMessage = await self._client.receive()
        if packet.type == WSMsgType.CLOSE:
            await self._client.close()
            return WS_CLOSED_MESSAGE

        if packet.type != WSMsgType.TEXT:
            # I need this for a moment because message types are not documented in the API
            # and I should to wait for a new event a long time
            log.warning(packet)
            return

        return packet.json() if packet.data and isinstance(packet.data, str) else None

    async def __dispatch_events(self, data: dict):
        """
        Принимает словарь с данными об ивенте и диспатчит их.

        .. warning::
           Не пытайтесь самостоятельно использовать этот метод!

        :param data: Словарь с данными об ивенте
        :type data: dict
        """
        self._listener.dispatch("on_raw_packet", data)

        type = data.get("type")
        if type is None:
            return await self.__dispatch_other_events(data)

        event_name = f"on_{type}"
        if type == EventType.TITLE_UPDATE:
            self._listener.dispatch(event_name, TitleUpdateEvent(**data[type]))
        elif type == EventType.PLAYLIST_UPDATE:
            event_model = PlayListUpdateEvent(**data[type])
            self._listener.dispatch(event_name, event_model)
            await self.__dispatch_new_series(event_model, data[type])
        elif type in [
            EventType.ENCODE_START,
            EventType.ENCODE_END,
            EventType.ENCODE_PROGRESS,
            EventType.ENCODE_FINISH
        ]:
            self._listener.dispatch(event_name, EncodeEvent(**data[type]))
        elif type == EventType.TORRENT_UPDATE:
            self._listener.dispatch(event_name, TorrentUpdateEvent(**data[type]))
        else:
            self._listener.dispatch(event_name, data)
            log.debug(f"Not documented event type {type} dispatched with data: {data}")

    async def __dispatch_new_series(self, event_model: PlayListUpdateEvent, data: dict):
        """
        Диспатчит ивент ``on_title_serie`` и вызывает функции с подпиской на тайтл, если найдёт

        .. warning::
           Не пытайтесь самостоятельно использовать этот метод!

        :param event_model:
        :param data:
        :return:
        """
        if not event_model.updated_episode:
            return
        hls = event_model.updated_episode.hls
        if not hls.fhd or not hls.hd:  # Can `or not hls.sd` be removed?
            return
        self._listener.dispatch("on_title_serie", event_model)

        if "on_subscription_title_serie" not in self._listener.events:
            return
        events = self._listener.events["on_subscription_title_serie"]
        title_data = data["updated_episode"]
        for event in events:
            filled_data = event["data"]
            if filled_data is None:
                continue  # Can be data is None?
            is_equal = self.check_equal(filled_data, title_data)
            if not is_equal:
                continue
            await event["coro"](event_model)  # It should be called in the Dispatcher but im not smart to do this.

    def check_equal(self, checker: dict, verifiable: dict):
        """
        Проверяет, идентичны ли значения первого словаря ко второму.
        Для списков проверяет наличие первого во втором.

        :param checker: Словарь, по которому будут проходится значения
        :param verifiable: Словарь, по которому будут проверять значения.
        :return: True - Если всё идентично, False - если нет
        :rtype: bool
        """
        for key, value in checker.items():
            if verifiable.get(key, "MISSING") == "MISSING":  # Can be None btw
                return False
            value_2 = verifiable[key]  # Can be first None and value_2 will be None???
            if isinstance(value, (int, str)) and value != value_2:
                return False
            if isinstance(value, list) and not all(list_value in value_2 for list_value in value):
                return False
            if isinstance(value, dict):
                if not self.check_equal(value, value_2):
                    return False

    async def __dispatch_other_events(self, data: dict):
        """
        Диспатчит ивент ``on_connect``.

        .. warning::
           Не пытайтесь самостоятельно использовать этот метод!

        :param data: словарь с данными об ивенте
        :type data: dict
        """
        if api_version := data.get("api_version"):
            self.api_version = api_version
            log.debug(f"Successfully connected to API. API version {api_version}")
            self._listener.dispatch("on_connect")
        else:
            log.debug(f"Not documented event data: {data}")
