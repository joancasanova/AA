# app/application/orchestration/types.py
from enum import Enum
from typing import Dict, Union
from dataclasses import dataclass
from app.domain.entities import ParseConfiguration, VerificationProcess

class StageType(Enum):
    GENERATE = "generate"
    PARSE = "parse"
    VERIFY = "verify"

@dataclass
class GenerateStageConfig:
    system_prompt: str
    user_prompt: str
    num_return_sequences: int
    max_new_tokens: int
    num_executions: int
    reference_data: Dict[str, str]

@dataclass
class ParseStageConfig:
    parse_configuration: ParseConfiguration

@dataclass
class VerifyStageConfig:
    verification_process: VerificationProcess

@dataclass
class StageConfig:
    stage_type: StageType
    config: Union[GenerateStageConfig, ParseStageConfig, VerifyStageConfig]