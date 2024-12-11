# infrastructure/exceptions.py
from typing import Optional, Dict, Any
from ..domain.exceptions.base_exception import DomainError

class InfrastructureError(DomainError):
    """Base class for infrastructure layer exceptions."""
    def __init__(
        self,
        message: str,
        code: str = "INFRASTRUCTURE_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)

# Database Exceptions
class DatabaseError(InfrastructureError):
    """Base class for database-related exceptions."""
    def __init__(
        self,
        message: str,
        code: str = "DATABASE_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)

class ConnectionError(DatabaseError):
    def __init__(
        self,
        host: str,
        port: int,
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"Failed to connect to database at {host}:{port}"
        if original_error:
            message += f" - {str(original_error)}"
        super().__init__(
            message=message,
            code="DB_CONNECTION_ERROR",
            details=details
        )

class QueryError(DatabaseError):
    def __init__(
        self,
        query: str,
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"Query execution failed: {query[:100]}..."
        if original_error:
            message += f" - {str(original_error)}"
        super().__init__(
            message=message,
            code="DB_QUERY_ERROR",
            details=details
        )

class TransactionError(DatabaseError):
    def __init__(
        self,
        operation: str,
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"Transaction failed during {operation}"
        if original_error:
            message += f" - {str(original_error)}"
        super().__init__(
            message=message,
            code="DB_TRANSACTION_ERROR",
            details=details
        )

# External Service Exceptions
class ExternalServiceError(InfrastructureError):
    """Base class for external service-related exceptions."""
    def __init__(
        self,
        message: str,
        code: str = "EXTERNAL_SERVICE_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)

class ModelLoadError(ExternalServiceError):
    def __init__(
        self,
        model_name: str,
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"Failed to load model '{model_name}'"
        if original_error:
            message += f" - {str(original_error)}"
        super().__init__(
            message=message,
            code="MODEL_LOAD_ERROR",
            details=details
        )

class ModelExecutionError(ExternalServiceError):
    def __init__(
        self,
        model_name: str,
        operation: str,
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"Error executing {operation} with model '{model_name}'"
        if original_error:
            message += f" - {str(original_error)}"
        super().__init__(
            message=message,
            code="MODEL_EXECUTION_ERROR",
            details=details
        )

# Cache Exceptions
class CacheError(InfrastructureError):
    """Base class for cache-related exceptions."""
    def __init__(
        self,
        message: str,
        code: str = "CACHE_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)

class CacheConnectionError(CacheError):
    def __init__(
        self,
        host: str,
        port: int,
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"Failed to connect to cache at {host}:{port}"
        if original_error:
            message += f" - {str(original_error)}"
        super().__init__(
            message=message,
            code="CACHE_CONNECTION_ERROR",
            details=details
        )

class CacheOperationError(CacheError):
    def __init__(
        self,
        operation: str,
        key: str,
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"Cache operation '{operation}' failed for key '{key}'"
        if original_error:
            message += f" - {str(original_error)}"
        super().__init__(
            message=message,
            code="CACHE_OPERATION_ERROR",
            details=details
        )

# Configuration Exceptions
class ConfigurationError(InfrastructureError):
    """Base class for configuration-related exceptions."""
    def __init__(
        self,
        message: str,
        code: str = "CONFIG_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)

class ConfigurationLoadError(ConfigurationError):
    def __init__(
        self,
        config_path: str,
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"Failed to load configuration from '{config_path}'"
        if original_error:
            message += f" - {str(original_error)}"
        super().__init__(
            message=message,
            code="CONFIG_LOAD_ERROR",
            details=details
        )

class ConfigurationValidationError(ConfigurationError):
    def __init__(
        self,
        validation_errors: Dict[str, str],
        details: Optional[Dict[str, Any]] = None
    ):
        message = "Configuration validation failed:\n" + "\n".join(
            f"- {key}: {error}" for key, error in validation_errors.items()
        )
        super().__init__(
            message=message,
            code="CONFIG_VALIDATION_ERROR",
            details=details
        )

# Resource Management Exceptions
class ResourceError(InfrastructureError):
    """Base class for resource management-related exceptions."""
    def __init__(
        self,
        message: str,
        code: str = "RESOURCE_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, details)

class ResourceNotFoundError(ResourceError):
    def __init__(
        self,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"{resource_type} with id '{resource_id}' not found"
        super().__init__(
            message=message,
            code="RESOURCE_NOT_FOUND",
            details=details
        )

class ResourceExhaustedError(ResourceError):
    def __init__(
        self,
        resource_type: str,
        limit: int,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"{resource_type} limit ({limit}) exceeded"
        super().__init__(
            message=message,
            code="RESOURCE_EXHAUSTED",
            details=details
        )