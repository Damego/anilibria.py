from ...const import __api_url__

__all__ = ["Route"]

URL = f"https://{__api_url__}"


class Route:
    def __init__(self, method: str, endpoint: str):
        self.method = method
        self.endpoint = endpoint

    @property
    def url(self) -> str:
        return f"{URL}{self.endpoint}"
