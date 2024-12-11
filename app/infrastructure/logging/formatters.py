# infrastructure/logging/formatters.py
import logging
import json
from datetime import datetime
from typing import Dict, Any

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {}
        
        # Add basic log record attributes
        log_data.update({
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "process": record.process,
            "thread": record.thread
        })
        
        # Add message and formatted message
        if isinstance(record.msg, dict):
            log_data.update(record.msg)
        else:
            log_data["message"] = record.getMessage()
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add custom attributes
        if hasattr(record, "context"):
            log_data["context"] = record.context
        
        return json.dumps(log_data, default=str)

class DetailedFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(
            fmt=(
                "%(asctime)s [%(levelname)s] %(name)s (%(process)d:%(thread)d) - "
                "%(message)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    def format(self, record: logging.LogRecord) -> str:
        formatted = super().format(record)
        
        # Add context if present
        if hasattr(record, "context"):
            formatted += f"\nContext: {json.dumps(record.context, default=str)}"
        
        # Add exception info if present
        if record.exc_info:
            formatted += f"\nException:\n{self.formatException(record.exc_info)}"
        
        return formatted