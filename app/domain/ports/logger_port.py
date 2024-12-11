# domain/ports/logger_port.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from enum import Enum

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LoggerPort(ABC):
    @abstractmethod
    def log(
        self,
        level: LogLevel,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        exception: Optional[Exception] = None
    ) -> None:
        """
        Log a message with the specified level and context.
        
        Args:
            level: Severity level of the log
            message: Message to log
            context: Optional dictionary of contextual information
            exception: Optional exception information
        """
        pass
    
    @abstractmethod
    def set_context(self, **kwargs: Any) -> None:
        """
        Set context values that will be included in all subsequent log messages.
        
        Args:
            **kwargs: Key-value pairs to add to the context
        """
        pass