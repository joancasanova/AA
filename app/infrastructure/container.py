# infrastructure/container.py
from dependency_injector import containers, providers
from typing import Optional
from sqlalchemy.orm import Session

from .config.settings import Settings
from .config.environment import EnvironmentManager
from .persistence.database import Database
from .persistence.repositories.benchmark_repository import BenchmarkRepository
from .persistence.repositories.verification_repository import VerificationRepository
from .external.embeddings.embedder_model import EmbedderModel
from .external.llm.instruct_model import InstructModel
from .logging.logger import ApplicationLogger
from .persistence.unit_of_work import UnitOfWork

from ..application.use_cases.benchmark.run_benchmark_use_case import RunBenchmarkUseCase
from ..application.use_cases.generation.generate_text_use_case import GenerateTextUseCase
from ..application.use_cases.parsing.parse_generated_output_use_case import ParseGeneratedOutputUseCase
from ..application.use_cases.verification.verify_text_use_case import VerifyTextUseCase

from ..domain.services.parse_service import ParseService
from ..domain.services.verifier_service import VerifierService
from ..domain.services.metrics_service import MetricsService

class Container(containers.DeclarativeContainer):
    """Dependency Injection Container"""

    # Configuration
    config = providers.Singleton(Settings)
    env_manager = providers.Singleton(EnvironmentManager)

    # Logging
    logger = providers.Singleton(
        ApplicationLogger,
        name="app",
        log_level=config.provided.app.DEBUG and "DEBUG" or "INFO",
        log_dir="logs"
    )

    # Database
    database = providers.Singleton(
        Database,
        connection_string=config.provided.database.connection_string
    )

    # Session Factory
    session_factory = providers.Factory(
        database.provided.get_session
    )

    # External Services
    embedder = providers.Singleton(
        EmbedderModel,
        model_name=config.provided.embeddings.MODEL_NAME,
        device=config.provided.embeddings.DEVICE,
        cache_dir=config.provided.embeddings.CACHE_DIR
    )

    llm = providers.Singleton(
        InstructModel,
        model_name=config.provided.llm.MODEL_NAME,
        device=config.provided.llm.DEVICE,
        cache_dir=config.provided.llm.CACHE_DIR,
        max_length=config.provided.llm.MAX_LENGTH
    )

    # Repositories
    benchmark_repository = providers.Factory(
        BenchmarkRepository,
        session=session_factory
    )

    verification_repository = providers.Factory(
        VerificationRepository,
        session=session_factory
    )

    # Unit of Work
    unit_of_work = providers.Factory(
        UnitOfWork,
        session=session_factory
    )

    # Domain Services
    parse_service = providers.Factory(
        ParseService
    )

    verifier_service = providers.Factory(
        VerifierService,
        embeddings=embedder,
        llm=llm
    )

    metrics_service = providers.Factory(
        MetricsService
    )

    # Use Cases
    generate_text_use_case = providers.Factory(
        GenerateTextUseCase,
        llm=llm,
        logger=logger
    )

    parse_generated_output_use_case = providers.Factory(
        ParseGeneratedOutputUseCase,
        parse_service=parse_service,
        logger=logger
    )

    verify_text_use_case = providers.Factory(
        VerifyTextUseCase,
        verifier_service=verifier_service,
        logger=logger
    )

    run_benchmark_use_case = providers.Factory(
        RunBenchmarkUseCase,
        verifier_service=verifier_service,
        metrics_service=metrics_service,
        repository=benchmark_repository,
        logger=logger
    )

    @classmethod
    def init_app(cls, settings: Optional[Settings] = None) -> 'Container':
        """Initialize the container with application settings."""
        container = cls()
        
        if settings:
            container.config.override(settings)
        
        # Initialize database
        container.database().create_database()
        
        return container