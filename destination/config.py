import os
from common.config import AppSettings


class DestinationSettings(AppSettings):
    DYNAMODB_DESTINATION_TABLE: str = os.getenv(
        "DYNAMODB_DESTINATION_TABLE", "airlineTable"
    )


app_settings = DestinationSettings()
