from datetime import datetime
from pydantic import BaseModel


class AirlineBase(BaseModel):
    name: str
    country: str


class AirlineCreateRequest(AirlineBase):
    pass


class AirlineUpdateRequest(AirlineBase):
    name: str | None = None
    country: str | None = None


class AirlineRead(AirlineBase):
    uuid: str
    created_at: str
    updated_at: str
