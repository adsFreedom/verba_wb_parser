from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    find_str: str = ""
    x_wbaas_token: str = ""

    def show_settings(self) -> None:
        print(f'{self.find_str=}')
        print(f'{self.x_wbaas_token=}')


settings = Settings()
settings.show_settings()
