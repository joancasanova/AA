# infrastructure/config/settings.py
from typing import Optional, Dict, Any, List
from pydantic import BaseSettings, Field

class LLMSettings(BaseSettings):
    MODEL_NAME: str = "gpt-3.5-turbo"
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 1.0
    
    class Config:
        env_prefix = "LLM_"

class EmbeddingsSettings(BaseSettings):
    MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    MAX_LENGTH: int = 512
    
    class Config:
        env_prefix = "EMBEDDINGS_"

class Settings(BaseSettings):
    # Basic app settings
    DEBUG: bool = False
    
    # Model settings
    llm: LLMSettings = LLMSettings()
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    
    # Optional output directory for saving results
    OUTPUT_DIR: str = "output"
    
    class Config:
        env_file = ".env"
        case_sensitive = True