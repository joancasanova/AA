# infrastructure/logging/handlers.py
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Optional
import gzip
import os

class CompressedRotatingFileHandler(RotatingFileHandler):
    def rotation_filename(self, default_name: str) -> str:
        """
        Append .gz to the rotated filename.
        """
        return default_name + ".gz"

    def rotate(self, source: str, dest: str) -> None:
        """
        Compress the source file and rotate it to destination.
        """
        with open(source, 'rb') as f_in:
            with gzip.open(dest, 'wb') as f_out:
                f_out.writelines(f_in)
        os.remove(source)

class CompressedTimedRotatingFileHandler(TimedRotatingFileHandler):
    def rotation_filename(self, default_name: str) -> str:
        """
        Append .gz to the rotated filename.
        """
        return default_name + ".gz"

    def rotate(self, source: str, dest: str) -> None:
        """
        Compress the source file and rotate it to destination.
        """
        with open(source, 'rb') as f_in:
            with gzip.open(dest, 'wb') as f_out:
                f_out.writelines(f_in)
        os.remove(source)

def create_file_handler(
    log_file: Path,
    formatter: logging.Formatter,
    max_bytes: int = 10_485_760,  # 10MB
    backup_count: int = 5
) -> logging.Handler:
    """
    Create a rotating file handler with compression.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    handler = CompressedRotatingFileHandler(
        filename=str(log_file),
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    handler.setFormatter(formatter)
    return handler

def create_console_handler() -> logging.Handler:
    """
    Create a console handler with colored output.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(DetailedFormatter())
    return handler