# domain/model/entities/verification.py
from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime

class VerificationMethodType(Enum):
    EMBEDDING = "embedding"
    CONSENSUS = "consensus"
    REGEX = "regex"
    CUSTOM = "custom"

class VerificationMode(Enum):
    ELIMINATORY = "eliminatory"
    CUMULATIVE = "cumulative"

@dataclass(frozen=True)
class VerificationThresholds:
    lower_bound: float
    upper_bound: float
    target_value: Optional[float] = None

    def is_within_bounds(self, value: float) -> bool:
        return self.lower_bound <= value <= self.upper_bound

@dataclass(frozen=True)
class VerificationMethod:
    name: str
    method_type: VerificationMethodType
    mode: VerificationMode
    thresholds: Optional[VerificationThresholds] = None
    reference_text: Optional[str] = None
    required_matches: Optional[int] = None

@dataclass(frozen=True)
class VerificationResult:
    method: VerificationMethod
    passed: bool
    score: Optional[float] = None
    details: Optional[Dict[str, any]] = None
    timestamp: datetime = datetime.now()

@dataclass(frozen=True)
class VerificationSummary:
    results: List[VerificationResult]
    final_status: str
    verification_time: float
    
    @property
    def passed_methods(self) -> List[str]:
        return [result.method.name for result in self.results if result.passed]
    
    @property
    def failed_methods(self) -> List[str]:
        return [result.method.name for result in self.results if not result.passed]
    
    @property
    def success_rate(self) -> float:
        if not self.results:
            return 0.0
        return len(self.passed_methods) / len(self.results)
