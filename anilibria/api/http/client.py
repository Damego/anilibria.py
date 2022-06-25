from .request import Request
from .other import SomeRequest
from .public import PublicRequest

class HTTPCLient(SomeRequest, PublicRequest):
    def __init__(self) -> None:
        self.request = Request()
        SomeRequest.__init__(self)
        PublicRequest.__init__(self)

        
