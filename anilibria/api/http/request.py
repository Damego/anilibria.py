from json import loads

from aiohttp import ClientSession

from ..error import HTTPException


_session = ClientSession()


class Request:
    session: ClientSession = _session

    def __init__(self, proxy: str = None) -> None:
        self.proxy = proxy

    async def request(self, method: str, url: str, payload: str = "", **kwargs):
        print(method, f"{url}?{payload}", kwargs)
        if self.proxy is not None:
            kwargs["proxy"] = self.proxy
        async with _session.request(method, url + payload, **kwargs) as response:
            raw = await response.text()
            data = loads(raw)
            if error := data.get("error"):
                raise HTTPException(error["code"], error["message"])
            return data
