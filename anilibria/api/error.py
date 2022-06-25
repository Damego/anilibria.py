class HTTPException(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message

        super().__init__(f"HTTP Error with code: {self.code}! Message: {self.message}")