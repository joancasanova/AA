# domain/entities.py

from typing import Any, Dict, List, Optional
from enum import Enum

class GeneratedResult:
    def __init__(self, response: str):
        self.response = response

class ParseEntry:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

class ParsedResult:
    def __init__(self, entries: List[ParseEntry]):
        self.entries = entries
        self.verification_methods_passed: List[str] = []
        self.verification_methods_failed: List[str] = []
        self.final_status: Optional[str] = None

class VerificationPrompt:
    def __init__(self, name: str, context: str, instruction: str,
                 num_return_sequences:int, max_new_tokens:int, num_positive:int, positive_responses:List[str]):
        self.name = name
        self.context = context
        self.instruction = instruction
        self.num_return_sequences = num_return_sequences
        self.max_new_tokens = max_new_tokens
        self.num_positive = num_positive
        self.positive_responses = positive_responses

class VerificationMethodType(Enum):
    EMBEDDING = "embedding"
    CONSENSUS = "consensus"

class VerificationMethodMode(Enum):
    ELIMINATORIO = "eliminatorio"
    ACUMULATIVO = "acumulativo"

class EmbeddingVerificationSettings:
    def __init__(self, lower_threshold: float, upper_threshold: float, reference_text: str):
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        self.reference_text = reference_text

class ConsensusVerificationSettings:
    def __init__(self, 
                 system_prompt: str, 
                 user_prompt: str, 
                 placeholders: List[str],
                 positive_responses: List[str],
                 num_responses: int,
                 num_positive_required: int,
                 max_new_tokens: int):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.placeholders = placeholders
        self.positive_responses = positive_responses
        self.num_responses = num_responses
        self.num_positive_required = num_positive_required
        self.max_new_tokens = max_new_tokens

class VerificationMethod:
    def __init__(self, 
                 name: str,
                 method_type: VerificationMethodType, 
                 mode: VerificationMethodMode,
                 embedding_settings: Optional[EmbeddingVerificationSettings],
                 consensus_settings: Optional[ConsensusVerificationSettings]):
        self.name = name
        self.method_type = method_type
        self.mode = mode
        self.embedding_settings = embedding_settings
        self.consensus_settings = consensus_settings

class VerificationProcess:
    def __init__(self,
                 methods: List[VerificationMethod],
                 required_for_confirmed: int,
                 required_for_review: int):
        self.methods = methods
        self.required_for_confirmed = required_for_confirmed
        self.required_for_review = required_for_review
        total_acumulativos = sum(1 for m in methods if m.mode == VerificationMethodMode.ACUMULATIVO)
        if required_for_confirmed > total_acumulativos:
            raise ValueError("required_for_confirmed no puede ser mayor que el total acumulativo")
        if required_for_review >= required_for_confirmed:
            raise ValueError("required_for_review debe ser menor que required_for_confirmed")

class ParseMode(Enum):
    REGEX = "regex"
    KEYWORD = "keyword"

class ParseScope(Enum):
    LINE_BY_LINE = "line_by_line"
    ALL_TEXT = "all_text"

class ParseFallbackStrategy(Enum):
    ERROR = "error"
    EMPTY = "empty"
    CUSTOM = "custom"

class ParseMultipleStrategy(Enum):
    FIRST = "first"
    ALL = "all"

class ParseRule:
    def __init__(
        self, 
        label: str,
        mode: ParseMode,
        pattern: str,
        secondary_pattern: str,
        scope: ParseScope = ParseScope.ALL_TEXT,
        fallback_strategy: ParseFallbackStrategy = ParseFallbackStrategy.ERROR,
        fallback_value: str = "",
        multiple_strategy: ParseMultipleStrategy = ParseMultipleStrategy.FIRST
    ):
        self.label = label
        self.mode = mode
        self.pattern = pattern
        self.secondary_pattern = secondary_pattern
        self.scope = scope
        self.fallback_strategy = fallback_strategy
        self.fallback_value = fallback_value
        self.multiple_strategy = multiple_strategy

class ParseConfiguration:
    def __init__(self, rules: List[ParseRule]):
        self.rules = rules
