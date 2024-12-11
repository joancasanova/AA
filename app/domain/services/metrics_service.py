# domain/services/metrics_service.py
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from ..model.value_objects.benchmark_metrics import (
    AccuracyMetrics, PerformanceMetrics, BenchmarkMetrics
)
from ..model.entities.verification import VerificationSummary

class MetricsService:
    def calculate_benchmark_metrics(
        self,
        verification_results: List[VerificationSummary],
        expected_statuses: List[str],
        start_time: datetime,
        end_time: datetime
    ) -> BenchmarkMetrics:
        # Calculate accuracy metrics
        tp = tn = fp = fn = 0
        total_verification_time = 0.0
        verification_times = []

        for result, expected in zip(verification_results, expected_statuses):
            # Collect verification times
            verification_times.append(result.verification_time)
            total_verification_time += result.verification_time

            # Calculate confusion matrix
            if result.final_status == expected:
                if expected == "confirmada":
                    tp += 1
                else:
                    tn += 1
            else:
                if expected == "confirmada":
                    fn += 1
                else:
                    fp += 1

        accuracy_metrics = AccuracyMetrics(
            true_positives=tp,
            true_negatives=tn,
            false_positives=fp,
            false_negatives=fn
        )

        # Calculate performance metrics
        performance_metrics = PerformanceMetrics(
            average_verification_time=sum(verification_times) / len(verification_times),
            max_verification_time=max(verification_times),
            min_verification_time=min(verification_times),
            total_execution_time=(end_time - start_time).total_seconds(),
            verification_count=len(verification_results)
        )

        return BenchmarkMetrics(
            accuracy=accuracy_metrics,
            performance=performance_metrics
        )