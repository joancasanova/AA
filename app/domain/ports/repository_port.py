# domain/ports/repository_port.py
from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')

class RepositoryPort(ABC, Generic[T]):
    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Save an entity to the repository.
        
        Args:
            entity: Entity to save
            
        Returns:
            Saved entity
        """
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Retrieve an entity by its ID.
        
        Args:
            entity_id: ID of the entity to retrieve
            
        Returns:
            Entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Retrieve all entities.
        
        Returns:
            List of all entities
        """
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Delete an entity by its ID.
        
        Args:
            entity_id: ID of the entity to delete
            
        Returns:
            True if entity was deleted, False otherwise
        """
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """
        Update an existing entity.
        
        Args:
            entity: Entity with updated values
            
        Returns:
            Updated entity
        """
        pass