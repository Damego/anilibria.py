from ...const import __api_url__

__all__ = ("Route",)

V1_URL = "https://www.anilibria.tv/public"
V3_URL = f"https://{__api_url__}"


class Route:
    def __init__(self, method: str, endpoint: str, *, is_v1: bool = False):
        self.method: str = method
        self.endpoint: str = endpoint
        self._is_v1: bool = is_v1

    @property
    def url(self) -> str:
        url = V1_URL if self._is_v1 else V3_URL
        return f"{url}{self.endpoint}"
