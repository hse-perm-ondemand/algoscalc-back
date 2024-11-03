import logging
import logging.config

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import LOGGING_CONFIG, Settings
from src.internal.algorithm_collection import AlgorithmCollection
from src.routers.algorithms import router as algorithms_router
from src.routers.error_handlers import init_error_handlers


def create_app(settings: Settings = None) -> FastAPI:
    """Создает экземпляра приложения. Если переданы параметры приложения,
    то они используются для создания приложения."""
    if not settings:
        settings = Settings()

    logger = None
    if settings.USE_LOGGER:
        logging.config.dictConfig(LOGGING_CONFIG)
        logger = logging.getLogger(__name__)
        logger.setLevel(settings.LOG_LEVEL)
        logger.info("Start app")

    app = FastAPI(
        title="AlgosСalc API",
        description="API для приложения Онлайн-калькулятор, предназначенного для "
        "проведения практических занятий со студентами по разработке алгоритмов.",
        version=settings.VERSION,
    )
    app.include_router(router=algorithms_router)
    init_error_handlers(app, logger)
    app.state.algorithms = AlgorithmCollection(
        algorithms_catalog_path=settings.ALGORITHMS_CATALOG_PATH,
        execute_timeout=settings.EXECUTE_TIMEOUT,
    )

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    return app


def start():
    """Запускает приложение."""
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    start()
