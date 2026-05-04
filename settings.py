from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    SCOPES: list[str]
    SHEET_ID: str
    SHEET_READ_RANGE: str
    WRITE_START_CELL: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    YF_PERIOD: str
    YF_INTERVAL: str

    @property
    def key_path(self) -> Path:
        path = BASE_DIR / self.GOOGLE_APPLICATION_CREDENTIALS
        if not path.exists():
            raise FileNotFoundError(f"Credentials not found: {path}")
        return path

    model_config = SettingsConfigDict(
        env_file=".env",
        frozen=True
    )


settings = Settings()
