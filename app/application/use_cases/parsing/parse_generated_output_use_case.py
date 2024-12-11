# application/use_cases/parsing/parse_generated_output_use_case.py
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from ....domain.model.entities.parsing import ParseRule, ParsedDocument
from ....domain.model.value_objects.parse_result import ParseResult
from ....domain.services.parse_service import ParseService
from ....domain.ports.logger_port import LoggerPort
from ....domain.exceptions.parsing_error import InvalidParseRule, ParseExecutionError

@dataclass
class ParseGeneratedOutputRequest:
    text: str
    rules: List[ParseRule]
    require_all_rules: bool = True

@dataclass
class ParseGeneratedOutputResponse:
    parse_result: ParseResult
    execution_time: float
    total_matches: int
    successful_rules: List[str]
    failed_rules: List[str]

class ParseGeneratedOutputUseCase:
    def __init__(self, parse_service: ParseService, logger: LoggerPort):
        self.parse_service = parse_service
        self.logger = logger

    def execute(self, request: ParseGeneratedOutputRequest) -> ParseGeneratedOutputResponse:
        self._validate_request(request)
        
        start_time = datetime.now()
        
        try:
            parse_result = self.parse_service.parse_text(
                text=request.text,
                rules=request.rules
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Determine successful and failed rules
            rule_names = {rule.name for rule in request.rules}
            matched_rules = set(parse_result.metrics.rules_matched)
            failed_rules = rule_names - matched_rules
            
            if request.require_all_rules and failed_rules:
                raise ParseExecutionError(
                    list(failed_rules)[0],
                    "Required rule did not match any content"
                )
            
            return ParseGeneratedOutputResponse(
                parse_result=parse_result,
                execution_time=execution_time,
                total_matches=parse_result.metrics.total_matches,
                successful_rules=list(matched_rules),
                failed_rules=list(failed_rules)
            )
            
        except Exception as e:
            self.logger.log(
                level="ERROR",
                message=f"Parsing failed: {str(e)}",
                context={"rules": [rule.name for rule in request.rules]}
            )
            raise

    def _validate_request(self, request: ParseGeneratedOutputRequest) -> None:
        if not request.text.strip():
            raise InvalidParseRule("any", "Input text cannot be empty")
        if not request.rules:
            raise InvalidParseRule("any", "At least one parse rule must be provided")
        for rule in request.rules:
            if not rule.pattern:
                raise InvalidParseRule(rule.name, "Rule pattern cannot be empty")