import pytest

from src.internal.data_dimension import DataShapeEnum
from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.errors import ErrorMessageTemplateEnum as ErrMsgTmpl


class TestDataShapeEnum:
    """Набор тестов для проверки класса DataShapeEnum"""

    def test_scalar(self):
        """Проверяет скалярный тип"""
        ds = DataShapeEnum.SCALAR
        assert ds.name == "SCALAR"
        assert ds.value == "SCALAR"

    def test_list(self):
        """Проверяет тип списка"""
        ds = DataShapeEnum.LIST
        assert ds.name == "LIST"
        assert ds.value == "LIST"

    def test_matrix(self):
        """Проверяет тип матрицы"""
        ds = DataShapeEnum.MATRIX
        assert ds.name == "MATRIX"
        assert ds.value == "MATRIX"

    def test_scalar_errors(self):
        """Проверяет функцию контроля скалярных данных"""
        ds = DataShapeEnum.SCALAR
        assert ds.get_shape_errors(1) is None
        assert ds.get_shape_errors("1") is None
        assert ds.get_shape_errors(1.0) is None
        assert ds.get_shape_errors(True) is None
        assert ds.get_shape_errors(None) == ErrMsg.NONE_VALUE
        assert ds.get_shape_errors([]) == ErrMsg.NOT_SCALAR_VALUE

    def test_list_errors(self):
        """Проверяет функцию контроля данных в виде списка"""
        ds = DataShapeEnum.LIST
        assert ds.get_shape_errors([]) is None
        assert ds.get_shape_errors(["1"]) is None
        assert ds.get_shape_errors([1.0, 2.0]) is None
        assert ds.get_shape_errors(None) == ErrMsg.NONE_VALUE
        assert ds.get_shape_errors(1) == ErrMsg.NOT_LIST_VALUE

    def test_matrix_errors(self):
        """Проверяет функцию контроля данных в виде матрицы"""
        ds = DataShapeEnum.MATRIX
        assert ds.get_shape_errors([[]]) is None
        assert ds.get_shape_errors([["1"]]) is None
        assert ds.get_shape_errors([[1.0, 2.0], [1.0, 2.0]]) is None
        assert ds.get_shape_errors(None) == ErrMsg.NONE_VALUE
        assert ds.get_shape_errors(1) == ErrMsg.NOT_MATRIX_VALUE
        assert ds.get_shape_errors(
            [[1.0, 2.0], [1.0, 2.0], "row"]
        ) == ErrMsgTmpl.NOT_LIST_ROW.format(2)


if __name__ == "__main__":
    pytest.main(["-k", "TestDataShapeEnum"])
