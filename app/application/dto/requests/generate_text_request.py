# application/dto/requests/generate_text_request.py
from dataclasses import dataclass
from typing import Dict, Optional, List
from pydantic import BaseModel, Field, validator

class GenerateTextRequest(BaseModel):
    system_prompt: str = Field(..., min_length=1, max_length=2000)
    user_prompt: str = Field(..., min_length=1, max_length=2000)
    num_sequences: int = Field(default=1, ge=1, le=10)
    max_tokens: int = Field(default=100, ge=1, le=2000)
    temperature: float = Field(default=1.0, ge=0.0, le=2.0)
    reference_data: Optional[Dict[str, str]] = None
    stop_sequences: Optional[List[str]] = None

    @validator('system_prompt', 'user_prompt')
    def validate_prompts(cls, v):
        if not v.strip():
            raise ValueError("Prompt cannot be empty or only whitespace")
        return v.strip()

    class Config:
        schema_extra = {
            "example": {
                "system_prompt": "You are a helpful assistant.",
                "user_prompt": "Tell me about clean architecture.",
                "num_sequences": 1,
                "max_tokens": 100,
                "temperature": 1.0
            }
        }