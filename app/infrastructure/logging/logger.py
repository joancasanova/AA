# infrastructure/logging/logger.py
from typing import Optional, Dict, Any
import logging
import json
from datetime import datetime
from pathlib import Path
from ....domain.ports.logger_port import LoggerPort, LogLevel
from .formatters import JsonFormatter, DetailedFormatter
from .handlers import create_file_handler, create_console_handler

class ApplicationLogger(LoggerPort):
    def __init__(
        self,
        name: str,
        log_level: str = "INFO",
        log_dir: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        self.context = context or {}
        
        # Create handlers
        handlers = [create_console_handler()]
        if log_dir:
            handlers.extend([
                create_file_handler(
                    Path(log_dir) / "app.log",
                    formatter=DetailedFormatter()
                ),
                create_file_handler(
                    Path(log_dir) / "app.json",
                    formatter=JsonFormatter()
                )
            ])
        
        # Add handlers to logger
        for handler in handlers:
            self.logger.addHandler(handler)

    def log(
        self,
        level: LogLevel,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        exception: Optional[Exception] = None
    ) -> None:
        log_context = {**self.context, **(context or {})}
        
        log_data = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "context": log_context
        }
        
        if exception:
            log_data["exception"] = {
                "type": type(exception).__name__,
                "message": str(exception),
                "traceback": self._format_traceback(exception)
            }
        
        log_method = getattr(self.logger, level.value.lower())
        log_method(log_data)

    def set_context(self, **kwargs: Any) -> None:
        self.context.update(kwargs)

    @staticmethod
    def _format_traceback(exception: Exception) -> str:
        import traceback
        return "".join(traceback.format_exception(
            type(exception),
            exception,
            exception.__traceback__
        ))