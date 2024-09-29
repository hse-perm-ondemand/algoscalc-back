from enum import auto
from typing import Any

from strenum import UppercaseStrEnum

from src.internal.data_dimension.data_type_enum import DataTypeEnum
from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.errors import ErrorMessageTemplateEnum as ErrMsgTmpl


class DataShapeEnum(UppercaseStrEnum):
    """Перечисление допустимых размерностей для входных и выходных данных алгоритмов.
    Значения SCALAR, LIST, MATRIX соответствуют скалярному значению, списку скалярных
    значений и двумерную матрицу соответственно.

    """

    SCALAR = auto()
    LIST = auto()
    MATRIX = auto()

    def get_shape_errors(self, value_to_check: Any) -> str | None:
        """Проверяет соответствие проверяемого значения размерности.

        :param value_to_check: значение для проверки;
        :type value_to_check: Any
        :return: текст сообщения об ошибке проверки размерности.
        :rtype: str or None
        """
        if value_to_check is None:
            return ErrMsg.NONE_VALUE
        if self.value == self.SCALAR and not isinstance(
            value_to_check, tuple(DataTypeEnum.types())
        ):
            return ErrMsg.NOT_SCALAR_VALUE
        if self.value == self.LIST and not isinstance(value_to_check, list):
            return ErrMsg.NOT_LIST_VALUE
        if self.value == self.MATRIX:
            if not isinstance(value_to_check, list):
                return ErrMsg.NOT_MATRIX_VALUE
            if len(value_to_check) == 0:
                return ErrMsg.NOT_MATRIX_VALUE
            for row_idx, row in enumerate(value_to_check):
                if not isinstance(row, list):
                    return ErrMsgTmpl.NOT_LIST_ROW.format(row_idx)
        return None

    def __str__(self) -> str:
        return self.name.lower()
