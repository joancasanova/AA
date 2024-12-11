# infrastructure/config/environment.py
from enum import Enum
from typing import Optional
import os
from pathlib import Path

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

class EnvironmentManager:
    def __init__(self):
        self._env = Environment(os.getenv("APP_ENV", "development").lower())
        self._config_path = Path(os.getenv("CONFIG_PATH", "config"))

    @property
    def is_development(self) -> bool:
        return self._env == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        return self._env == Environment.PRODUCTION

    @property
    def is_testing(self) -> bool:
        return self._env == Environment.TESTING

    def get_config_file(self, filename: str) -> Optional[Path]:
        env_specific = self._config_path / self._env.value / filename
        if env_specific.exists():
            return env_specific
        
        default = self._config_path / filename
        return default if default.exists() else None