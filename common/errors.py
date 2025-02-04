from typing import Any
from pydantic import BaseModel
from common.responses import BaseResponse


class APIError(BaseModel):
    detail: Any
    error_type: str | None = "INTERNAL_SERVER_ERROR"


class APIErrorResponse(BaseResponse):
    error: APIError


class APIErrorException(Exception):
    def __init__(
        self, detail: str, status_code: int, error_type: str | None = None
    ) -> None:
        self.detail = detail
        self.status_code = status_code
        self.error_type = error_type
