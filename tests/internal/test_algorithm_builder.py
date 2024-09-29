import pytest

from src.internal.algorithm_builder import AlgorithmBuilder
from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.errors import ErrorMessageTemplateEnum as ErrMsgTmpl
from tests import (
    EMPTY_STRING_CASES,
    FIB_DEF,
    FIB_FUNC,
    FIB_NAME,
    FIB_TESTS,
    NOT_INT_CASES,
    NOT_STRING_CASES,
    WRONG_FIB_TESTS,
    Case,
)


class TestAlgorithmBuilder:
    """Тесты для класса AlgorithmBuilder."""

    def test_valid_builder(self, fib_algo_dir):
        """Проверяет создание экземпляра класса с дефлотными параметрами"""
        builder = AlgorithmBuilder()
        algo_executor = builder.build_algorithm(fib_algo_dir)

        assert algo_executor.definition.name == FIB_NAME

    @pytest.mark.parametrize(
        "test_case",
        NOT_INT_CASES,
        ids=[test_case.description for test_case in NOT_INT_CASES],
    )
    def test_not_int_execute_timeout(
        self,
        fib_algo_dir,
        test_case: Case,
    ):
        """Проверяет ошибку указания не числового таймаута"""
        with pytest.raises(TypeError) as error:
            AlgorithmBuilder(execute_timeout=test_case.value)
        assert str(error.value) == ErrMsg.NON_INT_TIMEOUT

    def test_negative_execute_timeout(self, fib_algo_dir):
        """Проверяет ошибку указания отрицательного таймаута"""
        with pytest.raises(ValueError) as error:
            AlgorithmBuilder(execute_timeout=-1)
        assert str(error.value) == ErrMsg.NEG_INT_TIMEOUT

    @pytest.mark.parametrize(
        "test_case",
        NOT_STRING_CASES,
        ids=[test_case.description for test_case in NOT_STRING_CASES],
    )
    def test_not_str_def_file_name(
        self,
        fib_algo_dir,
        test_case: Case,
    ):
        """Проверяет ошибку указания не короректного имени файла с описанием
        алгоритма"""
        with pytest.raises(TypeError) as error:
            AlgorithmBuilder(definition_file_name=test_case.value)
        assert str(error.value) == ErrMsgTmpl.NON_STRING_PARAM.format(
            "definition_file_name"
        )

    @pytest.mark.parametrize(
        "test_case",
        EMPTY_STRING_CASES,
        ids=[test_case.description for test_case in EMPTY_STRING_CASES],
    )
    def test_empty_def_file_name(
        self,
        fib_algo_dir,
        test_case: Case,
    ):
        """Проверяет ошибку указания не короректного имени файла с описанием
        алгоритма"""
        with pytest.raises(ValueError) as error:
            AlgorithmBuilder(definition_file_name=test_case.value)
        assert str(error.value) == ErrMsgTmpl.EMPTY_STRING_PARAM.format(
            "definition_file_name"
        )

    @pytest.mark.parametrize(
        "test_case",
        NOT_STRING_CASES,
        ids=[test_case.description for test_case in NOT_STRING_CASES],
    )
    def test_not_str_func_file_name(
        self,
        fib_algo_dir,
        test_case: Case,
    ):
        """Проверяет ошибку указания не короректного имени файла с функцией для
        выполнения алгоритма"""
        with pytest.raises(TypeError) as error:
            AlgorithmBuilder(function_file_name=test_case.value)
        assert str(error.value) == ErrMsgTmpl.NON_STRING_PARAM.format(
            "function_file_name"
        )

    @pytest.mark.parametrize(
        "test_case",
        EMPTY_STRING_CASES,
        ids=[test_case.description for test_case in EMPTY_STRING_CASES],
    )
    def test_empty_func_file_name(
        self,
        fib_algo_dir,
        test_case: Case,
    ):
        """Проверяет ошибку указания не короректного имени файла с функцией для
        выполнения алгоритма"""
        with pytest.raises(ValueError) as error:
            AlgorithmBuilder(function_file_name=test_case.value)
        assert str(error.value) == ErrMsgTmpl.EMPTY_STRING_PARAM.format(
            "function_file_name"
        )

    @pytest.mark.parametrize(
        "test_case",
        NOT_STRING_CASES,
        ids=[test_case.description for test_case in NOT_STRING_CASES],
    )
    def test_not_str_test_file_name(
        self,
        fib_algo_dir,
        test_case: Case,
    ):
        """Проверяет ошибку указания не короректного имени файла с тестами для
        алгоритма"""
        with pytest.raises(TypeError) as error:
            AlgorithmBuilder(test_file_name=test_case.value)
        assert str(error.value) == ErrMsgTmpl.NON_STRING_PARAM.format("test_file_name")

    @pytest.mark.parametrize(
        "test_case",
        EMPTY_STRING_CASES,
        ids=[test_case.description for test_case in EMPTY_STRING_CASES],
    )
    def test_empty_test_file_name(
        self,
        fib_algo_dir,
        test_case: Case,
    ):
        """Проверяет ошибку указания не короректного имени файла с тестами для
        алгоритма"""
        with pytest.raises(ValueError) as error:
            AlgorithmBuilder(test_file_name=test_case.value)
        assert str(error.value) == ErrMsgTmpl.EMPTY_STRING_PARAM.format(
            "test_file_name"
        )

    def test_build_unit_tests_failed(self, algo_dir):
        """Проверяет ошибку сборки алгоритма при провале модульных тестов"""
        dir_name = algo_dir(FIB_NAME, FIB_DEF, FIB_FUNC, WRONG_FIB_TESTS)
        builder = AlgorithmBuilder()

        with pytest.raises(RuntimeError) as error:
            builder.build_algorithm(dir_name)

        assert str(error.value) == ErrMsg.UNIT_TEST_FAILED

    def test_build_no_def(self, algo_dir):
        """Проверяет ошибку сборки алгоритма при отсутствии описания алгоритма"""
        dir_name = algo_dir(FIB_NAME, None, FIB_FUNC, FIB_TESTS)
        builder = AlgorithmBuilder()

        with pytest.raises(FileNotFoundError):
            builder.build_algorithm(dir_name)

    def test_build_no_func(self, algo_dir):
        """Проверяет ошибку сборки алгоритма при отсутствии функции для алгоритма"""
        dir_name = algo_dir(FIB_NAME, FIB_DEF, None, FIB_TESTS)
        builder = AlgorithmBuilder()

        with pytest.raises(FileNotFoundError):
            builder.build_algorithm(dir_name)

    def test_build_no_test(self, algo_dir):
        """Проверяет ошибку сборки алгоритма при отсутствии тестов для алгоритма"""
        dir_name = algo_dir(FIB_NAME, FIB_DEF, FIB_FUNC, None)
        builder = AlgorithmBuilder()

        with pytest.raises(RuntimeError) as error:
            builder.build_algorithm(dir_name)

        assert str(error.value) == ErrMsg.UNIT_TEST_FAILED


if __name__ == "__main__":
    pytest.main(["-k", "TestAlgorithmBuilder"])
