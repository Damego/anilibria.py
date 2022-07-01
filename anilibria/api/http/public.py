from .request import Request


URL = "https://www.anilibria.tv/public"


class PublicRequest:
    request: Request

    def __init__(self, request: Request) -> None:
        """

        :param request:
        """
        self.request: Request = request

    async def login(self, mail: str, password: str) -> dict:
        """

        :param mail:
        :param password:
        :return:
        """
        payload: dict = {"mail": mail, "passwd": password}
        return await self.request.request("POST", f"{URL}/login.php", data=payload)

    # * В документации расписаны публичные методы, но им более 2х лет, и я не смог заставить их работать
    # * code: 400 Message: Unknown query
    # * В исходном коде сайта расписаны некоторые методы, но документацию на них не завезли.
    # * Поэтому они не будут реализованы.
