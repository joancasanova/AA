# app/application/benchmarking/analysis.py
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from scipy import stats
from collections import defaultdict

from .types import BenchmarkResult, MetricType
from app.domain.entities import VerificationMethodType

@dataclass
class ErrorAnalysis:
    error_patterns: Dict[str, int]
    common_failures: List[Dict[str, Any]]
    error_rate_by_method: Dict[str, float]
    error_examples: Dict[str, List[str]]

@dataclass
class PerformanceAnalysis:
    processing_times: Dict[str, Dict[str, float]]  # By stage
    token_usage: Dict[str, int]  # By stage
    memory_usage: Dict[str, float]  # By stage
    bottlenecks: List[Dict[str, Any]]

@dataclass
class StatisticalAnalysis:
    confidence_intervals: Dict[str, Dict[str, tuple]]  # By metric and label
    significance_tests: Dict[str, Dict[str, float]]  # Between configurations
    variance_analysis: Dict[str, Any]

@dataclass
class DataCharacteristicsAnalysis:
    input_length_impact: Dict[str, float]
    complexity_scores: Dict[str, float]
    edge_cases: List[Dict[str, Any]]
    performance_by_category: Dict[str, Dict[str, float]]

class AdvancedAnalyzer:
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level

    def analyze_errors(self, result: BenchmarkResult) -> ErrorAnalysis:
        error_patterns = defaultdict(int)
        common_failures = []
        error_rate_by_method = defaultdict(float)
        error_examples = defaultdict(list)

        for execution in result.execution_results:
            for stage in execution.stages_results:
                if stage.stage_type.value == "verify":
                    for output in (stage.output_data if isinstance(stage.output_data, list) else [stage.output_data]):
                        # Analyze verification failures
                        if output.verification_methods_failed:
                            # Track error patterns
                            error_key = "_".join(sorted(output.verification_methods_failed))
                            error_patterns[error_key] += 1
                            
                            # Track method-specific error rates
                            for method in output.verification_methods_failed:
                                error_rate_by_method[method] += 1
                            
                            # Collect error examples
                            if hasattr(stage.input_data, 'response'):
                                error_examples[error_key].append(stage.input_data.response[:200])  # First 200 chars

        # Normalize error rates
        total_verifications = len(result.execution_results)
        error_rate_by_method = {
            method: count / total_verifications 
            for method, count in error_rate_by_method.items()
        }

        # Identify common failure patterns
        for pattern, count in sorted(error_patterns.items(), key=lambda x: x[1], reverse=True)[:5]:
            common_failures.append({
                "pattern": pattern,
                "count": count,
                "percentage": (count / total_verifications) * 100
            })

        return ErrorAnalysis(
            error_patterns=dict(error_patterns),
            common_failures=common_failures,
            error_rate_by_method=error_rate_by_method,
            error_examples=dict(error_examples)
        )

    def analyze_performance(self, result: BenchmarkResult) -> PerformanceAnalysis:
        processing_times = defaultdict(list)
        token_usage = defaultdict(int)
        memory_usage = defaultdict(float)
        bottlenecks = []

        for execution in result.execution_results:
            prev_timestamp = None
            for stage in execution.stages_results:
                # Calculate processing time
                current_timestamp = datetime.fromisoformat(stage.timestamp)
                if prev_timestamp:
                    duration = (current_timestamp - prev_timestamp).total_seconds()
                    processing_times[stage.stage_type.value].append(duration)
                prev_timestamp = current_timestamp

                # Estimate token usage (if available in output metadata)
                if hasattr(stage.output_data, 'token_usage'):
                    token_usage[stage.stage_type.value] += stage.output_data.token_usage

        # Identify bottlenecks
        for stage_type, times in processing_times.items():
            avg_time = np.mean(times)
            if avg_time > np.mean([np.mean(t) for t in processing_times.values()]) * 1.5:
                bottlenecks.append({
                    "stage": stage_type,
                    "avg_time": avg_time,
                    "percentile_95": np.percentile(times, 95)
                })

        return PerformanceAnalysis(
            processing_times={k: {"mean": np.mean(v), "std": np.std(v)} for k, v in processing_times.items()},
            token_usage=dict(token_usage),
            memory_usage=dict(memory_usage),
            bottlenecks=bottlenecks
        )

    def analyze_statistics(
        self,
        result: BenchmarkResult,
        comparison_result: Optional[BenchmarkResult] = None
    ) -> StatisticalAnalysis:
        confidence_intervals = {}
        significance_tests = {}
        variance_analysis = {}

        # Calculate confidence intervals for each metric
        for metric in result.metrics:
            if metric.label not in confidence_intervals:
                confidence_intervals[metric.label] = {}
            
            # Calculate CI using bootstrap
            values = self._get_metric_values(result, metric.metric_type, metric.label)
            if values:
                ci = self._calculate_confidence_interval(values)
                confidence_intervals[metric.label][metric.metric_type.value] = ci

        # Perform significance tests if comparison result is provided
        if comparison_result:
            for metric in result.metrics:
                values1 = self._get_metric_values(result, metric.metric_type, metric.label)
                values2 = self._get_metric_values(comparison_result, metric.metric_type, metric.label)
                
                if values1 and values2:
                    t_stat, p_value = stats.ttest_ind(values1, values2)
                    significance_tests[f"{metric.label}_{metric.metric_type.value}"] = {
                        "t_statistic": t_stat,
                        "p_value": p_value
                    }

        # Perform variance analysis
        for metric in result.metrics:
            values = self._get_metric_values(result, metric.metric_type, metric.label)
            if values:
                variance_analysis[f"{metric.label}_{metric.metric_type.value}"] = {
                    "variance": np.var(values),
                    "std_dev": np.std(values)
                }

        return StatisticalAnalysis(
            confidence_intervals=confidence_intervals,
            significance_tests=significance_tests,
            variance_analysis=variance_analysis
        )

    def analyze_data_characteristics(self, result: BenchmarkResult) -> DataCharacteristicsAnalysis:
        input_length_impact = {}
        complexity_scores = {}
        edge_cases = []
        performance_by_category = defaultdict(lambda: defaultdict(list))

        for execution in result.execution_results:
            # Analyze input characteristics
            input_data = execution.stages_results[0].input_data
            if hasattr(input_data, 'response'):
                length = len(input_data.response)
                # Calculate performance metrics based on input length
                performance = self._calculate_performance_metrics(execution)
                
                # Track performance by input length category
                length_category = self._categorize_length(length)
                for metric, value in performance.items():
                    performance_by_category[length_category][metric].append(value)
                
                # Identify edge cases
                if self._is_edge_case(performance):
                    edge_cases.append({
                        "input_length": length,
                        "performance": performance,
                        "sample": input_data.response[:200]  # First 200 chars
                    })

        # Calculate average performance by category
        final_performance_by_category = {}
        for category, metrics in performance_by_category.items():
            final_performance_by_category[category] = {
                metric: np.mean(values) for metric, values in metrics.items()
            }

        return DataCharacteristicsAnalysis(
            input_length_impact=self._calculate_length_impact(performance_by_category),
            complexity_scores=complexity_scores,
            edge_cases=edge_cases,
            performance_by_category=final_performance_by_category
        )

    def _calculate_confidence_interval(self, values: List[float]) -> tuple:
        """Calculate confidence interval using bootstrap"""
        alpha = 1 - self.confidence_level
        lower = np.percentile(values, alpha/2 * 100)
        upper = np.percentile(values, (1-alpha/2) * 100)
        return (lower, upper)

    def _get_metric_values(
        self,
        result: BenchmarkResult,
        metric_type: MetricType,
        label: str
    ) -> List[float]:
        """Extract all values for a specific metric and label"""
        values = []
        for execution in result.execution_results:
            for stage in execution.stages_results:
                if hasattr(stage.output_data, 'metrics'):
                    for metric in stage.output_data.metrics:
                        if metric.metric_type == metric_type and metric.label == label:
                            values.append(metric.value)
        return values

    def _calculate_performance_metrics(self, execution: Any) -> Dict[str, float]:
        """Calculate performance metrics for an execution"""
        metrics = {}
        for stage in execution.stages_results:
            if stage.stage_type.value == "verify":
                if hasattr(stage.output_data, 'metrics'):
                    for metric in stage.output_data.metrics:
                        metrics[metric.metric_type.value] = metric.value
        return metrics

    def _categorize_length(self, length: int) -> str:
        """Categorize input length into buckets"""
        if length < 100:
            return "short"
        elif length < 500:
            return "medium"
        else:
            return "long"

    def _is_edge_case(self, performance: Dict[str, float]) -> bool:
        """Determine if a case is an edge case based on performance"""
        return any(value < 0.5 or value > 0.95 for value in performance.values())

    def _calculate_length_impact(
        self,
        performance_by_category: Dict[str, Dict[str, List[float]]]
    ) -> Dict[str, float]:
        """Calculate the impact of input length on performance"""
        impact = {}
        metrics = list(next(iter(performance_by_category.values())).keys())
        
        for metric in metrics:
            # Calculate correlation between length category and performance
            categories = list(performance_by_category.keys())
            values = [np.mean(performance_by_category[cat][metric]) for cat in categories]
            
            if len(categories) > 1:
                correlation = np.corrcoef(range(len(categories)), values)[0, 1]
                impact[metric] = correlation
            
        return impact