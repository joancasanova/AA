# domain/exceptions/generation_error.py
from typing import Optional, Dict, Any, List
from .base_exception import DomainError

class GenerationError(DomainError):
    """Base class for text generation-related errors."""
    def __init__(
        self,
        message: str,
        code: str = "GENERATION_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)

class InvalidPromptError(GenerationError):
    def __init__(
        self,
        prompt_type: str,
        reason: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Invalid {prompt_type} prompt: {reason}",
            code="INVALID_PROMPT",
            details=details
        )

class GenerationLimitExceeded(GenerationError):
    def __init__(
        self,
        limit_type: str,
        current_value: int,
        max_value: int,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"{limit_type} limit exceeded: {current_value} > {max_value}",
            code="GENERATION_LIMIT_EXCEEDED",
            details=details
        )

class ModelExecutionError(GenerationError):
    def __init__(
        self,
        model_name: str,
        error_description: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Error executing model '{model_name}': {error_description}",
            code="MODEL_EXECUTION_ERROR",
            details=details
        )
