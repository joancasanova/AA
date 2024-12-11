# application/use_cases/verification/verify_text_use_case.py
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from ....domain.model.entities.verification import VerificationMethod, VerificationSummary
from ....domain.services.verifier_service import VerifierService
from ....domain.ports.logger_port import LoggerPort
from ....domain.exceptions.verification_error import InvalidVerificationMethod, VerificationExecutionError

@dataclass
class VerifyTextRequest:
    text: str
    methods: List[VerificationMethod]
    required_for_confirmed: int
    required_for_review: int
    context: Optional[dict] = None

@dataclass
class VerifyTextResponse:
    verification_summary: VerificationSummary
    execution_time: float
    success_rate: float

class VerifyTextUseCase:
    def __init__(self, verifier_service: VerifierService, logger: LoggerPort):
        self.verifier_service = verifier_service
        self.logger = logger

    def execute(self, request: VerifyTextRequest) -> VerifyTextResponse:
        self._validate_request(request)
        
        start_time = datetime.now()
        
        try:
            verification_summary = self.verifier_service.verify_text(
                text=request.text,
                methods=request.methods,
                required_for_confirmed=request.required_for_confirmed,
                required_for_review=request.required_for_review
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            success_rate = verification_summary.success_rate
            
            self.logger.log(
                level="INFO",
                message="Text verification completed",
                context={
                    "success_rate": success_rate,
                    "execution_time": execution_time,
                    "user_context": request.context
                }
            )
            
            return VerifyTextResponse(
                verification_summary=verification_summary,
                execution_time=execution_time,
                success_rate=success_rate
            )
            
        except Exception as e:
            self.logger.log(
                level="ERROR",
                message=f"Verification failed: {str(e)}",
                context={"methods": [m.name for m in request.methods]}
            )
            raise

    def _validate_request(self, request: VerifyTextRequest) -> None:
        if not request.text.strip():
            raise InvalidVerificationMethod("any", "Input text cannot be empty")
        if not request.methods:
            raise InvalidVerificationMethod("any", "At least one verification method must be provided")
        if request.required_for_confirmed <= request.required_for_review:
            raise InvalidVerificationMethod(
                "any",
                "required_for_confirmed must be greater than required_for_review"
            )