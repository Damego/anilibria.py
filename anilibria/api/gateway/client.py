from asyncio import get_event_loop, get_running_loop, new_event_loop
from typing import List, Union, Optional
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
                data = await self.__receive_packet_data()
                if data is None:
                    continue
                if self._client is None or data == WS_CLOSED_MESSAGE:
                    await self.__connect()
                    break

                await self.__dispatch_events(data)

    async def __receive_packet_data(self) -> Optional[Union[dict, WSMessage]]:
        packet: WSMessage = await self._client.receive()
        if packet.type == WSMsgType.CLOSE:
            await self._client.close()
            return WS_CLOSED_MESSAGE

        if packet.type != WSMsgType.TEXT:
            # I need this for a moment because message types are not documented in the API
            # and I should to wait for a new event a long time
            log.warning(packet)
            raise Exception

        return packet.json() if packet and isinstance(packet.data, str) else None

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
            self._listener.dispatch(event_name, PlayListUpdateEvent(**data[type]))
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

    async def __dispatch_other_events(self, data: dict):
        """
        Диспатчит ивенты ``on_connect``

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
