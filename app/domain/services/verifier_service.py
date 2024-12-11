# domain/services/verifier_service.py
from typing import List, Dict, Optional, Callable
import logging
from datetime import datetime
from ..model.entities.verification import (
    VerificationMethod, VerificationMethodType, VerificationMode,
    VerificationResult, VerificationSummary
)
from ..model.value_objects.verification_status import VerificationStatus
from ..model.value_objects.similarity_score import SimilarityScore
from ..ports.embeddings_port import EmbeddingsPort
from ..ports.llm_port import LLMPort

logger = logging.getLogger(__name__)

class VerifierService:
    def __init__(self, embeddings: EmbeddingsPort, llm: LLMPort):
        self.embeddings = embeddings
        self.llm = llm

    def verify_text(
        self,
        text: str,
        methods: List[VerificationMethod],
        required_for_confirmed: int,
        required_for_review: int
    ) -> VerificationSummary:
        start_time = datetime.now()
        results: List[VerificationResult] = []
        cumulative_passes = 0

        for method in methods:
            result = self._apply_verification_method(method, text)
            results.append(result)

            if not result.passed and method.mode == VerificationMode.ELIMINATORY:
                final_status = VerificationStatus.DISCARDED
                break
            
            if result.passed and method.mode == VerificationMode.CUMULATIVE:
                cumulative_passes += 1

        else:  # Only executed if no break occurred
            if cumulative_passes >= required_for_confirmed:
                final_status = VerificationStatus.CONFIRMED
            elif cumulative_passes >= required_for_review:
                final_status = VerificationStatus.REVIEW
            else:
                final_status = VerificationStatus.DISCARDED

        verification_time = (datetime.now() - start_time).total_seconds()

        return VerificationSummary(
            results=results,
            final_status=final_status.value,
            verification_time=verification_time
        )

    def _apply_verification_method(
        self,
        method: VerificationMethod,
        text: str
    ) -> VerificationResult:
        if method.method_type == VerificationMethodType.EMBEDDING:
            return self._verify_embedding(method, text)
        elif method.method_type == VerificationMethodType.CONSENSUS:
            return self._verify_consensus(method, text)
        elif method.method_type == VerificationMethodType.REGEX:
            return self._verify_regex(method, text)
        elif method.method_type == VerificationMethodType.CUSTOM:
            return self._verify_custom(method, text)
        else:
            raise ValueError(f"Unknown verification method type: {method.method_type}")

    def _verify_embedding(self, method: VerificationMethod, text: str) -> VerificationResult:
        if not method.reference_text or not method.thresholds:
            raise ValueError("Embedding verification requires reference text and thresholds")

        similarity = self.embeddings.get_similarity(method.reference_text, text)
        passed = method.thresholds.is_within_bounds(similarity.value)

        return VerificationResult(
            method=method,
            passed=passed,
            score=similarity.value,
            details={
                "similarity_score": similarity.value,
                "reference_text": method.reference_text,
                "thresholds": {
                    "lower": method.thresholds.lower_bound,
                    "upper": method.thresholds.upper_bound
                }
            }
        )

    def _verify_consensus(self, method: VerificationMethod, text: str) -> VerificationResult:
        if not method.required_matches:
            raise ValueError("Consensus verification requires required_matches")

        # Generate multiple verifications using LLM
        system_prompt = f"Verify the following text:\n{text}"
        user_prompt = "Is this text valid? Respond with 'yes' or 'no'."
        
        responses = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            num_sequences=5,  # Generate 5 independent verifications
            max_tokens=10  # Short responses expected
        )

        positive_responses = sum(1 for r in responses if r.content.strip().lower() == 'yes')
        passed = positive_responses >= method.required_matches

        return VerificationResult(
            method=method,
            passed=passed,
            score=positive_responses / len(responses),
            details={
                "total_responses": len(responses),
                "positive_responses": positive_responses,
                "required_matches": method.required_matches
            }
        )

    def _verify_regex(self, method: VerificationMethod, text: str) -> VerificationResult:
        import re
        if not hasattr(method, 'pattern'):
            raise ValueError("Regex verification requires a pattern")

        pattern = getattr(method, 'pattern')
        matches = re.findall(pattern, text)
        passed = len(matches) > 0

        return VerificationResult(
            method=method,
            passed=passed,
            score=1.0 if passed else 0.0,
            details={
                "matches_found": len(matches),
                "pattern": pattern
            }
        )

    def _verify_custom(self, method: VerificationMethod, text: str) -> VerificationResult:
        if not hasattr(method, 'verification_function'):
            raise ValueError("Custom verification requires a verification_function")

        verification_func = getattr(method, 'verification_function')
        result = verification_func(text)
        
        if isinstance(result, tuple):
            passed, score = result
        else:
            passed = result
            score = 1.0 if passed else 0.0

        return VerificationResult(
            method=method,
            passed=passed,
            score=score,
            details={
                "custom_verification": "Applied custom verification function"
            }
        )