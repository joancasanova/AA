# domain/exceptions/benchmark_error.py
from typing import Optional, Dict, Any, List
from .base_exception import DomainError

class BenchmarkError(DomainError):
    """Base class for benchmark-related errors."""
    def __init__(
        self,
        message: str,
        code: str = "BENCHMARK_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)

class BenchmarkConfigurationError(BenchmarkError):
    def __init__(
        self,
        config_issue: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Benchmark configuration error: {config_issue}",
            code="BENCHMARK_CONFIG_ERROR",
            details=details
        )

class InvalidDatasetError(BenchmarkError):
    def __init__(
        self,
        dataset_name: str,
        reason: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Invalid dataset '{dataset_name}': {reason}",
            code="INVALID_DATASET",
            details=details
        )

class BenchmarkExecutionError(BenchmarkError):
    def __init__(
        self,
        benchmark_id: str,
        error_description: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Error executing benchmark '{benchmark_id}': {error_description}",
            code="BENCHMARK_EXECUTION_ERROR",
            details=details
        )