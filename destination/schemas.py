from datetime import datetime
import uuid
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator


class DestinationBase(BaseModel):
    city: str
    country: str
    airline_uuid: str

    @field_validator("airline_uuid", mode="after")
    @classmethod
    def validate_airline_uuid(cls, value: str) -> str:
        try:
            uuid_obj = uuid.UUID(value)
            if uuid_obj.version == 4:
                return value
        except ValueError:
            raise RequestValidationError(
                [
                    {
                        "loc": ("body", "airline_uuid"),
                        "msg": "Invalid airline uuid value",
                        "type": "ValueError",
                    }
                ]
            )


class DestinationCreateRequest(DestinationBase):
    pass


class DestinationUpdateRequest(BaseModel):
    active: bool


class DestinationRead(DestinationBase):
    uuid: str
    active: bool
    created_at: str
    updated_at: str
