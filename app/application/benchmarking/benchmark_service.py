# app/application/benchmarking/benchmark_service.py
from typing import List, Dict, Any
import logging
from datetime import datetime
from app.application.orchestration import Pipeline, StageType
from .types import BenchmarkDataset, BenchmarkResult, LabelConfiguration
from .metrics import MetricsCalculator

logger = logging.getLogger(__name__)

class BenchmarkService:
    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline
        logger.info("BenchmarkService initialized")

    def run_benchmark(
        self,
        dataset: BenchmarkDataset,
        stages: List[Any]  # List[StageConfig] but avoiding circular import
    ) -> BenchmarkResult:
        """
        Run benchmark on the given dataset using the specified pipeline stages.
        """
        # Validate pipeline ends with verify stage
        if not stages or stages[-1].stage_type != StageType.VERIFY:
            raise ValueError("Pipeline must end with a verify stage")

        execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        execution_results = []
        correct_predictions: Dict[str, int] = {config.label: 0 for config in dataset.label_configs}
        total_predictions: Dict[str, int] = {config.label: 0 for config in dataset.label_configs}

        # Process each entry in the dataset
        for entry in dataset.data:
            # Run the pipeline
            result = self.pipeline.execute(stages, entry)
            execution_results.append(result)

            # Get the final verification result (last stage, last output)
            final_stage_result = result.stages_results[-1]
            if isinstance(final_stage_result.output_data, list):
                verification_results = final_stage_result.output_data
            else:
                verification_results = [final_stage_result.output_data]

            # Check each verification result against label configurations
            entry_label = entry.get('label')  # Assuming each entry has a 'label' field
            if entry_label:
                label_config = next(
                    (config for config in dataset.label_configs if config.label == entry_label),
                    None
                )
                
                if label_config:
                    total_predictions[entry_label] += 1
                    
                    # Check if any verification result matches the expected configuration
                    for ver_result in verification_results:
                        if self._matches_label_config(ver_result, label_config):
                            correct_predictions[entry_label] += 1
                            break

        # Calculate metrics
        metrics = MetricsCalculator.calculate_metrics(
            correct_predictions,
            dataset.label_configs,
            total_predictions
        )

        return BenchmarkResult(
            metrics=metrics,
            execution_results=execution_results,
            total_samples=len(dataset.data),
            correct_predictions=correct_predictions,
            total_predictions=total_predictions,
            execution_id=execution_id,
            timestamp=datetime.now().isoformat()
        )

    def _matches_label_config(self, verification_result: Any, label_config: LabelConfiguration) -> bool:
        """
        Check if a verification result matches the expected configuration for its label.
        """
        # Check final status
        if verification_result.final_status != label_config.expected_status:
            return False

        # Check passed methods
        if set(verification_result.verification_methods_passed) != set(label_config.expected_methods_passed):
            return False

        return True