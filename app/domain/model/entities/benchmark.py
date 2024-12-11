# domain/model/entities/benchmark.py
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from .verification import VerificationSummary
from ..value_objects.benchmark_metrics import BenchmarkMetrics

@dataclass(frozen=True)
class BenchmarkConfiguration:
    name: str
    description: str
    verification_methods: List[str]
    required_success_rate: float
    max_verification_time: float
    tags: List[str] = None

@dataclass(frozen=True)
class BenchmarkEntry:
    input_text: str
    expected_status: str
    metadata: Dict[str, any]
    verification_summary: Optional[VerificationSummary] = None

@dataclass(frozen=True)
class BenchmarkExecution:
    entries: List[BenchmarkEntry]
    configuration: BenchmarkConfiguration
    start_time: datetime
    end_time: Optional[datetime] = None
    metrics: Optional[BenchmarkMetrics] = None

    def duration(self) -> float:
        if not self.end_time:
            return 0.0
        return (self.end_time - self.start_time).total_seconds()

    def success_rate(self) -> float:
        if not self.entries:
            return 0.0
        successful = sum(1 for entry in self.entries 
                        if entry.verification_summary 
                        and entry.verification_summary.final_status == entry.expected_status)
        return successful / len(self.entries)