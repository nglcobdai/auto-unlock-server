import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    API_VERSION: str
    OPENAPI_URL: str = None

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

    class Config:
        env = os.getenv("ENV", "dev")
        env_file = f".env.{env}"
        env_file_encoding = "utf-8"

    def __init__(self, **data):
        super().__init__(**data)
        self.OPENAPI_URL = f"/api/{self.API_VERSION}/openapi.json"


settings = Settings()
