# infrastructure/persistence/models/benchmark_model.py
from sqlalchemy import Column, String, JSON, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import BaseModel

class BenchmarkModel(BaseModel):
    __tablename__ = 'benchmarks'

    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    configuration = Column(JSON, nullable=False)
    metrics = Column(JSON)
    tags = Column(JSON)
    metadata = Column(JSON)
    
    executions = relationship("BenchmarkExecutionModel", back_populates="benchmark")

class BenchmarkExecutionModel(BaseModel):
    __tablename__ = 'benchmark_executions'

    benchmark_id = Column(String(36), ForeignKey('benchmarks.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    success_rate = Column(Float, nullable=False)
    total_entries = Column(Integer, nullable=False)
    results = Column(JSON, nullable=False)
    
    benchmark = relationship("BenchmarkModel", back_populates="executions")
