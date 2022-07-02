from asyncio import get_event_loop, get_running_loop, new_event_loop
from json import loads
from typing import List
from logging import getLogger
from sys import version_info

from aiohttp import WSMessage, ClientWebSocketResponse, WSMsgType
from aiohttp.http import WS_CLOSED_MESSAGE

from .events import TitleUpdateEvent, PlayListUpdateEvent, EncodeEvent, EventType, TorrentUpdateEvent
from ..http import HTTPCLient
from ..listener import EventListener


log = getLogger("anilibria.gateway")
URL = "ws://api.anilibria.tv/v2/ws/"


class WebSocketClient:
    def __init__(self, proxy: str = None):
        """
        Клиент для управления вебсокетом.

        :param proxy: Ссылка на прокси-сервер.
        """
        try:
            self._loop = get_event_loop() if version_info < (3, 10) else get_running_loop()
        except RuntimeError:
            self._loop = new_event_loop()
        self._http = HTTPCLient(proxy)
        self._listener = EventListener()
        self.proxy: str = proxy
        self._client: ClientWebSocketResponse = None
        self._closed: bool = False
        self._subscribes: List[dict] = None
        self.api_version: str = None

    async def run(self, subscribes: List[dict]):
        """
        Запускает вебсокет.

        :param subscribes: Список с данными о тайтлах, на которые вебсокет подпишется при запуске.
        """
        self._subscribes = subscribes
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
            if self._subscribes:
                await self.__subscribe_on_titles()

            if self._closed:
                await self.__connect()

            while not self._closed:
                packet = await self._client.receive()
                if self._client is None or packet in [WSMsgType.CLOSE, WS_CLOSED_MESSAGE]:
                    await self.__connect()
                    break
                await self._process_packet(packet)

    async def _process_packet(self, packet: WSMessage):
        """
        Принимает пакет и диспатчит ивенты.

        .. warning::
           Не пытайтесь самостоятельно использовать этот метод!

        :param packet: Пакет
        :type packet: WSMessage
        """
        data = loads(packet.data)
        self._listener.dispatch("on_raw_packet", data)

        type = data.get("type")
        if type is None:
            return await self._process_other_events(data)

        event_name = f"on_{type}"
        if type == EventType.TITLE_UPDATE:
            self._dispatch_title_update_event(data["title_update"])
        elif type == EventType.PLAYLIST_UPDATE:
            event = PlayListUpdateEvent(**data[type])
            self._listener.dispatch(event_name, event)
        elif type in [
            EventType.ENCODE_START,
            EventType.ENCODE_END,
            EventType.ENCODE_PROGRESS,
            EventType.ENCODE_FINISH
        ]:
            event = EncodeEvent(**data[type])
            self._listener.dispatch(event_name, event)
        elif type == EventType.TORRENT_UPDATE:
            event = TorrentUpdateEvent(**data[type])
            self._listener.dispatch(event_name, event)
        else:
            self._listener.dispatch(event_name, data)
            log.debug(f"Not documented event type {type} dispatched with data: {data}")

    def _dispatch_title_update_event(self, data: dict):
        """
        Диспачит ивенты ``on_title_update`` и ``on_title``.

        .. warning::
           Не пытайтесь самостоятельно использовать этот метод!

        :param data: Словарь с данными об ивенте
        :type data: dict
        """
        event_model = TitleUpdateEvent(**data)
        self._listener.dispatch("on_title_update", event_model)

        title_data = data["title"]
        events = self._listener.events
        for event in events:
            if event == "on_title":
                coro_data = events[event]["data"]
                if all(value == title_data[key] for key, value in coro_data.items()):
                    self._listener.dispatch("on_title", event_model)

    async def _process_other_events(self, data: dict):
        """
        Диспатчит ивент ``on_connect``

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
            log.debug(data)

    async def __subscribe_on_titles(self):
        """
        Подписывается на все тайтлы.

        .. warning::
           Не пытайтесь самостоятельно использовать этот метод!
        """
        for subscribe in self._subscribes:
            await self._subscribe(subscribe)
        self._subscribes = None

    async def _subscribe(self, data: dict):
        """
        Подписывается на тайтл, отправкой пакета

        .. warning::
           Не пытайтесь самостоятельно использовать этот метод!

        :param data: Словарь с данными о подписке.
        """
        await self._client.send_json(data)
        log.debug(f"Send json to websocket with data: {data}")
