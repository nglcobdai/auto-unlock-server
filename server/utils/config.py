import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    API_VERSION: str
    OPENAPI_URL: str | None = None

    SWITCH_BOT_TOKEN: str
    SWITCH_BOT_SECRET: str
    UNLOCK_BOT_ID: str
    CALL_BOT_ID: str
    TIMEOUT: int

    MONGODB_HOST_NAME: str
    MONGODB_PORT: int
    MONGODB_ROOT_USER_NAME: str
    MONGODB_ROOT_USER_PWD: str
    MONGODB_DATABASE: str
    MONGODB_USER_NAME: str
    MONGODB_USER_PWD: str
    DATADRIVE: str

    WHISPER_MODEL: str
    SECRET_PHRASE: str
    AUTHENTICATION_THRESHOLD: float

    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENV', 'dev')}",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def __init__(self, **data):
        super().__init__(**data)
        self.OPENAPI_URL = f"/{self.API_VERSION}/openapi.json"
