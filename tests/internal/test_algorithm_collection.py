import pytest

from src.internal.algorithm_collection import AlgorithmCollection
from src.internal.constants import DEFAULT_ALGORITHMS_CATALOG_PATH
from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.errors import ErrorMessageTemplateEnum as ErrMsgTmpl
from src.internal.schemas.algorithm_definition_schema import AlgorithmDefinitionSchema
from src.internal.schemas.definition_schema import DefinitionSchema
from tests import (
    FIB_DEF,
    FIB_FUNC,
    FIB_NAME,
    SUM_DEF,
    SUM_FUNC,
    SUM_NAME,
    SUM_TESTS,
    WRONG_FIB_TESTS,
)


class TestAlgorithmCollection:
    """Тесты для класса AlgorithmCollection."""

    def test_valid_collection(self, fib_algo_dir, tmp_path):
        """Проверяет создание экземпляра класса с дефлотными параметрами"""
        algo_collection = AlgorithmCollection(str(tmp_path))

        assert algo_collection.has_algorithm(FIB_NAME)

    def test_empty_catalog(self, tmp_path):
        """Проверяет ошибку при отсутствии алгоритмов в каталоге"""
        with pytest.raises(RuntimeError) as error:
            AlgorithmCollection(str(tmp_path))

        assert str(error.value) == ErrMsg.NO_ALGORITHMS

    def test_build_failed(self, tmp_path, algo_dir):
        """Проверяет ошибку сборки алгоритма"""
        algo_dir(FIB_NAME, FIB_DEF, FIB_FUNC, WRONG_FIB_TESTS)
        with pytest.raises(RuntimeError) as error:
            AlgorithmCollection(str(tmp_path))

        assert str(error.value) == ErrMsg.UNIT_TEST_FAILED

    def test_two_algorithms(self, fib_algo_dir, algo_dir, tmp_path):
        """Проверяет создание экземпляра класса с несколькими алгоритмами"""
        algo_dir(SUM_NAME, SUM_DEF, SUM_FUNC, SUM_TESTS)
        algo_collection = AlgorithmCollection(str(tmp_path))

        assert algo_collection.has_algorithm(FIB_NAME)
        assert algo_collection.has_algorithm(SUM_NAME)

    def test_has_algorithm(self, fib_algo_dir, tmp_path):
        """Проверяет наличие алгоритма"""
        algo_collection = AlgorithmCollection(str(tmp_path))

        assert algo_collection.has_algorithm(FIB_NAME)
        assert not algo_collection.has_algorithm("not_existed")

    def test_get_algorithm_list(self, fib_algo_dir, tmp_path):
        """Проверяет получение списка алгоритмов"""
        algo_collection = AlgorithmCollection(str(tmp_path))
        algorithms = algo_collection.get_algorithm_list()

        assert isinstance(algorithms, list)
        assert len(algorithms) == 1
        assert isinstance(algorithms[0], DefinitionSchema)
        assert algorithms[0].name == FIB_NAME

    def test_get_algorithm_definition(self, fib_algo_dir, tmp_path):
        """Проверяет получение описания алгоритма"""
        algo_collection = AlgorithmCollection(str(tmp_path))
        algo_definition = algo_collection.get_algorithm_definition(FIB_NAME)

        assert isinstance(algo_definition, AlgorithmDefinitionSchema)
        assert algo_definition.name == FIB_NAME

    def test_get_not_existed_algorithm_definition(self, fib_algo_dir, tmp_path):
        """Проверяет ошибку запроса описания несуществующего алгоритма"""
        algo_collection = AlgorithmCollection(str(tmp_path))
        with pytest.raises(ValueError) as error:
            algo_collection.get_algorithm_definition("not_existed")

        assert str(error.value) == ErrMsgTmpl.ALGORITHM_NOT_EXISTS.format("not_existed")

    def test_get_algorithm_result(self, fib_algo_dir, tmp_path):
        """Проверяет выполнение алгоритма"""
        algo_collection = AlgorithmCollection(str(tmp_path))
        result = algo_collection.get_algorithm_result(FIB_NAME, {"n": 1})

        assert result == {"result": 1}

    def test_get_not_existed_algorithm_result(self, fib_algo_dir, tmp_path):
        """Проверяет ошибку выполнения несуществующего алгоритма"""
        algo_collection = AlgorithmCollection(str(tmp_path))
        with pytest.raises(ValueError) as error:
            algo_collection.get_algorithm_result("not_existed", {"n": 1})

        assert str(error.value) == ErrMsgTmpl.ALGORITHM_NOT_EXISTS.format("not_existed")

    def test_build_real_algorithms(self):
        """Проверяет создание экземпляра класса со сборкой имеющихся в приложении
        алгоритмов"""
        algo_collection = AlgorithmCollection(DEFAULT_ALGORITHMS_CATALOG_PATH)

        algorithms = algo_collection.get_algorithm_list()
        assert len(algorithms) > 0


if __name__ == "__main__":
    pytest.main(["-k", "TestAlgorithmCollection"])
