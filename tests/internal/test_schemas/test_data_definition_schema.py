import pytest
from pydantic import ValidationError

from src.internal.data_dimension.data_shape_enum import DataShapeEnum
from src.internal.data_dimension.data_type_enum import DataTypeEnum
from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.errors import ErrorMessageTemplateEnum as ErrMsgTmpl
from src.internal.schemas.data_definition_schema import DataDefinitionSchema
from tests import (
    CHECK_ENUM_INVALID_CASES,
    DATA_SHAPE,
    DATA_TYPE,
    DESCRIPTION,
    NAME,
    NOT_BOOL_CASES,
    NOT_INT_CASES,
    NOT_NUMBER_CASES,
    NOT_SCALAR_CASES,
    NOT_STRING_CASES,
    SCALAR_CASES,
    TITLE,
    ErrorItemEnum,
)
from tests.internal.test_schemas.test_definition_schema import TestDefinitionSchema

DEFAULT_VALUE_CASES = [
    (DataShapeEnum.SCALAR, DataTypeEnum.INT, 1),
    (DataShapeEnum.SCALAR, DataTypeEnum.BOOL, True),
    (DataShapeEnum.SCALAR, DataTypeEnum.FLOAT, 1),
    (DataShapeEnum.SCALAR, DataTypeEnum.FLOAT, 1.1),
    (DataShapeEnum.SCALAR, DataTypeEnum.STRING, "string"),
    (DataShapeEnum.LIST, DataTypeEnum.INT, [1, 2]),
    (DataShapeEnum.LIST, DataTypeEnum.BOOL, [True, False]),
    (DataShapeEnum.LIST, DataTypeEnum.FLOAT, [1.1, 2.2]),
    (DataShapeEnum.LIST, DataTypeEnum.STRING, ["string", "string"]),
    (DataShapeEnum.MATRIX, DataTypeEnum.INT, [[1, 2]]),
    (DataShapeEnum.MATRIX, DataTypeEnum.BOOL, [[True, False]]),
    (DataShapeEnum.MATRIX, DataTypeEnum.FLOAT, [[1.1, 2.2]]),
    (DataShapeEnum.MATRIX, DataTypeEnum.STRING, [["string", "string"]]),
]


