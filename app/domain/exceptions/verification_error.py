# domain/exceptions/verification_error.py
from typing import Optional, Dict, Any, List
from .base_exception import DomainError

class VerificationError(DomainError):
    """Base class for verification-related errors."""
    def __init__(
        self,
        message: str,
        code: str = "VERIFICATION_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)

class InvalidVerificationMethod(VerificationError):
    def __init__(
        self,
        method_name: str,
        reason: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Invalid verification method '{method_name}': {reason}",
            code="INVALID_VERIFICATION_METHOD",
            details=details
        )

class VerificationConfigurationError(VerificationError):
    def __init__(
        self,
        config_issue: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Verification configuration error: {config_issue}",
            code="VERIFICATION_CONFIG_ERROR",
            details=details
        )

class VerificationExecutionError(VerificationError):
    def __init__(
        self,
        method_name: str,
        error_description: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Error executing verification method '{method_name}': {error_description}",
            code="VERIFICATION_EXECUTION_ERROR",
            details=details
        )