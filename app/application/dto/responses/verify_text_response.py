# application/dto/responses/verify_text_response.py
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from ....domain.model.entities.verification import VerificationMethodType, VerificationMode

class VerificationResultResponse(BaseModel):
    method_name: str
    method_type: VerificationMethodType
    passed: bool
    score: Optional[float] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime

class VerificationSummaryResponse(BaseModel):
    results: List[VerificationResultResponse]
    final_status: str
    verification_time: float
    success_rate: float
    passed_methods: List[str]
    failed_methods: List[str]

class VerifyTextResponse(BaseModel):
    verification_summary: VerificationSummaryResponse
    execution_time: float
    success_rate: float
    timestamp: datetime = Field(default_factory=datetime.now)