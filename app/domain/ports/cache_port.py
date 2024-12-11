# domain/ports/cache_port.py
from abc import ABC, abstractmethod
from typing import Any, Optional
from datetime import timedelta

class CachePort(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if found, None otherwise
        """
        pass
    
    @abstractmethod
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[timedelta] = None
    ) -> bool:
        """
        Store a value in cache.
        
        Args:
            key: Cache key
            value: Value to store
            ttl: Optional time-to-live duration
            
        Returns:
            True if value was cached successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        Delete a value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if value was deleted, False otherwise
        """
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all cached values."""
        pass
