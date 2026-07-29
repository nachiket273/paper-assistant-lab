"""
Configuration settings for the application.
"""

from pydantic import NonNegativeInt, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Chunking
    chunk_size: PositiveInt = 1000  # Number of characters per chunk
    chunk_overlap: NonNegativeInt = (
        200  # Number of overlapping characters between chunks
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="PAL_", extra="forbid"
    )


settings = Settings()
