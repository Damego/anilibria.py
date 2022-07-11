from .request import Request
from .v2 import V2Request
from .public import PublicRequest


__all__ = ["HTTPClient"]


class HTTPClient:
    def __init__(self, proxy: str = None) -> None:
        """
        :param proxy:
        """
        self.request = Request(proxy)
        self.v2 = V2Request(self.request)
        self.public = PublicRequest(self.request)
