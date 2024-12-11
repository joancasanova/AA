# application/dto/requests/parse_request.py
from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from ....domain.model.entities.parsing import ParseMode, ParseScope, ParseStrategy

class ParseRuleRequest(BaseModel):
    name: str = Field(..., min_length=1)
    pattern: str = Field(..., min_length=1)
    mode: ParseMode
    scope: ParseScope = ParseScope.ALL_TEXT
    strategy: ParseStrategy = ParseStrategy.FIRST_MATCH
    fallback_value: Optional[str] = None

    @validator('name', 'pattern')
    def validate_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Field cannot be empty or only whitespace")
        return v.strip()

class ParseRequest(BaseModel):
    text: str = Field(..., min_length=1)
    rules: List[ParseRuleRequest] = Field(..., min_items=1)
    require_all_rules: bool = True

    class Config:
        schema_extra = {
            "example": {
                "text": "Sample text to parse",
                "rules": [
                    {
                        "name": "sample_rule",
                        "pattern": r"\w+",
                        "mode": "regex",
                        "scope": "all_text",
                        "strategy": "first_match"
                    }
                ],
                "require_all_rules": True
            }
        }