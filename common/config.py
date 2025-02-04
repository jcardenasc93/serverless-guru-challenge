from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="APP_", extra="ignore", env_ignore_empty=True
    )

    ENVIRONMENT: Literal["local", "dev", "prod"] = "local"
    AWS_REGION: str = "us-east-2"
