from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "My FastAPI App"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
