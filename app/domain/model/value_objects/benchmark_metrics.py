# domain/model/value_objects/benchmark_metrics.py
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass(frozen=True)
class AccuracyMetrics:
    true_positives: int
    true_negatives: int
    false_positives: int
    false_negatives: int

    @property
    def accuracy(self) -> float:
        total = self.true_positives + self.true_negatives + self.false_positives + self.false_negatives
        if total == 0:
            return 0.0
        return (self.true_positives + self.true_negatives) / total

    @property
    def precision(self) -> float:
        if self.true_positives + self.false_positives == 0:
            return 0.0
        return self.true_positives / (self.true_positives + self.false_positives)

    @property
    def recall(self) -> float:
        if self.true_positives + self.false_negatives == 0:
            return 0.0
        return self.true_positives / (self.true_positives + self.false_negatives)

    @property
    def f1_score(self) -> float:
        if self.precision + self.recall == 0:
            return 0.0
        return 2 * (self.precision * self.recall) / (self.precision + self.recall)

@dataclass(frozen=True)
class PerformanceMetrics:
    average_verification_time: float
    max_verification_time: float
    min_verification_time: float
    total_execution_time: float
    verification_count: int

    @property
    def verifications_per_second(self) -> float:
        if self.total_execution_time == 0:
            return 0.0
        return self.verification_count / self.total_execution_time

@dataclass(frozen=True)
class BenchmarkMetrics:
    accuracy: AccuracyMetrics
    performance: PerformanceMetrics
    timestamp: datetime = datetime.now()