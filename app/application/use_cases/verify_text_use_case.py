# application/use_cases/verify_text_use_case.py
import logging
from app.domain.entities import ParsedResult, VerificationProcess, VerificationMethodType, VerificationMethodMode
from app.domain.services.verifier_service import VerifierService
from typing import Callable, List

logger = logging.getLogger(__name__)

class VerifyTextUseCase:
    def __init__(self, verifier_service: VerifierService, get_similarity: Callable[[str, str], float], generate_responses: Callable[[str, str, int, int], List[str]]):
        self.verifier_service = verifier_service
        self.get_similarity = get_similarity
        self.generate_responses = generate_responses
        logger.info("VerifyTextUseCase initialized")

    def execute(self, result: ParsedResult, process: VerificationProcess) -> ParsedResult:
        logger.info(f"Verifying text with result: {result.entries} and process: {process}")
        acumulativos_superados = 0
        for method in process.methods:
            passed = False
            if method.method_type == VerificationMethodType.EMBEDDING:
                # Take text from some placeholder. Here we simplify: take first entry and first placeholder available:
                if not result.entries or not result.entries[0].data:
                    passed = False
                    logger.warning("No entries or data found in result")
                else:
                    # First value of the dict:
                    text_to_check = next(iter(result.entries[0].data.values()))
                    passed = self.verifier_service.verify_embedding_method(method, self.get_similarity, text_to_check)
                    logger.debug(f"Embedding verification result: {passed}")

            elif method.method_type == VerificationMethodType.CONSENSUS:
                passed = self.verifier_service.verify_consensus_method(method, self.generate_responses, result.entries)
                logger.debug(f"Consensus verification result: {passed}")

            if not passed:
                result.verification_methods_failed.append(method.name)
                logger.debug(f"Method {method.name} failed verification")
                if method.mode == VerificationMethodMode.ELIMINATORIO:
                    result.final_status = "descartada"
                    logger.info("Final status set to 'descartada'")
                    return result
            else:
                result.verification_methods_passed.append(method.name)
                logger.debug(f"Method {method.name} passed verification")
                if method.mode == VerificationMethodMode.ACUMULATIVO:
                    acumulativos_superados += 1

        if acumulativos_superados >= process.required_for_confirmed:
            result.final_status = "confirmada"
            logger.info("Final status set to 'confirmada'")
        elif acumulativos_superados >= process.required_for_review:
            result.final_status = "a revisar"
            logger.info("Final status set to 'a revisar'")
        else:
            result.final_status = "descartada"
            logger.info("Final status set to 'descartada'")

        logger.debug(f"Final verification result: {result}")
        return result