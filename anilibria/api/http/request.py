from logging import getLogger

from orjson import loads, JSONDecodeError
from httpx import AsyncClient, Response

from .route import Route
from ..error import HTTPException
from ...utils.serializer import prepare_payload


log = getLogger("anilibria.request")
__all__ = ("Request", )


class Request:
    def __init__(self, proxy: str = None) -> None:
        self.proxy: str = proxy
        self.session: AsyncClient = None  # noqa

    async def check_session(self):
        if self.session is None or self.session.is_closed:
            self.session = AsyncClient(proxies=self.proxy)

    async def request(self, route: Route, params: dict = None, **kwargs):
        await self.check_session()

        if params:
            prepare_payload(params)

        log.debug(
            f"Send {route.method} request to {route.endpoint} endpoint with params: {params} and kwargs: {kwargs}"
        )
        response = await self.session.request(route.method, route.url, params=params, **kwargs)
        data = self._get_data(response)

        log.debug(f"Got response from request {data}")

        self._catch_error(data)

        return data

    @staticmethod
    def _get_data(response: Response) -> dict | str:
        text = response.text

        try:
            data = loads(text)
        except JSONDecodeError:  # Could be RSS
            data = text

        return data

    @staticmethod
    def _catch_error(data: dict):
        if not isinstance(data, dict):
            return
        if error := data.get("error"):
            raise HTTPException(error["code"], error["message"])
        if data.get("err"):
            raise HTTPException(0, data["mes"])
