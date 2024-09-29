from typing import Generator

import pytest
from fastapi.testclient import TestClient

from src.config import Settings
from src.main import create_app
from tests import SUM_DEF, SUM_FUNC, SUM_NAME, SUM_TESTS


@pytest.fixture()
def client(tmp_path, algo_dir, fib_algo_dir) -> Generator:
    """Создает клиента для тестирования"""
    algo_dir(SUM_NAME, SUM_DEF, SUM_FUNC, SUM_TESTS)
    test_settings = Settings(
        EXECUTE_TIMEOUT=0, ALGORITHMS_CATALOG_PATH=str(tmp_path), USE_LOGGER=False
    )
    app = create_app(test_settings)

    yield TestClient(app)
