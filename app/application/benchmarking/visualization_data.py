# app/application/benchmarking/visualization_data.py
from typing import Dict, List, Any
from .types import BenchmarkResult, MetricType

class BenchmarkVisualizationData:
    @staticmethod
    def prepare_metrics_summary(result: BenchmarkResult) -> Dict[str, Any]:
        """
        Prepares metrics data in a format suitable for frontend visualization.
        Returns a structured format that can be easily consumed by various chart libraries.
        """
        return {
            "summary": {
                "total_samples": result.total_samples,
                "labels": list(result.total_predictions.keys()),
                "sample_distribution": [
                    {
                        "label": label,
                        "total": count,
                        "correct": result.correct_predictions.get(label, 0)
                    }
                    for label, count in result.total_predictions.items()
                ]
            },
            "metrics": {
                "per_label": [
                    {
                        "label": metric.label,
                        "metric": metric.metric_type.value,
                        "value": metric.value
                    }
                    for metric in result.metrics
                    if metric.label != "overall"
                ],
                "overall": [
                    {
                        "metric": metric.metric_type.value,
                        "value": metric.value
                    }
                    for metric in result.metrics
                    if metric.label == "overall"
                ]
            },
            "pipeline_stats": {
                "execution_time": {
                    "start": result.execution_results[0].start_time,
                    "end": result.execution_results[0].end_time
                },
                "stages": [
                    {
                        "stage_type": stage.stage_type.value,
                        "timestamp": stage.timestamp
                    }
                    for stage in result.execution_results[0].stages_results
                ] if result.execution_results else []
            }
        }

    @staticmethod
    def prepare_confusion_matrix_data(result: BenchmarkResult) -> Dict[str, Any]:
        """
        Prepares confusion matrix data for the frontend.
        For verify stages, this tracks expected vs actual verification statuses.
        """
        # Get unique verification statuses from results
        statuses = {"confirmada", "descartada", "a revisar"}
        
        # Initialize confusion matrix
        matrix_data = {
            "labels": list(result.total_predictions.keys()),
            "statuses": list(statuses),
            "matrix": []
        }
        
        return matrix_data

    @staticmethod
    def prepare_timeline_data(result: BenchmarkResult) -> List[Dict[str, Any]]:
        """
        Prepares timeline data of the benchmark execution.
        Useful for performance analysis in the frontend.
        """
        timeline = []
        for execution in result.execution_results:
            for stage in execution.stages_results:
                timeline.append({
                    "stage_type": stage.stage_type.value,
                    "timestamp": stage.timestamp,
                    "execution_id": stage.execution_id
                })
        return timeline