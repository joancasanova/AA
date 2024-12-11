# domain/model/entities/parsing.py
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class ParseMode(Enum):
    REGEX = "regex"
    KEYWORD = "keyword"

class ParseScope(Enum):
    LINE_BY_LINE = "line_by_line"
    ALL_TEXT = "all_text"

class ParseStrategy(Enum):
    FIRST_MATCH = "first_match"
    ALL_MATCHES = "all_matches"
    LONGEST_MATCH = "longest_match"

@dataclass(frozen=True)
class ParseRule:
    name: str
    pattern: str
    mode: ParseMode
    scope: ParseScope = ParseScope.ALL_TEXT
    strategy: ParseStrategy = ParseStrategy.FIRST_MATCH
    fallback_value: Optional[str] = None

@dataclass(frozen=True)
class ParseEntry:
    rule_name: str
    extracted_value: str
    source_text: str
    start_position: int
    end_position: int

    def get_context(self, chars_before: int = 50, chars_after: int = 50) -> str:
        start = max(0, self.start_position - chars_before)
        end = min(len(self.source_text), self.end_position + chars_after)
        return self.source_text[start:end]

@dataclass(frozen=True)
class ParsedDocument:
    entries: List[ParseEntry]
    original_text: str
    rules_applied: List[ParseRule]

    def get_value_by_rule(self, rule_name: str) -> Optional[str]:
        for entry in self.entries:
            if entry.rule_name == rule_name:
                return entry.extracted_value
        return None

    def all_values_by_rule(self, rule_name: str) -> List[str]:
        return [entry.extracted_value for entry in self.entries if entry.rule_name == rule_name]