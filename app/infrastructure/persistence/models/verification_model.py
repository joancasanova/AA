# infrastructure/persistence/models/verification_model.py
from sqlalchemy import Column, String, JSON, Float, DateTime
from .base_model import BaseModel

class VerificationModel(BaseModel):
    __tablename__ = 'verifications'

    input_text = Column(String, nullable=False)
    methods = Column(JSON, nullable=False)
    final_status = Column(String(50), nullable=False)
    verification_time = Column(Float, nullable=False)
    results = Column(JSON, nullable=False)
    metadata = Column(JSON)

# infrastructure/persistence/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging
from typing import Generator
from .models.base_model import Base

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def create_database(self) -> None:
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise

    @contextmanager
    def get_session(self) -> Generator:
        session = self.SessionLocal()
        try:
            yield session
        except Exception as e:
            session.rollback()
            logger.error(f"Session error: {str(e)}")
            raise
        finally:
            session.close()