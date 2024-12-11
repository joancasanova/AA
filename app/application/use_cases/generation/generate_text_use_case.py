# application/use_cases/generation/generate_text_use_case.py
from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime
from ....domain.model.entities.generation import GeneratedResult, GenerationMetadata
from ....domain.ports.llm_port import LLMPort
from ....domain.ports.logger_port import LoggerPort
from ....domain.exceptions.generation_error import InvalidPromptError, GenerationLimitExceeded

@dataclass
class GenerateTextRequest:
    system_prompt: str
    user_prompt: str
    num_sequences: int = 1
    max_tokens: int = 100
    temperature: float = 1.0
    reference_data: Optional[Dict[str, str]] = None

@dataclass
class GenerateTextResponse:
    generated_texts: List[GeneratedResult]
    total_tokens: int
    generation_time: float
    model_name: str

class GenerateTextUseCase:
    def __init__(self, llm: LLMPort, logger: LoggerPort):
        self.llm = llm
        self.logger = logger
        self.MAX_SEQUENCES = 10
        self.MAX_TOKENS = 1000

    def execute(self, request: GenerateTextRequest) -> GenerateTextResponse:
        self._validate_request(request)
        
        start_time = datetime.now()
        
        try:
            generated_results = self.llm.generate(
                system_prompt=request.system_prompt,
                user_prompt=request.user_prompt,
                num_sequences=request.num_sequences,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            
            total_tokens = sum(result.metadata.tokens_used for result in generated_results)
            generation_time = (datetime.now() - start_time).total_seconds()
            
            return GenerateTextResponse(
                generated_texts=generated_results,
                total_tokens=total_tokens,
                generation_time=generation_time,
                model_name=generated_results[0].metadata.model_name if generated_results else "unknown"
            )
            
        except Exception as e:
            self.logger.log(
                level="ERROR",
                message=f"Text generation failed: {str(e)}",
                context={
                    "num_sequences": request.num_sequences,
                    "max_tokens": request.max_tokens
                }
            )
            raise

    def _validate_request(self, request: GenerateTextRequest) -> None:
        if not request.system_prompt.strip():
            raise InvalidPromptError("system", "System prompt cannot be empty")
        if not request.user_prompt.strip():
            raise InvalidPromptError("user", "User prompt cannot be empty")
        if request.num_sequences > self.MAX_SEQUENCES:
            raise GenerationLimitExceeded("sequences", request.num_sequences, self.MAX_SEQUENCES)
        if request.max_tokens > self.MAX_TOKENS:
            raise GenerationLimitExceeded("tokens", request.max_tokens, self.MAX_TOKENS)