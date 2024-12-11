# domain/exceptions/parsing_error.py
from typing import Optional, Dict, Any, List
from .base_exception import DomainError

class ParsingError(DomainError):
    """Base class for parsing-related errors."""
    def __init__(
        self,
        message: str,
        code: str = "PARSING_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)

class InvalidParseRule(ParsingError):
    def __init__(
        self,
        rule_name: str,
        reason: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Invalid parse rule '{rule_name}': {reason}",
            code="INVALID_PARSE_RULE",
            details=details
        )

class RequiredFieldNotFound(ParsingError):
    def __init__(
        self,
        field_name: str,
        text_preview: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Required field '{field_name}' not found in text: '{text_preview[:100]}...'",
            code="REQUIRED_FIELD_NOT_FOUND",
            details=details
        )

class ParseExecutionError(ParsingError):
    def __init__(
        self,
        rule_name: str,
        error_description: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Error executing parse rule '{rule_name}': {error_description}",
            code="PARSE_EXECUTION_ERROR",
            details=details
        )