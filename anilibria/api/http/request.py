from json import loads

from aiohttp import ClientSession

from ..error import HTTPException


_session = ClientSession()


class Request:
    session: ClientSession = _session

    def __init__(self) -> None:
        pass

    async def request(self, method: str, url: str, payload: str = "", **kwargs):
        print(method, url+payload, kwargs)
        async with _session.request(method, url + payload, **kwargs) as response:
            raw = await response.text()
            data = loads(raw)
            if error := data.get("error"):
                raise HTTPException(error["code"], error["message"])
            return data
