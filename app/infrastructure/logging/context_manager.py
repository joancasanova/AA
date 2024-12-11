# infrastructure/logging/context_manager.py
from typing import Optional, Dict, Any
from contextlib import contextmanager
import logging
from datetime import datetime

class LogContext:
    def __init__(self):
        self._context: Dict[str, Any] = {}

    def set(self, **kwargs: Any) -> None:
        self._context.update(kwargs)

    def get(self) -> Dict[str, Any]:
        return self._context.copy()

    def clear(self) -> None:
        self._context.clear()

@contextmanager
def log_context(**kwargs: Any):
    """
    Context manager for temporarily setting log context.
    """
    previous = LogContext().get()
    try:
        LogContext().set(**kwargs)
        yield
    finally:
        LogContext().clear()
        LogContext().set(**previous)