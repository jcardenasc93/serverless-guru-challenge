from fastapi import status
from destination.config import app_settings
import requests


class AirlinesService:
    AIRLINES_ENDPOINT = app_settings.AIRLINES_ENDPOINT_URL

    @classmethod
    def check_airline(cls, airline_uuid: str) -> bool:
        """Checks if an airline exists for the given airline_uuid"""
        try:
            response = requests.get(url=f"{cls.AIRLINES_ENDPOINT}{airline_uuid}")
        except Exception as e:
            raise e
        if response.status_code != status.HTTP_200_OK:
            return False
        response_body = response.json()["data"]
        if response_body["uuid"] != airline_uuid:
            return False
        return True
