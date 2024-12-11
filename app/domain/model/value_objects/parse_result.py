# domain/model/value_objects/parse_result.py
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass(frozen=True)
class ParseMetrics:
    total_matches: int
    execution_time: float
    chars_processed: int
    rules_matched: List[str]

@dataclass(frozen=True)
class ParseLocation:
    start: int
    end: int
    line_number: Optional[int] = None
    
    def length(self) -> int:
        return self.end - self.start

@dataclass(frozen=True)
class ParseMatch:
    value: str
    location: ParseLocation
    rule_name: str
    confidence: float = 1.0

@dataclass(frozen=True)
class ParseResult:
    matches: List[ParseMatch]
    metrics: ParseMetrics
    timestamp: datetime = datetime.now()

    def get_best_match(self, rule_name: str) -> Optional[ParseMatch]:
        relevant_matches = [m for m in self.matches if m.rule_name == rule_name]
        if not relevant_matches:
            return None
        return max(relevant_matches, key=lambda m: m.confidence)

    def get_all_matches(self, rule_name: str) -> List[ParseMatch]:
        return [m for m in self.matches if m.rule_name == rule_name]

    def to_dict(self) -> Dict[str, List[str]]:
        result = {}
        for match in self.matches:
            if match.rule_name not in result:
                result[match.rule_name] = []
            result[match.rule_name].append(match.value)
        return result