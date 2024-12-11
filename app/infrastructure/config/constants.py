# infrastructure/config/constants.py
from typing import Final

# Application Constants
MAX_RETRIES: Final[int] = 3
REQUEST_TIMEOUT: Final[int] = 30
BATCH_SIZE: Final[int] = 100

# Cache Keys
CACHE_KEY_PREFIX: Final[str] = "benchmark:"
CACHE_TTL_SHORT: Final[int] = 300  # 5 minutes
CACHE_TTL_MEDIUM: Final[int] = 3600  # 1 hour
CACHE_TTL_LONG: Final[int] = 86400  # 24 hours

# File Paths
LOG_FILE_PATH: Final[str] = "logs/app.log"
TEMP_DIR: Final[str] = "tmp"
UPLOAD_DIR: Final[str] = "uploads"

# Error Messages
ERR_DATABASE_CONNECTION: Final[str] = "Could not connect to database"
ERR_CACHE_CONNECTION: Final[str] = "Could not connect to cache"
ERR_MODEL_LOADING: Final[str] = "Could not load model"
ERR_INVALID_INPUT: Final[str] = "Invalid input provided"

# Success Messages
MSG_STARTUP: Final[str] = "Application started successfully"
MSG_SHUTDOWN: Final[str] = "Application shut down gracefully"

# Configuration Keys
CONFIG_DATABASE: Final[str] = "database"
CONFIG_CACHE: Final[str] = "cache"
CONFIG_LLM: Final[str] = "llm"
CONFIG_EMBEDDINGS: Final[str] = "embeddings"