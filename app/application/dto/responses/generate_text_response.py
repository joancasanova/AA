# application/dto/responses/generate_text_response.py
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from ....domain.model.entities.generation import GeneratedResult

class GenerationMetadataResponse(BaseModel):
    model_name: str
    tokens_used: int
    generation_time: float
    timestamp: datetime

class GeneratedTextResponse(BaseModel):
    content: str
    metadata: GenerationMetadataResponse
    reference_data: Optional[Dict[str, str]] = None

class GenerateTextResponse(BaseModel):
    generated_texts: List[GeneratedTextResponse]
    total_tokens: int
    generation_time: float
    model_name: str
    timestamp: datetime = Field(default_factory=datetime.now)