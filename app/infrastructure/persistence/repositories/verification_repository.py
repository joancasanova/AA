# infrastructure/persistence/repositories/verification_repository.py
from typing import List, Optional
from datetime import datetime
from sqlalchemy import and_
from ....domain.model.entities.verification import VerificationSummary
from .base_repository import BaseRepository
from ..models.verification_model import VerificationModel

class VerificationRepository(BaseRepository[VerificationSummary]):
    def _get_model(self):
        return VerificationModel

    def find_by_status(self, status: str) -> List[VerificationSummary]:
        try:
            return (
                self.session.query(VerificationModel)
                .filter(VerificationModel.final_status == status)
                .all()
            )
        except Exception as e:
            self.logger.error(f"Error finding verifications by status: {str(e)}")
            raise

    def get_success_rate(self, time_window_minutes: int = 60) -> float:
        try:
            cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
            total = (
                self.session.query(VerificationModel)
                .filter(VerificationModel.created_at >= cutoff_time)
                .count()
            )
            if total == 0:
                return 0.0

            successful = (
                self.session.query(VerificationModel)
                .filter(and_(
                    VerificationModel.created_at >= cutoff_time,
                    VerificationModel.final_status == "confirmada"
                ))
                .count()
            )
            return successful / total
        except Exception as e:
            self.logger.error(f"Error calculating success rate: {str(e)}")
            raise