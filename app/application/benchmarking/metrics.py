# app/application/benchmarking/metrics.py
from typing import List, Dict, Set
from collections import defaultdict
from .types import MetricType, MetricResult, LabelConfiguration
import numpy as np

class MetricsCalculator:
    @staticmethod
    def calculate_metrics(
        predictions: Dict[str, int],  # Correct predictions per label
        label_configs: List[LabelConfiguration],
        total_per_label: Dict[str, int],  # Total predictions per label
        all_results: List[Dict[str, Any]] = None  # All verification results for detailed metrics
    ) -> List[MetricResult]:
        metrics = []
        all_labels = {config.label for config in label_configs}
        
        # Calculate per-label metrics
        for label_config in label_configs:
            label = label_config.label
            if label not in total_per_label or total_per_label[label] == 0:
                continue

            # Get true positives, false positives, etc.
            tp, fp, fn, tn = MetricsCalculator._get_confusion_matrix_values(
                label,
                label_configs,
                all_results,
                all_labels
            )

            # Accuracy for this label
            accuracy = (tp + tn) / (tp + fp + fn + tn) if (tp + fp + fn + tn) > 0 else 0
            metrics.append(MetricResult(
                metric_type=MetricType.ACCURACY,
                value=accuracy,
                label=label
            ))

            # Precision for this label
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            metrics.append(MetricResult(
                metric_type=MetricType.PRECISION,
                value=precision,
                label=label
            ))

            # Recall for this label
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            metrics.append(MetricResult(
                metric_type=MetricType.RECALL,
                value=recall,
                label=label
            ))

            # F1 Score for this label
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            metrics.append(MetricResult(
                metric_type=MetricType.F1_SCORE,
                value=f1,
                label=label
            ))

        # Calculate overall metrics (macro average)
        overall_metrics = defaultdict(list)
        for metric in metrics:
            overall_metrics[metric.metric_type].append(metric.value)

        for metric_type, values in overall_metrics.items():
            metrics.append(MetricResult(
                metric_type=metric_type,
                value=np.mean(values),
                label="overall"
            ))

        return metrics

    @staticmethod
    def _get_confusion_matrix_values(
        target_label: str,
        label_configs: List[LabelConfiguration],
        all_results: List[Dict[str, Any]],
        all_labels: Set[str]
    ) -> tuple:
        """
        Calculate confusion matrix values for a specific label.
        Returns (true_positives, false_positives, false_negatives, true_negatives)
        """
        if not all_results:
            return (0, 0, 0, 0)

        true_positives = 0
        false_positives = 0
        false_negatives = 0
        true_negatives = 0

        target_config = next(
            (config for config in label_configs if config.label == target_label),
            None
        )

        if not target_config:
            return (0, 0, 0, 0)

        for result in all_results:
            actual_label = result.get('label')
            predicted_status = result.get('predicted_status')
            predicted_methods = result.get('predicted_methods', [])

            # Check if this prediction matches the target configuration
            predicted_matches_target = (
                predicted_status == target_config.expected_status and
                set(predicted_methods) == set(target_config.expected_methods_passed)
            )

            if actual_label == target_label:
                if predicted_matches_target:
                    true_positives += 1
                else:
                    false_negatives += 1
            else:
                if predicted_matches_target:
                    false_positives += 1
                else:
                    true_negatives += 1

        return (true_positives, false_positives, false_negatives, true_negatives)

class MetricsAnalyzer:
    """Helper class for analyzing metrics and providing insights"""
    
    @staticmethod
    def get_performance_summary(metrics: List[MetricResult]) -> Dict[str, Any]:
        """
        Provides a summary of the metrics with insights about model performance
        """
        summary = {
            "overall_performance": {},
            "per_label_performance": defaultdict(dict),
            "potential_issues": []
        }

        # Collect metrics by label
        for metric in metrics:
            if metric.label == "overall":
                summary["overall_performance"][metric.metric_type.value] = metric.value
            else:
                summary["per_label_performance"][metric.label][metric.metric_type.value] = metric.value

        # Analyze for potential issues
        for label, label_metrics in summary["per_label_performance"].items():
            # Check for significant precision/recall imbalance
            if abs(label_metrics.get("precision", 0) - label_metrics.get("recall", 0)) > 0.2:
                summary["potential_issues"].append({
                    "label": label,
                    "issue": "precision_recall_imbalance",
                    "description": f"Significant imbalance between precision ({label_metrics.get('precision', 0):.2f}) "
                                 f"and recall ({label_metrics.get('recall', 0):.2f}) for label {label}"
                })

            # Check for poor F1 score
            if label_metrics.get("f1_score", 0) < 0.5:
                summary["potential_issues"].append({
                    "label": label,
                    "issue": "low_f1_score",
                    "description": f"Low F1 score ({label_metrics.get('f1_score', 0):.2f}) for label {label}"
                })

        return summary