from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    API_VERSION: str
    OPENAPI_URL: str = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **data):
        super().__init__(**data)
        self.OPENAPI_URL = f"/api/{self.API_VERSION}/openapi.json"


settings = Settings()
