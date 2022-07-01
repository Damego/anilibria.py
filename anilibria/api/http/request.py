from json import loads
from logging import getLogger

from aiohttp import ClientSession

from ..error import HTTPException


log = getLogger("anilibria.request")
_session = ClientSession()


class Request:
    session: ClientSession = _session

    def __init__(self, proxy: str = None) -> None:
        """

        :param proxy:
        """
        self.proxy = proxy

    async def request(self, method: str, url: str, payload: str = "", **kwargs):
        """

        :param method:
        :param url:
        :param payload:
        :param kwargs:
        :return:
        """
        if self.proxy is not None:
            kwargs["proxy"] = self.proxy

        log.debug(f"Send {method} request to {url}?{payload} with data: {kwargs}")
        async with _session.request(method, f"{url}?{payload}", **kwargs) as response:
            raw = await response.text()
            data = loads(raw)
            log.debug(f"Got response from request {data}")
            if isinstance(data, dict) and (error := data.get("error")):
                raise HTTPException(error["code"], error["message"])
            return data
