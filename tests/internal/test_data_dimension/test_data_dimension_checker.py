import pytest

from src.internal.data_dimension.data_dimension import DataDimension
from src.internal.data_dimension.data_dimension_checker import DataDimensionChecker
from src.internal.data_dimension.data_shape_enum import DataShapeEnum
from src.internal.data_dimension.data_type_enum import DataTypeEnum
from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.errors import ErrorMessageTemplateEnum as ErrMsgTmpl
from tests import (
    NOT_BOOL_CASES,
    NOT_INT_CASES,
    NOT_NUMBER_CASES,
    NOT_SCALAR_CASES,
    NOT_STRING_CASES,
    SCALAR_CASES,
)


class TestDataDimensionChecker:
    """Набор тестов для проверки класса DataDimensionChecker"""

    @pytest.mark.parametrize(
        "test_case",
        NOT_SCALAR_CASES,
        ids=[test_case.description for test_case in NOT_SCALAR_CASES],
    )
    def test_check_wrong_scalar_value(self, test_case):
        """Проверка метода check_value при передаче некорректного
        скалярного значения"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.SCALAR,
        )

        assert (
            DataDimensionChecker.check_value(data_dimension, test_case.value)
            == ErrMsg.NOT_SCALAR_VALUE
        )

    @pytest.mark.parametrize(
        "test_case",
        NOT_INT_CASES,
        ids=[test_case.description for test_case in NOT_INT_CASES],
    )
    def test_check_wrong_scalar_int_value(self, test_case):
        """Проверка метода check_value при передаче некорректного значения
        для типа int"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.SCALAR,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, test_case.value
        ) == ErrMsgTmpl.MISMATCH_VALUE_TYPE.format(DataTypeEnum.INT)

    @pytest.mark.parametrize(
        "test_case",
        NOT_NUMBER_CASES,
        ids=[test_case.description for test_case in NOT_NUMBER_CASES],
    )
    def test_check_wrong_scalar_float_value(self, test_case):
        """Проверка метода check_value при передаче некорректного значения
        для типа float"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.FLOAT,
            data_shape=DataShapeEnum.SCALAR,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, test_case.value
        ) == ErrMsgTmpl.MISMATCH_VALUE_TYPE.format(DataTypeEnum.FLOAT)

    @pytest.mark.parametrize(
        "test_case",
        NOT_STRING_CASES,
        ids=[test_case.description for test_case in NOT_STRING_CASES],
    )
    def test_check_wrong_scalar_str_value(self, test_case):
        """Проверка метода check_value при передаче некорректного значения
        для типа str"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.STRING,
            data_shape=DataShapeEnum.SCALAR,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, test_case.value
        ) == ErrMsgTmpl.MISMATCH_VALUE_TYPE.format(DataTypeEnum.STRING)

    @pytest.mark.parametrize(
        "test_case",
        NOT_BOOL_CASES,
        ids=[test_case.description for test_case in NOT_BOOL_CASES],
    )
    def test_check_wrong_scalar_bool_value(self, test_case):
        """Проверка метода check_value при передаче некорректного значения
        для типа bool"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.BOOL,
            data_shape=DataShapeEnum.SCALAR,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, test_case.value
        ) == ErrMsgTmpl.MISMATCH_VALUE_TYPE.format(DataTypeEnum.BOOL)

    @pytest.mark.parametrize(
        "test_case",
        SCALAR_CASES,
        ids=[test_case.description for test_case in SCALAR_CASES],
    )
    def test_check_wrong_list_value(self, test_case):
        """Проверка метода check_value при передаче некорректного значения
        списка"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.LIST,
        )
        assert (
            DataDimensionChecker.check_value(data_dimension, test_case.value)
            == ErrMsg.NOT_LIST_VALUE
        )

    def test_check_wrong_list_value_matrix(self):
        """Проверка метода check_value при передаче матрицы вместо списка"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.LIST,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, [[1]]
        ) == ErrMsgTmpl.MISMATCH_LIST_VALUE_TYPE.format(0, DataTypeEnum.INT)

    @pytest.mark.parametrize(
        "test_case",
        NOT_INT_CASES,
        ids=[test_case.description for test_case in NOT_INT_CASES],
    )
    def test_check_wrong_int_list_value(self, test_case):
        """Проверка метода check_value при передаче в списке некорректного значения"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.LIST,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, [1, test_case.value]
        ) == ErrMsgTmpl.MISMATCH_LIST_VALUE_TYPE.format(1, DataTypeEnum.INT)

    @pytest.mark.parametrize(
        "test_case",
        NOT_NUMBER_CASES,
        ids=[test_case.description for test_case in NOT_NUMBER_CASES],
    )
    def test_check_wrong_float_list_value(self, test_case):
        """Проверка метода check_value при передаче в списке некорректного значения"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.FLOAT,
            data_shape=DataShapeEnum.LIST,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, [1, test_case.value]
        ) == ErrMsgTmpl.MISMATCH_LIST_VALUE_TYPE.format(1, DataTypeEnum.FLOAT)

    @pytest.mark.parametrize(
        "test_case",
        NOT_BOOL_CASES,
        ids=[test_case.description for test_case in NOT_BOOL_CASES],
    )
    def test_check_wrong_bool_list_value(self, test_case):
        """Проверка метода check_value при передаче в списке
        некорректного значения"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.BOOL,
            data_shape=DataShapeEnum.LIST,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, [True, test_case.value]
        ) == ErrMsgTmpl.MISMATCH_LIST_VALUE_TYPE.format(1, DataTypeEnum.BOOL)

    @pytest.mark.parametrize(
        "test_case",
        NOT_STRING_CASES,
        ids=[test_case.description for test_case in NOT_STRING_CASES],
    )
    def test_check_wrong_str_list_value(self, test_case):
        """Проверка метода check_value при передаче в списке некорректного значения"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.STRING,
            data_shape=DataShapeEnum.LIST,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, ["string", test_case.value]
        ) == ErrMsgTmpl.MISMATCH_LIST_VALUE_TYPE.format(1, DataTypeEnum.STRING)

    @pytest.mark.parametrize(
        "test_case",
        SCALAR_CASES,
        ids=[test_case.description for test_case in SCALAR_CASES],
    )
    def test_check_wrong_matrix_value(self, test_case):
        """Проверка метода check_value при передаче некорректного значения списка"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.MATRIX,
        )
        assert (
            DataDimensionChecker.check_value(data_dimension, test_case.value)
            == ErrMsg.NOT_MATRIX_VALUE
        )

    def test_check_wrong_matrix_value_list(self):
        """Проверка метода check_value с передачей списка вместо матрицы"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.MATRIX,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, [1, 2]
        ) == ErrMsgTmpl.NOT_LIST_ROW.format(0)

    @pytest.mark.parametrize(
        "test_case",
        NOT_INT_CASES,
        ids=[test_case.description for test_case in NOT_INT_CASES],
    )
    def test_check_wrong_int_matrix_value(self, test_case):
        """Проверка метода check_value при передаче в матрице некорректного значения"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.MATRIX,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, [[1, test_case.value]]
        ) == ErrMsgTmpl.MISMATCH_MATRIX_VALUE_TYPE.format(1, 0, DataTypeEnum.INT)

    @pytest.mark.parametrize(
        "test_case",
        NOT_NUMBER_CASES,
        ids=[test_case.description for test_case in NOT_NUMBER_CASES],
    )
    def test_check_wrong_float_matrix_value(self, test_case):
        """Проверка метода check_value при передаче в матрице некорректного значения"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.FLOAT,
            data_shape=DataShapeEnum.MATRIX,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, [[1, test_case.value]]
        ) == ErrMsgTmpl.MISMATCH_MATRIX_VALUE_TYPE.format(1, 0, DataTypeEnum.FLOAT)

    @pytest.mark.parametrize(
        "test_case",
        NOT_BOOL_CASES,
        ids=[test_case.description for test_case in NOT_BOOL_CASES],
    )
    def test_check_wrong_bool_matrix_value(self, test_case):
        """Проверка метода check_value при передаче в матрице некорректного значения"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.BOOL,
            data_shape=DataShapeEnum.MATRIX,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, [[True, test_case.value]]
        ) == ErrMsgTmpl.MISMATCH_MATRIX_VALUE_TYPE.format(1, 0, DataTypeEnum.BOOL)

    @pytest.mark.parametrize(
        "test_case",
        NOT_STRING_CASES,
        ids=[test_case.description for test_case in NOT_STRING_CASES],
    )
    def test_check_wrong_str_matrix_value(self, test_case):
        """Проверка метода check_value при передаче в матрице некорректного значения"""
        data_dimension = DataDimension(
            data_type=DataTypeEnum.STRING,
            data_shape=DataShapeEnum.MATRIX,
        )
        assert DataDimensionChecker.check_value(
            data_dimension, [["string", test_case.value]]
        ) == ErrMsgTmpl.MISMATCH_MATRIX_VALUE_TYPE.format(1, 0, DataTypeEnum.STRING)


if __name__ == "__main__":
    pytest.main(["-k", "TestDataDimensionChecker"])
