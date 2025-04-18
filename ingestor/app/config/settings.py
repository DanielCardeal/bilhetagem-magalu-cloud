from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Ingestor"
    VERSION: str = "1.0.0"

    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 80

    DATABASE_URL: str = "sqlite:///ingestor.db"

    DEBUG: bool = False


def get_settings() -> Settings:
    return Settings()

