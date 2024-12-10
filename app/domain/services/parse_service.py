# domain/services/parse_service.py
import logging
import re
from typing import Dict, List, Optional
from app.domain.entities import (ParseConfiguration, ParseRule, ParseMode, ParseScope, ParseFallbackStrategy, ParseMultipleStrategy)

logger = logging.getLogger(__name__)

class ParseService:
    def __init__(self):
        logger.info("ParseService initialized")

    def parse_text(self, text: str, config: ParseConfiguration) -> List[Dict[str, str]]:
        logger.info(f"Parsing text: {text} with config: {config}")
        # Return a list of dictionaries. Each dictionary is a set of placeholders for a "row".
        # First, extract all matches per rule.
        all_rule_matches = []
        for rule in config.rules:
            if rule.scope == ParseScope.LINE_BY_LINE:
                raw_matches = self._parse_line_by_line_all(text, rule)
            else:
                raw_matches = self._parse_all_text_all(text, rule)

            if not raw_matches:
                # Nothing found
                if rule.fallback_strategy == ParseFallbackStrategy.ERROR:
                    logger.error(f"No match found for '{rule.label}'")
                    raise ValueError(f"No match found for '{rule.label}'")
                elif rule.fallback_strategy == ParseFallbackStrategy.EMPTY:
                    raw_matches = [""]
                elif rule.fallback_strategy == ParseFallbackStrategy.CUSTOM:
                    raw_matches = [rule.fallback_value]

            # Apply multiple_strategy
            if rule.multiple_strategy == ParseMultipleStrategy.FIRST:
                raw_matches = [raw_matches[0]]  # only first match

            # Save the final matches for this rule
            # raw_matches is the final list of strings for this rule
            all_rule_matches.append((rule.label, raw_matches))

        # Combine the matches of all rules
        # Find the minimum length of the lists "all"
        min_length = min(len(m[1]) for m in all_rule_matches)
        # Create min_length entries
        entries = []
        for i in range(min_length):
            entry_data = {}
            for (label, matches) in all_rule_matches:
                # If this rule has less matches of i (shouldn't happen by min_length), take the first
                # but thanks to min_length this doesn't happen.
                entry_data[label] = matches[i if i < len(matches) else 0]
            entries.append(entry_data)

        logger.debug(f"Parsed entries: {entries}")
        return entries

    def _parse_line_by_line_all(self, text: str, rule: ParseRule) -> List[str]:
        lines = text.splitlines()
        results = []
        for line in lines:
            matches = self._apply_rule_on_text_all(line, rule)
            results.extend(matches)
        return results

    def _parse_all_text_all(self, text: str, rule: ParseRule) -> List[str]:
        return self._apply_rule_on_text_all(text, rule)

    def _apply_rule_on_text_all(self, text: str, rule: ParseRule) -> List[str]:
        if rule.mode == ParseMode.REGEX:
            # For multiple matches we use findall
            matches = re.findall(rule.pattern, text)
            if not matches:
                return []
            return matches if isinstance(matches, list) else [matches]
        else:
            # KEYWORD mode with multiple matches
            # Search for all appearances
            results = []
            start_idx = 0
            while True:
                start_pos = text.find(rule.pattern, start_idx) if rule.pattern else 0
                if rule.pattern and start_pos == -1:
                    break
                if rule.pattern:
                    start_search = start_pos + len(rule.pattern)
                else:
                    start_search = start_idx

                end_pos = len(text)
                if rule.secondary_pattern:
                    sec_pos = text.find(rule.secondary_pattern, start_search)
                    if sec_pos == -1:
                        # no more matches
                        break
                    end_pos = sec_pos

                extracted = text[start_search:end_pos].strip()
                if extracted:
                    results.append(extracted)

                # advance start_idx
                if rule.pattern:
                    start_idx = end_pos + (len(rule.secondary_pattern) if rule.secondary_pattern else 0)
                else:
                    # If no initial pattern, avoid infinite loop
                    break

            return results