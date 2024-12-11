# domain/services/parse_service.py
from typing import List, Dict, Optional, Tuple
import re
import logging
from ..model.entities.parsing import (
    ParseRule, ParseEntry, ParsedDocument, ParseMode, 
    ParseScope, ParseStrategy
)
from ..model.value_objects.parse_result import ParseResult, ParseMatch, ParseMetrics, ParseLocation
from datetime import datetime

logger = logging.getLogger(__name__)

class ParseService:
    def parse_text(self, text: str, rules: List[ParseRule]) -> ParseResult:
        start_time = datetime.now()
        matches: List[ParseMatch] = []
        rules_matched: List[str] = []

        for rule in rules:
            if rule.scope == ParseScope.LINE_BY_LINE:
                rule_matches = self._parse_line_by_line(text, rule)
            else:
                rule_matches = self._parse_all_text(text, rule)
            
            if rule_matches:
                matches.extend(rule_matches)
                rules_matched.append(rule.name)

        execution_time = (datetime.now() - start_time).total_seconds()
        metrics = ParseMetrics(
            total_matches=len(matches),
            execution_time=execution_time,
            chars_processed=len(text),
            rules_matched=rules_matched
        )

        return ParseResult(
            matches=matches,
            metrics=metrics
        )

    def _parse_line_by_line(self, text: str, rule: ParseRule) -> List[ParseMatch]:
        matches = []
        for i, line in enumerate(text.splitlines(), 1):
            line_matches = self._apply_rule(line, rule, line_number=i)
            if line_matches:
                matches.extend(line_matches)
                if rule.strategy == ParseStrategy.FIRST_MATCH:
                    break
        return matches

    def _parse_all_text(self, text: str, rule: ParseRule) -> List[ParseMatch]:
        return self._apply_rule(text, rule)

    def _apply_rule(self, text: str, rule: ParseRule, line_number: Optional[int] = None) -> List[ParseMatch]:
        matches = []
        
        if rule.mode == ParseMode.REGEX:
            regex_matches = list(re.finditer(rule.pattern, text))
            for match in regex_matches:
                location = ParseLocation(
                    start=match.start(),
                    end=match.end(),
                    line_number=line_number
                )
                matches.append(ParseMatch(
                    value=match.group(),
                    location=location,
                    rule_name=rule.name,
                    confidence=1.0
                ))
        
        elif rule.mode == ParseMode.KEYWORD:
            start = 0
            while True:
                start_idx = text.find(rule.pattern, start)
                if start_idx == -1:
                    break
                    
                end_idx = len(text)
                if rule.secondary_pattern:
                    end_match = text.find(rule.secondary_pattern, start_idx + len(rule.pattern))
                    if end_match != -1:
                        end_idx = end_match
                
                location = ParseLocation(
                    start=start_idx,
                    end=end_idx,
                    line_number=line_number
                )
                
                value = text[start_idx + len(rule.pattern):end_idx].strip()
                if value:
                    matches.append(ParseMatch(
                        value=value,
                        location=location,
                        rule_name=rule.name,
                        confidence=0.9  # Slightly lower confidence for keyword matching
                    ))
                
                start = end_idx + 1

        # Apply strategy
        if matches and rule.strategy == ParseStrategy.FIRST_MATCH:
            return [matches[0]]
        elif matches and rule.strategy == ParseStrategy.LONGEST_MATCH:
            return [max(matches, key=lambda m: len(m.value))]
        
        return matches