import os
from common.config import AppSettings


class AirlineSettings(AppSettings):
    DYNAMODB_AIRLINE_TABLE: str = os.getenv("DYNAMODB_AIRLINE_TABLE", "airlineTable")


app_settings = AirlineSettings()
