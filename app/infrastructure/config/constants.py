# infrastructure/config/constants.py
from typing import Final

# Generation Constants
MAX_GENERATIONS: Final[int] = 5
MAX_TOKENS_PER_GENERATION: Final[int] = 2000

# Verification Constants  
SIMILARITY_THRESHOLD: Final[float] = 0.85
VERIFICATION_TIMEOUT: Final[int] = 30

# Parsing Constants
MAX_PARSE_LENGTH: Final[int] = 10000

# Pipeline Constants
MAX_PIPELINE_STAGES: Final[int] = 10

# Error Messages
ERR_INVALID_PIPELINE: Final[str] = "Invalid pipeline configuration"
ERR_VERIFICATION_AFTER_PARSE: Final[str] = "Verification cannot follow parsing in pipeline"
ERR_INVALID_INPUT: Final[str] = "Invalid input provided"

# Success Messages
MSG_PIPELINE_COMPLETE: Final[str] = "Pipeline execution completed successfully"