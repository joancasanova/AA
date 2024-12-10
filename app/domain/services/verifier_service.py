# domain/services/verifier_service.py
import logging
from app.domain.entities import VerificationMethod, VerificationMethodType

logger = logging.getLogger(__name__)

class VerifierService:
    def __init__(self):
        logger.info("VerifierService initialized")

    def verify_embedding_method(self, method: VerificationMethod, get_similarity, response: str) -> bool:
        logger.info(f"Verifying embedding method with response: {response}")
        sim = get_similarity(method.embedding_settings.reference_text, response)
        low = method.embedding_settings.lower_threshold
        up = method.embedding_settings.upper_threshold
        result = (sim > low) and (sim < up)
        logger.debug(f"Similarity: {sim}, Lower Threshold: {low}, Upper Threshold: {up}, Result: {result}")
        return result

    def verify_consensus_method(self, method: VerificationMethod, generate_responses, entries) -> bool:
        logger.info(f"Verifying consensus method with entries: {entries}")
        cs = method.consensus_settings
        # Try to fill placeholders from entries
        placeholder_values = {}
        for ph in cs.placeholders:
            found = False
            for e in entries:
                if ph in e.data:
                    placeholder_values[ph] = e.data[ph]
                    found = True
                    break
            if not found:
                logger.warning(f"Placeholder {ph} not found in entries")
                return False

        final_system = cs.system_prompt
        final_user = cs.user_prompt
        for ph, val in placeholder_values.items():
            final_system = final_system.replace("{" + ph + "}", val)
            final_user = final_user.replace("{" + ph + "}", val)

        responses = generate_responses(final_system, final_user, cs.num_responses, cs.max_new_tokens)
        positives = sum(any(p.lower() in r.lower() for p in cs.positive_responses) for r in responses)
        result = positives >= cs.num_positive_required
        logger.debug(f"Positive responses count: {positives}, Required: {cs.num_positive_required}, Result: {result}")
        return result