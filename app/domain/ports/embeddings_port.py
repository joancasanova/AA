# domain/ports/embeddings_port.py
from abc import ABC, abstractmethod
from typing import List
from ..model.value_objects.similarity_score import SimilarityScore

class EmbeddingsPort(ABC):
    @abstractmethod
    def get_similarity(self, text1: str, text2: str) -> SimilarityScore:
        """
        Calculate similarity between two texts using embeddings.
        
        Args:
            text1: First text to compare
            text2: Second text to compare
            
        Returns:
            SimilarityScore object containing the similarity value and metadata
        """
        pass
    
    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """
        Get the embedding vector for a given text.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        pass
    
    @abstractmethod
    def batch_similarities(self, reference_text: str, comparison_texts: List[str]) -> List[SimilarityScore]:
        """
        Calculate similarities between one reference text and multiple comparison texts.
        
        Args:
            reference_text: Text to compare against
            comparison_texts: List of texts to compare with reference
            
        Returns:
            List of SimilarityScore objects for each comparison
        """
        pass