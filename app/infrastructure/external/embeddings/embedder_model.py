# infrastructure/external/embeddings/embedder_model.py
from typing import List, Optional
from datetime import datetime
import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer
import logging
from ....domain.ports.embeddings_port import EmbeddingsPort
from ....domain.model.value_objects.similarity_score import SimilarityScore

logger = logging.getLogger(__name__)

class EmbedderModel(EmbeddingsPort):
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: Optional[str] = None,
        cache_dir: Optional[str] = None
    ):
        self.model_name = model_name
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.cache_dir = cache_dir
        
        logger.info(f"Initializing EmbedderModel with {model_name} on {self.device}")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
            self.model = AutoModel.from_pretrained(model_name, cache_dir=cache_dir)
            self.model.to(self.device)
        except Exception as e:
            logger.error(f"Error initializing embedder model: {str(e)}")
            raise

    def get_similarity(self, text1: str, text2: str) -> SimilarityScore:
        try:
            emb1 = self._get_embedding(text1)
            emb2 = self._get_embedding(text2)
            
            # Calculate cosine similarity
            similarity = F.cosine_similarity(emb1, emb2).item()
            
            return SimilarityScore(
                value=similarity,
                method=self.model_name,
                reference_text=text1,
                compared_text=text2
            )
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            raise

    def get_embedding(self, text: str) -> List[float]:
        try:
            embedding = self._get_embedding(text)
            return embedding.squeeze().tolist()
        except Exception as e:
            logger.error(f"Error getting embedding: {str(e)}")
            raise

    def batch_similarities(
        self,
        reference_text: str,
        comparison_texts: List[str]
    ) -> List[SimilarityScore]:
        try:
            ref_embedding = self._get_embedding(reference_text)
            similarities = []
            
            # Process in batches
            batch_size = 32
            for i in range(0, len(comparison_texts), batch_size):
                batch = comparison_texts[i:i + batch_size]
                batch_embeddings = torch.cat([
                    self._get_embedding(text) for text in batch
                ])
                
                # Calculate similarities for the batch
                batch_similarities = F.cosine_similarity(
                    batch_embeddings,
                    ref_embedding.expand(len(batch), -1)
                )
                
                # Create SimilarityScore objects
                for text, sim in zip(batch, batch_similarities):
                    similarities.append(SimilarityScore(
                        value=sim.item(),
                        method=self.model_name,
                        reference_text=reference_text,
                        compared_text=text
                    ))
            
            return similarities
        except Exception as e:
            logger.error(f"Error calculating batch similarities: {str(e)}")
            raise

    def _get_embedding(self, text: str) -> torch.Tensor:
        # Tokenize and prepare input
        tokens = self.tokenizer(
            text,
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors='pt'
        ).to(self.device)
        
        # Get embeddings
        with torch.no_grad():
            output = self.model(**tokens)
        
        # Use CLS token embedding and normalize
        embedding = F.normalize(output.last_hidden_state[:, 0], p=2, dim=1)
        return embedding