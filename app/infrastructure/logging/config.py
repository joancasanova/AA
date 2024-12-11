# infrastructure/logging/config.py
from typing import Dict, Any, Optional
from pydantic import BaseSettings, DirectoryPath
from pathlib import Path

class LoggingConfig(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOG_DIR: Optional[DirectoryPath] = None
    CONSOLE_LOGGING: bool = True
    FILE_LOGGING: bool = True
    JSON_LOGGING: bool = True
    
    # Rotation settings
    MAX_BYTES: int = 10_485_760  # 10MB
    BACKUP_COUNT: int = 5
    
    # Additional settings
    INCLUDE_PROCESS_INFO: bool = True
    INCLUDE_THREAD_INFO: bool = True
    INCLUDE_TIMESTAMP: bool = True
    
    class Config:
        env_prefix = "LOG_"
        case_sensitive = True

def setup_logging(config: LoggingConfig) -> None:
    """
    Set up logging configuration based on settings.
    """
    handlers = []
    
    if config.CONSOLE_LOGGING:
        handlers.append(create_console_handler())
    
    if config.FILE_LOGGING and config.LOG_DIR:
        handlers.extend([
            create_file_handler(
                Path(config.LOG_DIR) / "app.log",
                formatter=DetailedFormatter(),
                max_bytes=config.MAX_BYTES,
                backup_count=config.BACKUP_COUNT
            )
        ])
    
    if config.JSON_LOGGING and config.LOG_DIR:
        handlers.append(
            create_file_handler(
                Path(config.LOG_DIR) / "app.json",
                formatter=JsonFormatter(),
                max_bytes=config.MAX_BYTES,
                backup_count=config.BACKUP_COUNT
            )
        )
    
    return ApplicationLogger(
        name="app",
        log_level=config.LOG_LEVEL,
        log_dir=str(config.LOG_DIR) if config.LOG_DIR else None
    )