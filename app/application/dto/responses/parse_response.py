# application/dto/responses/parse_response.py
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from ....domain.model.value_objects.parse_result import ParseMatch, ParseMetrics

class ParseLocationResponse(BaseModel):
    start: int
    end: int
    line_number: Optional[int] = None

class ParseMatchResponse(BaseModel):
    value: str
    location: ParseLocationResponse
    rule_name: str
    confidence: float

class ParseMetricsResponse(BaseModel):
    total_matches: int
    execution_time: float
    chars_processed: int
    rules_matched: List[str]

class ParseResponse(BaseModel):
    parse_result: List[ParseMatchResponse]
    metrics: ParseMetricsResponse
    execution_time: float
    total_matches: int
    successful_rules: List[str]
    failed_rules: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)