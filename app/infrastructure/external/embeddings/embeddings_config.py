# infrastructure/external/embeddings/embeddings_config.py
from typing import Optional
from pydantic import BaseSettings

class EmbeddingsConfig(BaseSettings):
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    device: Optional[str] = None
    cache_dir: Optional[str] = None
    max_length: int = 512
    batch_size: int = 32

    class Config:
        env_prefix = "EMBEDDINGS_"