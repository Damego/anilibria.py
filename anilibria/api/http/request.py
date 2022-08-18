from json import loads, JSONDecodeError
from logging import getLogger

from aiohttp import ClientSession

from ..error import HTTPException


log = getLogger("anilibria.request")
__all__ = ["Request"]


class Request:
    def __init__(self, proxy: str = None) -> None:
        """

        :param proxy:
        """
        self.proxy = proxy
        self.session = ClientSession()

    async def request(self, method: str, url: str, data: dict = None, **kwargs):
        """
        :param method:
        :param url:
        :param data:
        :param kwargs:
        :return:
        """
        if self.proxy is not None:
            kwargs["proxy"] = self.proxy

        log.debug(
            f"Send {method} request to {url} with data: {data} and additional kwargs: {kwargs}"
        )
        async with self.session.request(method, url, params=data, **kwargs) as response:
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
