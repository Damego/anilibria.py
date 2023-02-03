from logging import getLogger

from aiohttp import ClientResponse, ClientSession
from orjson import JSONDecodeError, loads

from ...utils.serializer import prepare_payload
from ..error import HTTPException
from .route import Route

log = getLogger("anilibria.request")
__all__ = ("Request",)


class Request:
    def __init__(self, proxy: str | None = None) -> None:
        self.proxy: str | None = proxy
        self.session: ClientSession = None  # noqa

    async def create_session(self) -> ClientSession:
        if self.session is None or self.session.closed:
            self.session = ClientSession()

        return self.session

    async def request(self, route: Route, params: dict = None, **kwargs):
        await self.create_session()

        if params is not None:
            prepare_payload(params)

        if self.proxy is not None:
            kwargs["proxy"] = self.proxy

        log.debug(
            f"Send {route.method} request to {route.endpoint} endpoint with params: {params} and kwargs: {kwargs}"
        )

        async with self.session.request(
            route.method, route.url, params=params, **kwargs
        ) as response:
            data = await self._get_data(response)

            log.debug(f"Got response from request {data}")

            self._catch_error(data)

            return data

    @staticmethod
    async def _get_data(response: ClientResponse) -> dict | str:
        try:
            data = await response.json(loads=loads)
        except JSONDecodeError:  # Could be RSS
            data = await response.text()

        return data

    @staticmethod
    def _catch_error(data: dict):
        if not isinstance(data, dict):
            return

        if error := data.get("error"):
            raise HTTPException(error["code"], error["message"])

        if data.get("err"):
            raise HTTPException(0, data["mes"])
