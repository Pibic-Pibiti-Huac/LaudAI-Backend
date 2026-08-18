from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PATH_FIREBASE_CREDENTIALS: str | None = None # O Pydantic mapeia direto o nome correto do .env

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()