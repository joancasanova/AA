# infrastructure/config/settings.py
from typing import Optional, Dict, Any, List
from pydantic import BaseSettings, Field, validator
from pathlib import Path
import json
import yaml

class DatabaseSettings(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASSWORD: str = Field(..., env="DB_PASSWORD")
    DATABASE: str = "benchmark_db"
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    ECHO: bool = False

    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"

    class Config:
        env_prefix = "DB_"

class LLMSettings(BaseSettings):
    MODEL_NAME: str = "EleutherAI/gpt-neo-125M"
    MAX_LENGTH: int = 2048
    DEFAULT_TEMPERATURE: float = 1.0
    BATCH_SIZE: int = 4
    CACHE_DIR: Optional[str] = None
    DEVICE: Optional[str] = None

    class Config:
        env_prefix = "LLM_"

class EmbeddingsSettings(BaseSettings):
    MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    MAX_LENGTH: int = 512
    BATCH_SIZE: int = 32
    CACHE_DIR: Optional[str] = None
    DEVICE: Optional[str] = None

    class Config:
        env_prefix = "EMBEDDINGS_"

class CacheSettings(BaseSettings):
    BACKEND: str = "redis"
    HOST: str = "localhost"
    PORT: int = 6379
    PASSWORD: Optional[str] = None
    DEFAULT_TTL: int = 3600  # 1 hour
    MAX_MEMORY: str = "1gb"

    class Config:
        env_prefix = "CACHE_"

class AppSettings(BaseSettings):
    ENV: str = Field(..., env="APP_ENV")
    DEBUG: bool = False
    SECRET_KEY: str = Field(..., env="APP_SECRET_KEY")
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["*"]
    MAX_REQUEST_SIZE: int = 10 * 1024 * 1024  # 10MB

    class Config:
        env_prefix = "APP_"

class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    llm: LLMSettings = LLMSettings()
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    cache: CacheSettings = CacheSettings()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True