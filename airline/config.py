from common.config import AppSettings


class AirlineSettings(AppSettings):
    TABLE_NAME: str = "airlineTable"


app_settings = AirlineSettings()
