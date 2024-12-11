# infrastructure/persistence/repositories/benchmark_repository.py
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import and_, or_
from ....domain.model.entities.benchmark import BenchmarkResult
from .base_repository import BaseRepository
from ..models.benchmark_model import BenchmarkModel

class BenchmarkRepository(BaseRepository[BenchmarkResult]):
    def _get_model(self):
        return BenchmarkModel

    def find_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[BenchmarkResult]:
        try:
            return (
                self.session.query(BenchmarkModel)
                .filter(and_(
                    BenchmarkModel.created_at >= start_date,
                    BenchmarkModel.created_at <= end_date
                ))
                .all()
            )
        except Exception as e:
            self.logger.error(f"Error finding benchmarks by date range: {str(e)}")
            raise

    def find_by_tags(self, tags: List[str]) -> List[BenchmarkResult]:
        try:
            return (
                self.session.query(BenchmarkModel)
                .filter(BenchmarkModel.tags.contains(tags))
                .all()
            )
        except Exception as e:
            self.logger.error(f"Error finding benchmarks by tags: {str(e)}")
            raise

    def get_latest_execution(self) -> Optional[BenchmarkResult]:
        try:
            return (
                self.session.query(BenchmarkModel)
                .order_by(BenchmarkModel.created_at.desc())
                .first()
            )
        except Exception as e:
            self.logger.error(f"Error getting latest execution: {str(e)}")
            raise