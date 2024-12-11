# domain/model/aggregates/benchmark_result.py
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from ..entities.benchmark import BenchmarkExecution, BenchmarkConfiguration
from ..value_objects.benchmark_metrics import BenchmarkMetrics

@dataclass(frozen=True)
class BenchmarkResult:
    id: str
    name: str
    executions: List[BenchmarkExecution]
    configuration: BenchmarkConfiguration
    created_at: datetime
    updated_at: datetime
    metrics: Optional[BenchmarkMetrics] = None
    tags: List[str] = None
    metadata: Dict[str, any] = None

    def latest_execution(self) -> Optional[BenchmarkExecution]:
        if not self.executions:
            return None
        return max(self.executions, key=lambda x: x.start_time)

    def successful_executions(self) -> List[BenchmarkExecution]:
        return [ex for ex in self.executions 
                if ex.success_rate() >= self.configuration.required_success_rate]

    def failed_executions(self) -> List[BenchmarkExecution]:
        return [ex for ex in self.executions 
                if ex.success_rate() < self.configuration.required_success_rate]

    def average_success_rate(self) -> float:
        if not self.executions:
            return 0.0
        return sum(ex.success_rate() for ex in self.executions) / len(self.executions)

    def total_execution_time(self) -> float:
        return sum(ex.duration() for ex in self.executions)

    def is_successful(self) -> bool:
        latest = self.latest_execution()
        if not latest:
            return False
        return latest.success_rate() >= self.configuration.required_success_rate