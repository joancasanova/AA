# domain/model/value_objects/similarity_score.py
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class SimilarityScore:
    value: float
    method: str
    reference_text: str
    compared_text: str
    threshold: Optional[float] = None

    def exceeds_threshold(self) -> bool:
        if self.threshold is None:
            return True
        return self.value >= self.threshold

    def as_percentage(self) -> float:
        return self.value * 100

    def __lt__(self, other: 'SimilarityScore') -> bool:
        return self.value < other.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SimilarityScore):
            return NotImplemented
        return (self.value == other.value and 
                self.method == other.method and 
                self.reference_text == other.reference_text and 
                self.compared_text == other.compared_text)