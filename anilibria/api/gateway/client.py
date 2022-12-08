try:
    from orjson import loads
except ImportError:
    from json import loads

from asyncio import get_event_loop, get_running_loop, new_event_loop, AbstractEventLoop
from typing import List, Union, Optional
from logging import getLogger
from sys import version_info

from aiohttp import WSMessage, ClientWebSocketResponse, WSMsgType
from aiohttp.http import WS_CLOSED_MESSAGE
import trio
from trio import open_nursery, Nursery
from trio._core._run import NurseryManager  # noqa
from trio_websocket import open_websocket_url, WebSocketConnection


from .events import (
    TitleUpdateEvent,
    PlayListUpdateEvent,
    EncodeEvent,
    EventType,
    TorrentUpdateEvent,
    TitleSerieEvent,
)
from ..http import HTTPClient
from ..dispatch import EventDispatcher


log = getLogger("anilibria.gateway")
URL = "wss://api.anilibria.tv/v2.13/ws/"
__all__ = ["WebSocketClient"]


class GatewayClient:
    def __init__(self, proxy: str):
        self._nursery_manager: NurseryManager | None = None
        self._connection: WebSocketConnection | None = None
        self._closed: bool = None  # noqa
        self._stopped: bool = None  # noqa

        self._http: HTTPClient(proxy)

    async def __aenter__(self):
        self._nursery_manager = open_nursery()
        nursery: Nursery = await self._nursery_manager.__aenter__()
        nursery.start_soon(self.reconnect)

        return self

    async def __aexit__(self, *args):
        await self._nursery_manager.__aexit__(*args)

    async def reconnect(self):
        self._closed = True

        if self._closed:
            await self.connect()

    async def connect(self):
        self._stopped = False

        async with open_websocket_url(URL) as self._connection:
            self._closed = self._connection.closed

            if self._stopped:
                await self._connection.aclose()
            if self._closed:
                await self._match_error()

            while not self._closed:
                data = await self._receive_data()

                await self._track_data(data)

    async def _receive_data(self) -> dict:
        response = await self._connection.get_message()
        return loads(response)

    async def _track_data(self, data: dict):
        ...

    async def _match_error(self):
        code: int = self._connection.closed.code

        print("ERROR", code)


class WebSocketClient:
    """
    Клиент для управления вебсокетом.
    """

    def __init__(self, proxy: str = None):
        self._loop: AbstractEventLoop = self.__get_event_loop()
        self._http = HTTPClient(proxy)
        self.dispatcher = EventDispatcher()
        self.proxy: str = proxy
        self._client: ClientWebSocketResponse = None  # type: ignore
        self._closed: bool = False
        self._subscribes: List[dict] = None  # type: ignore
        self.api_version: str = None  # type: ignore

    def __get_event_loop(self):
        try:
            loop = get_event_loop() if version_info < (3, 10) else get_running_loop()
        except RuntimeError:
            loop = new_event_loop()
        return loop

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
        if packet.type == WSMsgType.CLOSED:
            return WS_CLOSED_MESSAGE

        return packet.json() if packet.data and isinstance(packet.data, str) else None

    async def __dispatch_events(self, data: dict):
        """
        Диспатчит ивенты

        .. warning::
           Не пытайтесь самостоятельно использовать этот метод!

        :param data: Словарь с данными об ивенте
        :type data: dict
        """
        self.dispatcher.dispatch("on_raw_packet", data)

        type = data.get("type")
        if type is None:
            return await self.__dispatch_other_events(data)

        event_name = f"on_{type}"
        event_model = self.__get_event_model(EventType(type), data[type])
        if event_model is not None:
            self.dispatcher.dispatch(event_name, event_model)
            if type == EventType.PLAYLIST_UPDATE:
                await self.__dispatch_title_serie(event_model)
        else:
            self.dispatcher.dispatch(event_name, data)
            log.debug(f"Not documented event type {type} dispatched with data: {data}")

    def __get_event_model(self, event_type: EventType, data: dict):
        events = {
            EventType.TITLE_UPDATE: TitleUpdateEvent,
            EventType.PLAYLIST_UPDATE: PlayListUpdateEvent,
            EventType.ENCODE_START: EncodeEvent,
            EventType.ENCODE_PROGRESS: EncodeEvent,
            EventType.ENCODE_END: EncodeEvent,
            EventType.ENCODE_FINISH: EncodeEvent,
            EventType.TORRENT_UPDATE: TorrentUpdateEvent,
        }
        return model(**data) if (model := events.get(event_type)) else None

    async def __dispatch_title_serie(self, event_model: PlayListUpdateEvent):
        """
        Диспатчит ивент ``on_title_serie``

        .. warning::
           Не пытайтесь самостоятельно использовать этот метод!

        :param event_model:
        :type event_model: PlayListUpdateEvent
        """

        # Cool(hehe no. pls help me) logic of checking new series
        if not self.is_new_serie(event_model):
            return

        title = await self._http.v2.get_title(id=event_model.id)
        event_model = TitleSerieEvent(title=title, episode=event_model.updated_episode)
        self.dispatcher.dispatch("on_title_serie", event_model)

    def is_new_serie(self, event: PlayListUpdateEvent):
        """
        Проверяет, это новая серия или перезалив/другое

        :param event:
        """
        if (
            event.updated_episode
            and ((hls := event.updated_episode.hls) and hls.fhd and hls.hd and hls.sd)
            and not event.diff.get("playlist")
        ):
            return True
        if (playlist := event.diff.get("playlist")) is None:
            return
        if (series := list(playlist.values())) is None:
            return
        if (not series) or (series and series[0].get("hls") is None):
            return
        hls_diff = series[0]["hls"]
        if all(v is not None for k, v in hls_diff.items()):
            return
        if event.updated_episode is None:
            return
        if not hls.fhd or not hls.hd or not hls.sd:
            return

        return True

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
            self.dispatcher.dispatch("on_connect")
        elif data.get("subscribe"):
            log.debug(f"Successfully subscribed! subscription_id={data['subscription_id']}")
        else:
            log.debug(f"Not documented event data: {data}")

    async def subscribe(self, data: dict):
        """
        Отправляет словарь с данными о подписке вебсокету

        :param data:
        :return:
        """
        await self._client.send_json(data)
