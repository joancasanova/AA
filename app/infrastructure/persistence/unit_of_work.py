# infrastructure/persistence/unit_of_work.py
from typing import Optional
from sqlalchemy.orm import Session
from contextlib import contextmanager
import logging
from .repositories.benchmark_repository import BenchmarkRepository
from .repositories.verification_repository import VerificationRepository

logger = logging.getLogger(__name__)

class UnitOfWork:
    def __init__(self, session: Session):
        self.session = session
        self.benchmarks: Optional[BenchmarkRepository] = None
        self.verifications: Optional[VerificationRepository] = None

    def __enter__(self):
        self.benchmarks = BenchmarkRepository(self.session)
        self.verifications = VerificationRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
            logger.error(f"Transaction rolled back due to error: {str(exc_val)}")
        else:
            self.commit()

    def commit(self):
        try:
            self.session.commit()
        except Exception as e:
            logger.error(f"Error committing transaction: {str(e)}")
            self.rollback()
            raise

    def rollback(self):
        self.session.rollback()

@contextmanager
def get_unit_of_work(session: Session):
    uow = UnitOfWork(session)
    try:
        with uow:
            yield uow
    except Exception as e:
        logger.error(f"Error in unit of work: {str(e)}")
        raise