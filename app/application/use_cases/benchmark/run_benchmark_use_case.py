# application/use_cases/benchmark/run_benchmark_use_case.py
from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass
from ....domain.model.entities.benchmark import BenchmarkConfiguration, BenchmarkEntry, BenchmarkExecution
from ....domain.services.metrics_service import MetricsService
from ....domain.services.verifier_service import VerifierService
from ....domain.ports.logger_port import LoggerPort
from ....domain.ports.repository_port import RepositoryPort
from ....domain.exceptions.benchmark_error import BenchmarkConfigurationError

@dataclass
class RunBenchmarkRequest:
    configuration: BenchmarkConfiguration
    entries: List[BenchmarkEntry]
    tags: Optional[List[str]] = None

@dataclass
class RunBenchmarkResponse:
    execution_id: str
    start_time: datetime
    end_time: datetime
    total_entries: int
    successful_entries: int
    failed_entries: int
    execution_time: float

class RunBenchmarkUseCase:
    def __init__(
        self,
        verifier_service: VerifierService,
        metrics_service: MetricsService,
        repository: RepositoryPort,
        logger: LoggerPort
    ):
        self.verifier_service = verifier_service
        self.metrics_service = metrics_service
        self.repository = repository
        self.logger = logger

    def execute(self, request: RunBenchmarkRequest) -> RunBenchmarkResponse:
        self._validate_request(request)
        
        start_time = datetime.now()
        execution_id = f"bench_{start_time.strftime('%Y%m%d_%H%M%S')}"
        
        verification_results = []
        successful_entries = 0
        failed_entries = 0

        for entry in request.entries:
            try:
                verification_summary = self.verifier_service.verify_text(
                    text=entry.input_text,
                    methods=request.configuration.verification_methods,
                    required_for_confirmed=request.configuration.required_success_rate,
                    required_for_review=request.configuration.max_verification_time
                )
                
                if verification_summary.final_status == entry.expected_status:
                    successful_entries += 1
                else:
                    failed_entries += 1
                
                verification_results.append(verification_summary)
                
            except Exception as e:
                failed_entries += 1
                self.logger.log(
                    level="ERROR",
                    message=f"Error processing benchmark entry: {str(e)}",
                    context={"execution_id": execution_id, "entry_id": id(entry)}
                )

        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        # Create and store benchmark execution
        execution = BenchmarkExecution(
            entries=request.entries,
            configuration=request.configuration,
            start_time=start_time,
            end_time=end_time,
            metrics=self.metrics_service.calculate_benchmark_metrics(
                verification_results=verification_results,
                expected_statuses=[entry.expected_status for entry in request.entries],
                start_time=start_time,
                end_time=end_time
            )
        )

        self.repository.save(execution)

        return RunBenchmarkResponse(
            execution_id=execution_id,
            start_time=start_time,
            end_time=end_time,
            total_entries=len(request.entries),
            successful_entries=successful_entries,
            failed_entries=failed_entries,
            execution_time=execution_time
        )

    def _validate_request(self, request: RunBenchmarkRequest) -> None:
        if not request.entries:
            raise BenchmarkConfigurationError("No entries provided for benchmark")
        if not request.configuration.verification_methods:
            raise BenchmarkConfigurationError("No verification methods configured")
        if request.configuration.required_success_rate <= 0 or request.configuration.required_success_rate > 1:
            raise BenchmarkConfigurationError("Invalid required success rate")