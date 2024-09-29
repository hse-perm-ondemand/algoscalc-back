from typing import Any

from src.internal.data_dimension.data_dimension import DataDimension
from src.internal.data_dimension.data_shape_enum import DataShapeEnum
from src.internal.data_dimension.data_type_enum import DataTypeEnum
from src.internal.errors import ErrorMessageTemplateEnum as ErrMsgTmpl


class DataDimensionChecker:
    """Класс реализует проверку значений на соответствие типу и размерности данных."""

    @classmethod
    def check_value(cls, data_dimension: DataDimension, value: Any) -> str | None:
        """Проверяет соответствие проверяемого значения типу данных
        и размерности элемента данных.

        :param data_dimension: описание элемента данных;
        :param value: значение для проверки;
        :type value: Any
        :return: текст сообщения об ошибке проверки типа и размерности.
        :rtype: str or None
        """
        shape_errors = data_dimension.data_shape.get_shape_errors(value)
        if shape_errors is not None:
            return shape_errors
        if data_dimension.data_shape == DataShapeEnum.SCALAR:
            return cls.__check_scalar_value(data_dimension, value)
        if data_dimension.data_shape == DataShapeEnum.LIST:
            return cls.__check_list_value(data_dimension, value)
        if data_dimension.data_shape == DataShapeEnum.MATRIX:
            return cls.__check_matrix_value(data_dimension, value)
        return None

    @classmethod
    def __check_scalar_value(
        cls, data_dimension: DataDimension, value: Any
    ) -> str | None:
        """Проверяет тип данных для скалярного значения."""
        err_msg = ErrMsgTmpl.MISMATCH_VALUE_TYPE.format(data_dimension.data_type)
        if data_dimension.data_type.type == float:
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                return err_msg
        elif data_dimension.data_type.type == int:
            if not isinstance(value, int) or isinstance(value, bool):
                return err_msg
        elif not isinstance(value, data_dimension.data_type.type):
            return err_msg

    @classmethod
    def __check_list_value(
        cls, data_dimension: DataDimension, value: Any
    ) -> str | None:
        """Проверяет тип данных для элементов списка."""
        for idx, item in enumerate(value):
            if item is not None and cls.__check_scalar_value(data_dimension, item):
                return ErrMsgTmpl.MISMATCH_LIST_VALUE_TYPE.format(
                    idx, data_dimension.data_type
                )

    @classmethod
    def __check_matrix_value(
        cls, data_dimension: DataDimension, value: Any
    ) -> str | None:
        """Проверяет тип данных для элементов матрицы."""
        for row_idx, row in enumerate(value):
            for item_idx, item in enumerate(row):
                if item is not None and cls.__check_scalar_value(data_dimension, item):
                    return ErrMsgTmpl.MISMATCH_MATRIX_VALUE_TYPE.format(
                        item_idx, row_idx, data_dimension.data_type
                    )


if __name__ == "__main__":
    data_dimension = DataDimension(
        data_type=DataTypeEnum.INT, data_shape=DataShapeEnum.SCALAR
    )
    print(DataDimensionChecker.check_value(data_dimension, "string"))
