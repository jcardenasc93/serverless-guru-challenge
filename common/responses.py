from typing import Any
from pydantic import BaseModel


class BaseResponse(BaseModel):
    err: Any | None = None
