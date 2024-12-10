# application/use_cases/parse_generated_output_use_case.py
import logging
from app.domain.entities import GeneratedResult, ParsedResult, ParseEntry, ParseConfiguration
from app.domain.services.parse_service import ParseService

logger = logging.getLogger(__name__)

class ParseGeneratedOutputUseCase:
    def __init__(self, parse_service: ParseService):
        self.parse_service = parse_service
        logger.info("ParseGeneratedOutputUseCase initialized")

    def execute(self, result: GeneratedResult, config: ParseConfiguration) -> ParsedResult:
        logger.info(f"Parsing result: {result.response} with config: {config}")
        entries_data = self.parse_service.parse_text(result.response, config)
        entries = [ParseEntry(e) for e in entries_data]
        parsed_result = ParsedResult(entries)
        logger.debug(f"Parsed result: {parsed_result.entries}")
        return parsed_result