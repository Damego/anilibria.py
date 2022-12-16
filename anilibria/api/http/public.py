from .request import Request
from ...const import __api_url__
from .route import Route

URL = f"https://{__api_url__}/public"
__all__ = ["PublicRequest"]


class PublicRequest:
    """
    Представляет собой запросы на сайт "https://www.anilibria.tv/public"
    Здесь не будут реализованы методы для "/api", так как существует v2, в котором точно такие же запросы,
    и к тому же документация к "/api" не обновлялась более двух лет.
    """

    request: Request

    def __init__(self, request: Request) -> None:
        self.request: Request = request

    async def login(self, mail: str, password: str) -> dict:
        payload: dict = {"mail": mail, "passwd": password}

        route = Route("POST", "")
        route._url = f"{URL}/login.php"

        return await self.request.request(route, data=payload)
