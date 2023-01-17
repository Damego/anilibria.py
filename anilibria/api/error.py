__all__ = ("HTTPException", "NoArgumentsError")


class HTTPException(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(f"HTTP error with code: {code}!\nMessage: {message}")


class NoArgumentsError(Exception):
    def __init__(self, *missed_args):
        super().__init__(f"Should be at least one argument of {', '.join(missed_args)}")
