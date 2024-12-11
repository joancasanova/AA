# app/application/orchestration/results.py
from dataclasses import dataclass
from typing import List, Any
import json
from .types import StageType
from app.domain.entities import GeneratedResult, ParsedResult

@dataclass
class StageResult:
    stage_type: StageType
    input_data: Any
    output_data: Any
    timestamp: str
    execution_id: str

@dataclass
class ExecutionResult:
    stages_results: List[StageResult]
    start_time: str
    end_time: str
    execution_id: str

    def to_json(self) -> str:
        return json.dumps({
            'execution_id': self.execution_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'stages_results': [
                {
                    'stage_type': sr.stage_type.value,
                    'input_data': self._serialize_data(sr.input_data),
                    'output_data': self._serialize_data(sr.output_data),
                    'timestamp': sr.timestamp,
                    'execution_id': sr.execution_id
                }
                for sr in self.stages_results
            ]
        }, indent=2)

    def _serialize_data(self, data: Any) -> Any:
        if isinstance(data, GeneratedResult):
            return {'response': data.response}
        elif isinstance(data, ParsedResult):
            return {
                'entries': [{'data': entry.data} for entry in data.entries],
                'verification_methods_passed': data.verification_methods_passed,
                'verification_methods_failed': data.verification_methods_failed,
                'final_status': data.final_status
            }
        elif isinstance(data, list):
            return [self._serialize_data(item) for item in data]
        elif isinstance(data, dict):
            return {k: self._serialize_data(v) for k, v in data.items()}
        return data