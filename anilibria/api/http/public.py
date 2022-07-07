from .request import Request


URL = "https://www.anilibria.tv/public"
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
        """

        :param mail:
        :param password:
        :return:
        """
        payload: dict = {"mail": mail, "passwd": password}
        return await self.request.request("POST", f"{URL}/login.php", data=payload)
