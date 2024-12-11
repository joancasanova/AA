# app/application/orchestration/pipeline.py
from typing import List, Any
from datetime import datetime
import logging
from .types import StageConfig
from .results import StageResult, ExecutionResult
from .stage_executor import StageExecutor

logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self, stage_executor: StageExecutor):
        self.stage_executor = stage_executor
        logger.info("Pipeline initialized")

    def execute(self, stages: List[StageConfig], initial_input: Any) -> ExecutionResult:
        self._validate_stage_order(stages)
        
        execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        start_time = datetime.now().isoformat()
        stages_results = []
        current_inputs = [initial_input]

        for stage in stages:
            stage_results = []
            for input_data in current_inputs:
                result = self.stage_executor.execute_stage(stage, input_data)
                stage_results.append(
                    StageResult(
                        stage_type=stage.stage_type,
                        input_data=input_data,
                        output_data=result,
                        timestamp=datetime.now().isoformat(),
                        execution_id=execution_id
                    )
                )
            
            stages_results.extend(stage_results)
            current_inputs = [sr.output_data for sr in stage_results]
            current_inputs = self._flatten_results(current_inputs)

        end_time = datetime.now().isoformat()
        
        return ExecutionResult(
            stages_results=stages_results,
            start_time=start_time,
            end_time=end_time,
            execution_id=execution_id
        )

    def _validate_stage_order(self, stages: List[StageConfig]):
        for i in range(len(stages) - 1):
            if (stages[i].stage_type == StageType.VERIFY and 
                stages[i + 1].stage_type == StageType.PARSE):
                raise ValueError("Invalid stage order: Verify cannot be followed by Parse")

    def _flatten_results(self, results: List[Any]) -> List[Any]:
        flattened = []
        for result in results:
            if isinstance(result, list):
                flattened.extend(result)
            else:
                flattened.append(result)
        return flattened