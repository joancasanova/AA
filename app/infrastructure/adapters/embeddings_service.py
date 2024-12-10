# infrastructure/adapters/embeddings_service.py

from app.infrastructure.embeddings.embedder_model import EmbedderModel
from app.domain.ports.embeddings_port import EmbeddingsPort

def get_embedder(model_name:str="sentence-transformers/all-MiniLM-L6-v2") -> EmbeddingsPort:
    return EmbedderModel(model_name)