class TestDataDefinitionSchema(TestDefinitionSchema):
    """Набор тестов для проверки класса DataDefinitionModel"""

    @pytest.mark.parametrize(
        "data_shape, data_type, default_value",
        DEFAULT_VALUE_CASES,
    )
    def test_valid_entity(self, data_shape, data_type, default_value):
        """Проверка создания объекта"""
        data_definition = DataDefinitionSchema(
            name=NAME,
            title=TITLE,
            description=DESCRIPTION,
            data_type=data_type,
            data_shape=data_shape,
            default_value=default_value,
        )
        assert data_definition.name == NAME
        assert data_definition.title == TITLE
        assert data_definition.description == DESCRIPTION
        assert data_definition.data_type == data_type
        assert data_definition.data_shape == data_shape
        assert data_definition.default_value == default_value

    def test_immutable_entity(self):
        """Проверка на неизменяемость объекта"""
        data_definition = DataDefinitionSchema(
            name=NAME,
            title=TITLE,
            description=DESCRIPTION,
            data_type=DataTypeEnum.INT,
            data_shape=DataShapeEnum.SCALAR,
            default_value=1,
        )
        with pytest.raises(ValueError):
            data_definition.name = "NewName"
        with pytest.raises(ValueError):
            data_definition.title = "NewTitle"
        with pytest.raises(ValueError):
            data_definition.description = "NewDescription"
        with pytest.raises(ValueError):
            data_definition.data_type = DataTypeEnum.BOOL
        with pytest.raises(ValueError):
            data_definition.data_shape = DataShapeEnum.LIST
        with pytest.raises(ValueError):
            data_definition.default_value = 2

    @pytest.mark.parametrize(
        "test_case",
        CHECK_ENUM_INVALID_CASES,
        ids=[test_case.description for test_case in CHECK_ENUM_INVALID_CASES],
    )
    def test_wrong_data_type(self, test_case):
        """Проверка создания объекта с неверным значением data_type"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=test_case.value,
                data_shape=DataShapeEnum.SCALAR,
                default_value=1,
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][ErrorItemEnum.LOC] == (DATA_TYPE,)

    @pytest.mark.parametrize(
        "test_case",
        CHECK_ENUM_INVALID_CASES,
        ids=[test_case.description for test_case in CHECK_ENUM_INVALID_CASES],
    )
    def test_wrong_data_shape(self, test_case):
        """Проверка создания объекта с неверным значением data_shape"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.INT,
                data_shape=test_case.value,
                default_value=1,
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][ErrorItemEnum.LOC] == (DATA_SHAPE,)

    @pytest.mark.parametrize(
        "test_case",
        NOT_SCALAR_CASES,
        ids=[test_case.description for test_case in NOT_SCALAR_CASES],
    )
    def test_wrong_scalar_value(self, test_case):
        """Проверка создания объекта с неверным скалярным значением"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.INT,
                data_shape=DataShapeEnum.SCALAR,
                default_value=test_case.value,
            )
        assert len(ctx.value.errors()) == 1
        assert (
            ctx.value.errors()[0][ErrorItemEnum.MSG]
            == "Value error, " + ErrMsg.NOT_SCALAR_VALUE
        )

    @pytest.mark.parametrize(
        "test_case",
        NOT_INT_CASES,
        ids=[test_case.description for test_case in NOT_INT_CASES],
    )
    def test_wrong_scalar_int_value(self, test_case):
        """Проверка создания объекта с неверным значением значением для типа int"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.INT,
                data_shape=DataShapeEnum.SCALAR,
                default_value=test_case.value,
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_VALUE_TYPE.format(DataTypeEnum.INT)

    @pytest.mark.parametrize(
        "test_case",
        NOT_NUMBER_CASES,
        ids=[test_case.description for test_case in NOT_NUMBER_CASES],
    )
    def test_wrong_scalar_float_value(self, test_case):
        """Проверка создания объекта с неверным значением значением для типа float"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.FLOAT,
                data_shape=DataShapeEnum.SCALAR,
                default_value=test_case.value,
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_VALUE_TYPE.format(DataTypeEnum.FLOAT)

    @pytest.mark.parametrize(
        "test_case",
        NOT_STRING_CASES,
        ids=[test_case.description for test_case in NOT_STRING_CASES],
    )
    def test_wrong_scalar_str_value(self, test_case):
        """Проверка создания объекта с неверным значением значением для типа str"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.STRING,
                data_shape=DataShapeEnum.SCALAR,
                default_value=test_case.value,
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_VALUE_TYPE.format(
            DataTypeEnum.STRING
        )

    @pytest.mark.parametrize(
        "test_case",
        NOT_BOOL_CASES,
        ids=[test_case.description for test_case in NOT_BOOL_CASES],
    )
    def test_wrong_scalar_bool_value(self, test_case):
        """Проверка создания объекта с неверным значением для типа bool"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.BOOL,
                data_shape=DataShapeEnum.SCALAR,
                default_value=test_case.value,
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_VALUE_TYPE.format(DataTypeEnum.BOOL)

    @pytest.mark.parametrize(
        "test_case",
        SCALAR_CASES,
        ids=[test_case.description for test_case in SCALAR_CASES],
    )
    def test_wrong_list_value(self, test_case):
        """Проверка создания объекта с неверным значением списка"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.INT,
                data_shape=DataShapeEnum.LIST,
                default_value=test_case.value,
            )
        assert len(ctx.value.errors()) == 1
        assert (
            ctx.value.errors()[0][ErrorItemEnum.MSG]
            == "Value error, " + ErrMsg.NOT_LIST_VALUE
        )

    def test_wrong_list_value_matrix(self):
        """Проверка создания объекта с передачей матрицы вместо списка"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.INT,
                data_shape=DataShapeEnum.LIST,
                default_value=[[1]],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_LIST_VALUE_TYPE.format(
            0, DataTypeEnum.INT
        )

    @pytest.mark.parametrize(
        "test_case",
        NOT_INT_CASES,
        ids=[test_case.description for test_case in NOT_INT_CASES],
    )
    def test_wrong_int_list_value(self, test_case):
        """Проверка создания объекта с передачей в списке некорректного значения"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.INT,
                data_shape=DataShapeEnum.LIST,
                default_value=[1, test_case.value],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_LIST_VALUE_TYPE.format(
            1, DataTypeEnum.INT
        )

    @pytest.mark.parametrize(
        "test_case",
        NOT_NUMBER_CASES,
        ids=[test_case.description for test_case in NOT_NUMBER_CASES],
    )
    def test_wrong_float_list_value(self, test_case):
        """Проверка создания объекта с передачей в списке некорректного значения"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.FLOAT,
                data_shape=DataShapeEnum.LIST,
                default_value=[1, test_case.value],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_LIST_VALUE_TYPE.format(
            1, DataTypeEnum.FLOAT
        )

    @pytest.mark.parametrize(
        "test_case",
        NOT_BOOL_CASES,
        ids=[test_case.description for test_case in NOT_BOOL_CASES],
    )
    def test_wrong_bool_list_value(self, test_case):
        """Проверка создания объекта с передачей в списке некорректного значения"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.BOOL,
                data_shape=DataShapeEnum.LIST,
                default_value=[True, test_case.value],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_LIST_VALUE_TYPE.format(
            1, DataTypeEnum.BOOL
        )

    @pytest.mark.parametrize(
        "test_case",
        NOT_STRING_CASES,
        ids=[test_case.description for test_case in NOT_STRING_CASES],
    )
    def test_wrong_str_list_value(self, test_case):
        """Проверка создания объекта с передачей в списке некорректного значения"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.STRING,
                data_shape=DataShapeEnum.LIST,
                default_value=["string", test_case.value],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_LIST_VALUE_TYPE.format(
            1, DataTypeEnum.STRING
        )

    @pytest.mark.parametrize(
        "test_case",
        SCALAR_CASES,
        ids=[test_case.description for test_case in SCALAR_CASES],
    )
    def test_wrong_matrix_value(self, test_case):
        """Проверка создания объекта с неверным значением матрицы"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.INT,
                data_shape=DataShapeEnum.MATRIX,
                default_value=test_case.value,
            )
        assert len(ctx.value.errors()) == 1
        assert (
            ctx.value.errors()[0][ErrorItemEnum.MSG]
            == "Value error, " + ErrMsg.NOT_MATRIX_VALUE
        )

    def test_wrong_matrix_value_list(self):
        """Проверка создания объекта с передачей списка вместо матрицы"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.INT,
                data_shape=DataShapeEnum.MATRIX,
                default_value=[1, 2],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.NOT_LIST_ROW.format(0)

    @pytest.mark.parametrize(
        "test_case",
        NOT_INT_CASES,
        ids=[test_case.description for test_case in NOT_INT_CASES],
    )
    def test_wrong_int_matrix_value(self, test_case):
        """Проверка создания объекта с передачей в матрице некорректного значения"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.INT,
                data_shape=DataShapeEnum.MATRIX,
                default_value=[[1, test_case.value]],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_MATRIX_VALUE_TYPE.format(
            1, 0, DataTypeEnum.INT
        )

    @pytest.mark.parametrize(
        "test_case",
        NOT_NUMBER_CASES,
        ids=[test_case.description for test_case in NOT_NUMBER_CASES],
    )
    def test_wrong_float_matrix_value(self, test_case):
        """Проверка создания объекта с передачей в матрице некорректного значения"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.FLOAT,
                data_shape=DataShapeEnum.MATRIX,
                default_value=[[1, test_case.value]],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_MATRIX_VALUE_TYPE.format(
            1, 0, DataTypeEnum.FLOAT
        )

    @pytest.mark.parametrize(
        "test_case",
        NOT_BOOL_CASES,
        ids=[test_case.description for test_case in NOT_BOOL_CASES],
    )
    def test_wrong_bool_matrix_value(self, test_case):
        """Проверка создания объекта с передачей в матрице некорректного значения"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.BOOL,
                data_shape=DataShapeEnum.MATRIX,
                default_value=[[True, test_case.value]],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_MATRIX_VALUE_TYPE.format(
            1, 0, DataTypeEnum.BOOL
        )

    @pytest.mark.parametrize(
        "test_case",
        NOT_STRING_CASES,
        ids=[test_case.description for test_case in NOT_STRING_CASES],
    )
    def test_wrong_str_matrix_value(self, test_case):
        """Проверка создания объекта с передачей в матрице некорректного значения"""
        with pytest.raises(ValidationError) as ctx:
            DataDefinitionSchema(
                name=NAME,
                title=TITLE,
                description=DESCRIPTION,
                data_type=DataTypeEnum.STRING,
                data_shape=DataShapeEnum.MATRIX,
                default_value=[["string", test_case.value]],
            )
        assert len(ctx.value.errors()) == 1
        assert ctx.value.errors()[0][
            ErrorItemEnum.MSG
        ] == "Value error, " + ErrMsgTmpl.MISMATCH_MATRIX_VALUE_TYPE.format(
            1, 0, DataTypeEnum.STRING
        )


if __name__ == "__main__":
    pytest.main(["-k", "TestDataDefinitionSchema"])
