from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    find_string: str = ""
    x_wbaas_token: str = ""

    def show_settings(self) -> None:
        env_src = self.model_config.get("env_file")
        if Path(env_src).exists():
            env_src = Path(env_src).resolve()
        else:
            env_src = "Unknown source"

        print(f'Loaded settings from "{env_src}":')
        print(f' - {self.find_string=}')
        print(f' - {self.x_wbaas_token=}')
        print()


settings = Settings()
settings.show_settings()
