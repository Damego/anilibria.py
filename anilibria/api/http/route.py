from typing import Final

__all__ = ["Route"]

URL: Final = "http://api.anilibria.tv/v2"


class Route:
    def __init__(self, method: str, endpoint: str):
        self.method = method
        self.endpoint = endpoint

    @property
    def url(self) -> str:
        return f"{URL}{self.endpoint}"
