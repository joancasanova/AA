# domain/model/value_objects/verification_status.py
from enum import Enum
from typing import Optional

class VerificationStatus(Enum):
    CONFIRMED = "confirmada"
    DISCARDED = "descartada"
    REVIEW = "a revisar"

    @classmethod
    def from_string(cls, status: str) -> Optional['VerificationStatus']:
        try:
            return cls(status.lower())
        except ValueError:
            return None

    def is_final(self) -> bool:
        return self in [VerificationStatus.CONFIRMED, VerificationStatus.DISCARDED]

    def requires_review(self) -> bool:
        return self == VerificationStatus.REVIEW