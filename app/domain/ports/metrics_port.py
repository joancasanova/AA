# domain/ports/metrics_port.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime

class MetricsPort(ABC):
    @abstractmethod
    def record_counter(
        self,
        name: str,
        value: int = 1,
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Record a counter metric.
        
        Args:
            name: Metric name
            value: Value to add to counter
            tags: Optional tags for the metric
        """
        pass
    
    @abstractmethod
    def record_gauge(
        self,
        name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Record a gauge metric.
        
        Args:
            name: Metric name
            value: Current value
            tags: Optional tags for the metric
        """
        pass
    
    @abstractmethod
    def record_histogram(
        self,
        name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Record a histogram metric.
        
        Args:
            name: Metric name
            value: Value to add to histogram
            tags: Optional tags for the metric
        """
        pass
    
    @abstractmethod
    def start_timer(self, name: str) -> Any:
        """
        Start a timer for measuring durations.
        
        Args:
            name: Timer name
            
        Returns:
            Timer context manager or object
        """
        pass