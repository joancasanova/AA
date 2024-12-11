# app/application/benchmarking/types.py
from dataclasses import dataclass
from typing import Dict, List, Any
from enum import Enum

class MetricType(Enum):
    ACCURACY = "accuracy"
    PRECISION = "precision"
    RECALL = "recall"
    F1_SCORE = "f1_score"

@dataclass
class LabelConfiguration:
    label: str
    expected_status: str  # The expected verification status
    expected_methods_passed: List[str]  # Expected verification methods that should pass

@dataclass
class BenchmarkDataset:
    data: List[Dict[str, Any]]  # The actual data entries
    label_configs: List[LabelConfiguration]

@dataclass
class MetricResult:
    metric_type: MetricType
    value: float
    label: str

@dataclass
class BenchmarkResult:
    metrics: List[MetricResult]
    execution_results: List[Any]  # Will store ExecutionResult objects
    total_samples: int
    correct_predictions: Dict[str, int]  # Per label
    total_predictions: Dict[str, int]  # Per label
    execution_id: str
    timestamp: str