from .request import Request


URL = "https://www.anilibria.tv/public"

class PublicRequest:
    request: Request

    async def login(self, login: str, password: str) -> dict:
        payload: str = {
            "mail": login,
            "passwd": password
        }
        return await self.request.request("POST", f"{URL}/login.php", data=payload) 