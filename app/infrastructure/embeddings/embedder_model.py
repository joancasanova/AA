# infrastructure/embeddings/embedder_model.py

import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer
from app.domain.ports.embeddings_port import EmbeddingsPort

class EmbedderModel(EmbeddingsPort):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def get_similarity(self, text1: str, text2:str) -> float:
        emb1 = self._get_embedding(text1)
        emb2 = self._get_embedding(text2)
        return (emb1 @ emb2.T).item()

    def _get_embedding(self, text: str) -> torch.Tensor:
        tokens = self.tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt').to(self.device)
        with torch.no_grad():
            output = self.model(**tokens)
        embedding = F.normalize(output.last_hidden_state[:, 0], p=2, dim=1)
        return embedding
