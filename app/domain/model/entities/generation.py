# domain/model/entities/generation.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List

@dataclass(frozen=True)
class GenerationMetadata:
    model_name: str
    tokens_used: int
    generation_time: float
    timestamp: datetime = datetime.now()

@dataclass(frozen=True)
class GeneratedResult:
    content: str
    metadata: GenerationMetadata
    reference_data: Optional[Dict[str, str]] = None

    def contains_reference(self, text: str) -> bool:
        return text.lower() in self.content.lower()

    def word_count(self) -> int:
        return len(self.content.split())