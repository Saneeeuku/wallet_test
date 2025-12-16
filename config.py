from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    UVC_HOST: str
    UVC_PORT: int
    UVC_RELOAD: bool

    model_config = SettingsConfigDict(env_file=Path(".env"))


settings = Settings()
