# domain/exceptions/validation_error.py
from typing import Optional, Dict, Any, List
from .base_exception import DomainError

class ValidationError(DomainError):
    """Base class for validation-related errors."""
    def __init__(
        self,
        message: str,
        code: str = "VALIDATION_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)

class InvalidValueError(ValidationError):
    def __init__(
        self,
        field_name: str,
        value: Any,
        reason: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Invalid value for {field_name}: {value}. {reason}",
            code="INVALID_VALUE",
            details=details
        )

class MissingRequiredField(ValidationError):
    def __init__(
        self,
        field_name: str,
        entity_type: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Missing required field '{field_name}' in {entity_type}",
            code="MISSING_REQUIRED_FIELD",
            details=details
        )

class InvalidStateTransition(ValidationError):
    def __init__(
        self,
        current_state: str,
        attempted_state: str,
        entity_type: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Invalid state transition in {entity_type}: {current_state} -> {attempted_state}",
            code="INVALID_STATE_TRANSITION",
            details=details
        )