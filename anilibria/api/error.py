class HTTPException(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message

        super().__init__(f"HTTP error with code: {self.code}!\nMessage: {self.message}")
