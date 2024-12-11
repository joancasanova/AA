# application/dto/requests/benchmark_request.py
from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, validator
from ....domain.model.entities.verification import VerificationMethod

class BenchmarkEntryRequest(BaseModel):
    input_text: str = Field(..., min_length=1)
    expected_status: str = Field(..., regex="^(confirmada|descartada|a revisar)$")
    metadata: Dict[str, any] = Field(default_factory=dict)

class BenchmarkConfigRequest(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    verification_methods: List[str] = Field(..., min_items=1)
    required_success_rate: float = Field(..., ge=0.0, le=1.0)
    max_verification_time: float = Field(..., gt=0)
    tags: Optional[List[str]] = None

class BenchmarkRequest(BaseModel):
    configuration: BenchmarkConfigRequest
    entries: List[BenchmarkEntryRequest] = Field(..., min_items=1)
    tags: Optional[List[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "configuration": {
                    "name": "Sample Benchmark",
                    "description": "Testing verification methods",
                    "verification_methods": ["method1", "method2"],
                    "required_success_rate": 0.8,
                    "max_verification_time": 30.0,
                    "tags": ["test", "verification"]
                },
                "entries": [
                    {
                        "input_text": "Sample text to verify",
                        "expected_status": "confirmada",
                        "metadata": {"source": "test_data"}
                    }
                ]
            }
        }