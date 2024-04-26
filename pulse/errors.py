from .types import APIErrorData
from typing import Dict, Type


class APIError(Exception):
    code: str

    def __init__(self, data: APIErrorData):
        super().__init__(data.error)
        self.code = data.code


class TokenNotFoundError(APIError):
    pass


class TokenUsedError(APIError):
    pass


class TokenExpiredError(APIError):
    pass


error_map: Dict[str, Type[APIError]] = {
    "TOKEN_NOT_FOUND": TokenNotFoundError,
    "TOKEN_USED": TokenUsedError,
    "TOKEN_EXPIRED": TokenExpiredError,
}
