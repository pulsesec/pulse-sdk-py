from .types import APIErrorData
from typing import Dict, Type


class PulseError(Exception):
    code: str

    def __init__(self, data: APIErrorData):
        super().__init__(data.error)
        self.code = data.code


class TokenNotFoundError(PulseError):
    pass


class TokenUsedError(PulseError):
    pass


class TokenExpiredError(PulseError):
    pass


error_map: Dict[str, Type[PulseError]] = {
    "TOKEN_NOT_FOUND": TokenNotFoundError,
    "TOKEN_USED": TokenUsedError,
    "TOKEN_EXPIRED": TokenExpiredError,
}
