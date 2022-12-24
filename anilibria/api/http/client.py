from .public import PublicRequest


__all__ = ("HTTPClient", )


class HTTPClient(PublicRequest):
    def __init__(self, proxy: str | None = None) -> None:
        PublicRequest.__init__(self, proxy)
