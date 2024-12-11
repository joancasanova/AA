# application/dto/requests/verify_text_request.py
from dataclasses import dataclass
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, validator
from ....domain.model.entities.verification import VerificationMethodType, VerificationMode

class VerificationMethodRequest(BaseModel):
    name: str = Field(..., min_length=1)
    method_type: VerificationMethodType
    mode: VerificationMode
    thresholds: Optional[Dict[str, float]] = None
    reference_text: Optional[str] = None
    required_matches: Optional[int] = None

class VerifyTextRequest(BaseModel):
    text: str = Field(..., min_length=1)
    methods: List[VerificationMethodRequest] = Field(..., min_items=1)
    required_for_confirmed: int = Field(..., gt=0)
    required_for_review: int = Field(..., ge=0)
    context: Optional[Dict[str, any]] = None

    @validator('required_for_confirmed')
    def validate_required_counts(cls, v, values):
        if 'required_for_review' in values and v <= values['required_for_review']:
            raise ValueError("required_for_confirmed must be greater than required_for_review")
        return v

