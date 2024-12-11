# app/application/orchestration/stage_executor.py
from typing import Any, List
import logging
from app.application.use_cases.generate_text_use_case import GenerateTextUseCase
from app.application.use_cases.parse_generated_output_use_case import ParseGeneratedOutputUseCase
from app.application.use_cases.verify_text_use_case import VerifyTextUseCase
from app.domain.entities import GeneratedResult, ParsedResult, ParseEntry
from .types import StageType, StageConfig, GenerateStageConfig, ParseStageConfig, VerifyStageConfig

logger = logging.getLogger(__name__)

class StageExecutor:
    def __init__(
        self,
        generate_use_case: GenerateTextUseCase,
        parse_use_case: ParseGeneratedOutputUseCase,
        verify_use_case: VerifyTextUseCase
    ):
        self.generate_use_case = generate_use_case
        self.parse_use_case = parse_use_case
        self.verify_use_case = verify_use_case
        logger.info("StageExecutor initialized")

    def execute_stage(self, stage: StageConfig, input_data: Any) -> Any:
        if stage.stage_type == StageType.GENERATE:
            return self._execute_generate(stage.config, input_data)
        elif stage.stage_type == StageType.PARSE:
            return self._execute_parse(stage.config, input_data)
        elif stage.stage_type == StageType.VERIFY:
            return self._execute_verify(stage.config, input_data)
        raise ValueError(f"Unknown stage type: {stage.stage_type}")

    def _execute_generate(self, config: GenerateStageConfig, input_data: Any) -> List[GeneratedResult]:
        if isinstance(input_data, ParsedResult):
            results = []
            for entry in input_data.entries:
                config.reference_data = entry.data
                results.extend(
                    self.generate_use_case.execute(
                        config.system_prompt,
                        config.user_prompt,
                        config.num_return_sequences,
                        config.max_new_tokens,
                        config.num_executions,
                        config.reference_data
                    )
                )
            return results

        return self.generate_use_case.execute(
            config.system_prompt,
            config.user_prompt,
            config.num_return_sequences,
            config.max_new_tokens,
            config.num_executions,
            config.reference_data
        )

    def _execute_parse(self, config: ParseStageConfig, input_data: Any) -> List[ParsedResult]:
        if isinstance(input_data, GeneratedResult):
            return [self.parse_use_case.execute(input_data, config.parse_configuration)]
        elif isinstance(input_data, list):
            return [
                self.parse_use_case.execute(result, config.parse_configuration)
                for result in input_data
            ]
        raise ValueError(f"Invalid input type for Parse stage: {type(input_data)}")

    def _execute_verify(self, config: VerifyStageConfig, input_data: Any) -> List[ParsedResult]:
        if isinstance(input_data, GeneratedResult):
            parsed_result = ParsedResult([ParseEntry({"input": input_data.response})])
            return [self.verify_use_case.execute(parsed_result, config.verification_process)]
        elif isinstance(input_data, ParsedResult):
            return [self.verify_use_case.execute(input_data, config.verification_process)]
        elif isinstance(input_data, list):
            results = []
            for item in input_data:
                if isinstance(item, GeneratedResult):
                    parsed_result = ParsedResult([ParseEntry({"input": item.response})])
                    results.append(
                        self.verify_use_case.execute(parsed_result, config.verification_process)
                    )
                elif isinstance(item, ParsedResult):
                    results.append(
                        self.verify_use_case.execute(item, config.verification_process)
                    )
            return results
        raise ValueError(f"Invalid input type for Verify stage: {type(input_data)}")
