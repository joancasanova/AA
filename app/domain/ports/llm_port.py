# domain/ports/llm_port.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from ..model.entities.generation import GeneratedResult

class LLMPort(ABC):
    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        num_sequences: int = 1,
        max_tokens: int = 100,
        temperature: float = 1.0,
        stop_sequences: Optional[List[str]] = None
    ) -> List[GeneratedResult]:
        """
        Generate text using the language model.
        
        Args:
            system_prompt: System-level instructions for the model
            user_prompt: User input/question
            num_sequences: Number of different sequences to generate
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            stop_sequences: Optional list of sequences that will stop generation
            
        Returns:
            List of GeneratedResult objects containing the generated texts and metadata
        """
        pass

    @abstractmethod
    def get_token_count(self, text: str) -> int:
        """
        Count the number of tokens in a text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Number of tokens
        """
        pass