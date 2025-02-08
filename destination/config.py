import os
from common.config import AppSettings


class DestinationSettings(AppSettings):
    DYNAMODB_DESTINATION_TABLE: str = os.getenv(
        "DYNAMODB_DESTINATION_TABLE", "airlineTable"
    )
    AIRLINES_ENDPOINT_URL: str = os.getenv(
        "AIRLINES_ENDPOINT_URL", "localhost:8000/airlines/api/v1/"
    )


app_settings = DestinationSettings()
