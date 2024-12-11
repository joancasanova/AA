# infrastructure/persistence/repositories/base_repository.py
from typing import Generic, TypeVar, List, Optional, Dict, Any
from abc import ABC, abstractmethod
from datetime import datetime
import logging
from sqlalchemy.orm import Session
from ....domain.ports.repository_port import RepositoryPort

T = TypeVar('T')

class BaseRepository(RepositoryPort[T], Generic[T]):
    def __init__(self, session: Session):
        self.session = session
        self.logger = logging.getLogger(self.__class__.__name__)

    def save(self, entity: T) -> T:
        try:
            self.session.add(entity)
            self.session.commit()
            return entity
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error saving entity: {str(e)}")
            raise

    def get_by_id(self, entity_id: str) -> Optional[T]:
        try:
            return self.session.query(self._get_model()).filter_by(id=entity_id).first()
        except Exception as e:
            self.logger.error(f"Error retrieving entity by ID: {str(e)}")
            raise

    def get_all(self) -> List[T]:
        try:
            return self.session.query(self._get_model()).all()
        except Exception as e:
            self.logger.error(f"Error retrieving all entities: {str(e)}")
            raise

    def delete(self, entity_id: str) -> bool:
        try:
            entity = self.get_by_id(entity_id)
            if entity:
                self.session.delete(entity)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error deleting entity: {str(e)}")
            raise

    def update(self, entity: T) -> T:
        try:
            self.session.merge(entity)
            self.session.commit()
            return entity
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error updating entity: {str(e)}")
            raise

    @abstractmethod
    def _get_model(self):
        """Return the SQLAlchemy model class for this repository"""
        pass