from datetime import datetime
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, root_validator


class AirlineBase(BaseModel):
    airline_name: str
    country: str


class AirlineCreateRequest(AirlineBase):
    pass


class AirlineUpdateRequest(BaseModel):
    airline_name: str | None = None
    country: str | None = None

    @root_validator(pre=True)
    def check_at_least_one_attr(cls, values):
        """Validates that at least one value is passed."""
        airline_name_v = values.get("airline_name")
        country_v = values.get("country")
        if airline_name_v is None and country_v is None:
            raise RequestValidationError(
                [
                    {
                        "loc": ("body",),
                        "msg": "You must provide at least airline_name or country value",
                        "type": "value_error",
                    }
                ]
            )
        return values


class AirlineRead(AirlineBase):
    uuid: str
    created_at: str
    updated_at: str
