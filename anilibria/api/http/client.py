from .request import Request
from .other import SomeRequest
from .public import PublicRequest

class HTTPCLient(SomeRequest, PublicRequest):
    def __init__(self, proxy: str = None) -> None:
        self.proxy = proxy
        self.request = Request(proxy)
        SomeRequest.__init__(self)
        PublicRequest.__init__(self)

        
