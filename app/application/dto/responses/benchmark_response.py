# application/dto/responses/benchmark_response.py
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class AccuracyMetricsResponse(BaseModel):
    true_positives: int
    true_negatives: int
    false_positives: int
    false_negatives: int
    accuracy: float
    precision: float
    recall: float
    f1_score: float

class PerformanceMetricsResponse(BaseModel):
    average_verification_time: float
    max_verification_time: float
    min_verification_time: float
    total_execution_time: float
    verification_count: int
    verifications_per_second: float

class BenchmarkMetricsResponse(BaseModel):
    accuracy: AccuracyMetricsResponse
    performance: PerformanceMetricsResponse

class BenchmarkEntryResultResponse(BaseModel):
    input_text: str
    expected_status: str
    actual_status: str
    verification_time: float
    success: bool
    metadata: Dict[str, Any]

class BenchmarkResponse(BaseModel):
    execution_id: str
    start_time: datetime
    end_time: datetime
    total_entries: int
    successful_entries: int
    failed_entries: int
    execution_time: float
    metrics: BenchmarkMetricsResponse
    entries: List[BenchmarkEntryResultResponse]
    tags: Optional[List[str]] = None
