# infrastructure/external/model_cache.py
from typing import Optional, Dict, Any
import os
import shutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelCache:
    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized model cache at {cache_dir}")

    def get_model_path(self, model_name: str) -> Optional[str]:
        model_dir = self.cache_dir / model_name
        return str(model_dir) if model_dir.exists() else None

    def save_model(self, model_name: str, model_data: Dict[str, Any]) -> str:
        model_dir = self.cache_dir / model_name
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # Save model data
        try:
            # Implementation depends on model format
            pass
        except Exception as e:
            logger.error(f"Error saving model {model_name}: {str(e)}")
            raise

        return str(model_dir)

    def clear_cache(self, model_name: Optional[str] = None) -> None:
        try:
            if model_name:
                model_dir = self.cache_dir / model_name
                if model_dir.exists():
                    shutil.rmtree(model_dir)
                    logger.info(f"Cleared cache for model {model_name}")
            else:
                shutil.rmtree(self.cache_dir)
                self.cache_dir.mkdir(parents=True)
                logger.info("Cleared entire model cache")
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            raise

    def get_cache_size(self) -> int:
        total_size = 0
        for dirpath, _, filenames in os.walk(self.cache_dir):
            for filename in filenames:
                total_size += os.path.getsize(os.path.join(dirpath, filename))
        return total_size