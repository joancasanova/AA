# application/use_cases/orchestration/execute_pipeline_use_case.py
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from ....domain.ports.logger_port import LoggerPort
from ....application.interfaces.pipeline_orchestrator import (
    PipelineConfig, PipelineResult, PipelineStageType, StageResult
)
from ....application.use_cases.generation.generate_text_use_case import GenerateTextUseCase
from ....application.use_cases.parsing.parse_generated_output_use_case import ParseGeneratedOutputUseCase
from ....application.use_cases.verification.verify_text_use_case import VerifyTextUseCase
from ....domain.exceptions.base_exception import DomainError

@dataclass
class ExecutePipelineRequest:
    config: PipelineConfig
    initial_input: Any
    context: Optional[Dict[str, Any]] = None

@dataclass
class ExecutePipelineResponse:
    pipeline_result: PipelineResult
    execution_time: float
    stages_completed: int
    stages_failed: int
    error_details: Optional[Dict[str, Any]] = None

class ExecutePipelineUseCase:
    def __init__(
        self,
        generate_use_case: GenerateTextUseCase,
        parse_use_case: ParseGeneratedOutputUseCase,
        verify_use_case: VerifyTextUseCase,
        logger: LoggerPort
    ):
        self.generate_use_case = generate_use_case
        self.parse_use_case = parse_use_case
        self.verify_use_case = verify_use_case
        self.logger = logger

    def execute(self, request: ExecutePipelineRequest) -> ExecutePipelineResponse:
        start_time = datetime.now()
        stages_results = []
        stages_completed = 0
        stages_failed = 0
        current_input = request.initial_input
        error = None

        try:
            for stage_config in request.config.stages:
                stage_result = self._execute_stage(
                    stage_type=stage_config.stage_type,
                    parameters=stage_config.parameters,
                    input_data=current_input,
                    timeout=stage_config.timeout_seconds,
                    retry_count=stage_config.retry_count
                )

                stages_results.append(stage_result)

                if stage_result.error:
                    stages_failed += 1
                    if request.config.error_handling_strategy == "fail_fast":
                        error = stage_result.error
                        break
                else:
                    stages_completed += 1
                    current_input = stage_result.output_data

            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            pipeline_result = PipelineResult(
                stages_results=stages_results,
                start_time=start_time,
                end_time=end_time,
                total_time=execution_time,
                success=stages_failed == 0,
                error=error
            )

            return ExecutePipelineResponse(
                pipeline_result=pipeline_result,
                execution_time=execution_time,
                stages_completed=stages_completed,
                stages_failed=stages_failed,
                error_details={"error": str(error)} if error else None
            )

        except Exception as e:
            self.logger.log(
                level="ERROR",
                message="Pipeline execution failed",
                context={
                    "error": str(e),
                    "stages_completed": stages_completed,
                    "stages_failed": stages_failed
                }
            )
            raise

    def _execute_stage(
        self,
        stage_type: PipelineStageType,
        parameters: Dict[str, Any],
        input_data: Any,
        timeout: Optional[float],
        retry_count: Optional[int]
    ) -> StageResult:
        start_time = datetime.now()
        error = None
        output_data = None
        metadata = {}

        try:
            if stage_type == PipelineStageType.GENERATE:
                output_data = self.generate_use_case.execute(
                    system_prompt=parameters.get("system_prompt", ""),
                    user_prompt=parameters.get("user_prompt", ""),
                    num_sequences=parameters.get("num_sequences", 1),
                    max_tokens=parameters.get("max_tokens", 100)
                )
            elif stage_type == PipelineStageType.PARSE:
                output_data = self.parse_use_case.execute(
                    text=input_data,
                    rules=parameters.get("rules", [])
                )
            elif stage_type == PipelineStageType.VERIFY:
                output_data = self.verify_use_case.execute(
                    text=input_data,
                    methods=parameters.get("methods", []),
                    required_for_confirmed=parameters.get("required_for_confirmed", 1),
                    required_for_review=parameters.get("required_for_review", 0)
                )

        except Exception as e:
            error = str(e)
            self.logger.log(
                level="ERROR",
                message=f"Stage execution failed: {stage_type.value}",
                context={
                    "error": error,
                    "parameters": parameters
                }
            )

        execution_time = (datetime.now() - start_time).total_seconds()
        metadata["execution_time"] = execution_time

        return StageResult(
            stage_type=stage_type,
            input_data=input_data,
            output_data=output_data,
            execution_time=execution_time,
            metadata=metadata,
            error=error
        )