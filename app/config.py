from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    max_upload_bytes: int
    allowed_image_types_str: str = Field(alias='allowed_image_types')

    model_config = SettingsConfigDict(env_file=('.env', '.env.local'))

    @property
    def allowed_image_types(self) -> list[str]:
        return [mime.strip() for mime in self.allowed_image_types_str.split(',')]


settings = Settings()


settings = Settings()
