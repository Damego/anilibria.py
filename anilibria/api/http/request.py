from json import loads, JSONDecodeError
from logging import getLogger

from aiohttp import ClientSession

from .route import Route
from ..error import HTTPException
from ...utils.serializer import prepare_payload


log = getLogger("anilibria.request")
__all__ = ["Request"]


class Request:
    def __init__(self, proxy: str = None) -> None:
        """

        :param proxy:
        """
        self.proxy = proxy
        self.session: ClientSession = None

    async def check_session(self):
        if self.session is None or self.session.closed:
            self.session = ClientSession()

    async def request(self, route: Route, params: dict = None, **kwargs):
        await self.check_session()

        if params:
            prepare_payload(params)

        if self.proxy is not None:
            kwargs["proxy"] = self.proxy

        log.debug(
            f"Send {route.method} request to {route.endpoint} endpoint with params: {params} and kwargs: {kwargs}"
        )
        async with self.session.request(route.method, route.url, params=params, **kwargs) as response:
            raw = await response.text()
            try:
                data = loads(raw)
            except JSONDecodeError:  # Can be RSS
                data = raw
            log.debug(f"Got response from request {data}")
            self.__catch_error(data)
            return data

    def __catch_error(self, data: dict):
        if not isinstance(data, dict):
            return
        if error := data.get("error"):
            raise HTTPException(error["code"], error["message"])
        if data.get("err"):
            raise HTTPException(0, data["mes"])
