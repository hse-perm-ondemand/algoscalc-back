from enum import auto
from typing import Any, Optional

from strenum import UppercaseStrEnum

from src.core import (
    EMPTY_STRING_PARAM_TEMPL,
    MISMATCH_LIST_VALUE_TYPE_TEMPL,
    MISMATCH_MATRIX_VALUE_TYPE_TEMPL,
    MISMATCH_VALUE_TYPE_TEMPL,
    NON_STRING_PARAM_TEMPL,
    NONE_VALUE_MSG,
    NOT_DATA_SHAPE_MSG,
    NOT_DATA_TYPE_MSG,
    NOT_LIST_ROW_TEMPL,
    NOT_LIST_VALUE_MSG,
    NOT_MATRIX_VALUE_MSG,
    NOT_SCALAR_VALUE_MSG,
)


class DataType(UppercaseStrEnum):
    """Класс является перечислением, представляет допустимые типы данных
    для входных и выходных данных. Возможными значениями класса являются
    INT, FLOAT, STRING, BOOL, соответствующие типам данных
    int, float, str, bool.

    """

    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()

    @property
    def type(self) -> type:
        """Возвращает соответствующий тип данных.

        :return: тип данных.
        :rtype: type
        """
        return DataType.__types_dict()[self]

    @staticmethod
    def types() -> list[type]:
        """Возвращает список допустимых типов данных.

        :return: список допустимых типов данных.
        :rtype: list[type]
        """
        return list(DataType.__types_dict().values())

    def __str__(self) -> str:
        """Возвращает строковое представление экземпляра класса."""
        return self.name.lower()

    @staticmethod
    def __types_dict():
        """Возвращает словарь соответствия типам данных."""
        return {
            DataType.INT: int,
            DataType.FLOAT: float,
            DataType.STRING: str,
            DataType.BOOL: bool,
        }


class DataShape(UppercaseStrEnum):
    """Класс DataShape является перечислением, представляет допустимые
    размерности для входных и выходных данных. Возможными значениями
    класса являются SCALAR, LIST, MATRIX, соответствующие скалярному значению,
    списку скалярных значений и двумерную матрицу соответственно.

    """

    SCALAR = auto()
    LIST = auto()
    MATRIX = auto()

    def get_shape_errors(self, value_to_check: Any) -> Optional[str]:
        """Проверяет соответствие проверяемого значения размерности.

        :param value_to_check: значение для проверки;
        :type value_to_check: Any
        :return: текст сообщения об ошибке проверки размерности.
        :rtype: str or None
        """
        if value_to_check is None:
            return NONE_VALUE_MSG
        if self.value == self.SCALAR and not isinstance(
            value_to_check, tuple(DataType.types())
        ):
            return NOT_SCALAR_VALUE_MSG
        if self.value == self.LIST and not isinstance(value_to_check, list):
            return NOT_LIST_VALUE_MSG
        if self.value == self.MATRIX:
            if not isinstance(value_to_check, list):
                return NOT_MATRIX_VALUE_MSG
            if len(value_to_check) == 0:
                return NOT_MATRIX_VALUE_MSG
            for row_idx, row in enumerate(value_to_check):
                if not isinstance(row, list):
                    return NOT_LIST_ROW_TEMPL.format(row_idx)
        return None

    def __str__(self) -> str:
        return self.name.lower()


class DataElement(object):
    """Класс представляет элемент входных или выходных данных для алгоритма."""

    def __init__(
        self,
        name: str,
        title: str,
        description: str,
        data_type: DataType,
        data_shape: DataShape,
        default_value: Any,
    ):
        """Конструктор класса

        :param name: уникальное имя элемента входных/выходных данных;
        :type name: str
        :param title: название элемента входных/выходных данных;
        :type title: str
        :param description: описание элемента входных/выходных данных;
        :type description: str
        :param data_type: тип данных;
        :type data_type: DataType
        :param data_shape: размерность данных;
        :type data_shape: DataShape
        :param default_value: значение по умолчанию.
        :type default_value: Any
        :raises ValueError: при несоответствии типов данных для параметров.
        """
        param_errors = DataElement.__check_params(
            name, title, description, data_type, data_shape
        )
        if param_errors is not None:
            raise ValueError(param_errors)
        self.__name: str = name
        self.__title: str = title
        self.__description: str = description
        self.__data_type: DataType = data_type
        self.__data_shape: DataShape = data_shape
        default_value_errors = self.get_check_value_errors(default_value)
        if default_value_errors is not None:
            raise ValueError(default_value_errors)
        self.__default_value: Any = default_value

    def __str__(self) -> str:
        """Возвращает строковое представление экземпляра класса."""
        return (
            f'DataElement: {self.__name}, "{self.__title}", '
            f"value: {self.__default_value}"
        )

    @property
    def name(self) -> str:
        """Возвращает уникальное имя элемента.

        :return: уникальное имя элемента.
        :rtype: str
        """
        return self.__name

    @property
    def title(self) -> str:
        """Возвращает название элемента.

        :return: название элемента.
        :rtype: str
        """
        return self.__title

    @property
    def description(self) -> str:
        """Возвращает описание элемента.

        :return: описание элемента.
        :rtype: str
        """
        return self.__description

    @property
    def data_type(self) -> DataType:
        """Возвращает тип данных элемента.

        :return: тип данных элемента.
        :rtype: DataType
        """
        return self.__data_type

    @property
    def data_shape(self) -> DataShape:
        """Возвращает размерность данных элемента.

        :return: размерность данных элемента.
        :rtype: DataShape
        """
        return self.__data_shape

    @property
    def default_value(self) -> Any:
        """Возвращает значение по умолчанию элемента.

        :return: значение по умолчанию элемента.
        :rtype: Any
        """
        return self.__default_value

    def get_check_value_errors(self, value: Any) -> Optional[str]:
        """Проверяет соответствие проверяемого значения типу данных
        и размерности.

        :param value: значение для проверки;
        :type value: Any
        :return: текст сообщения об ошибке проверки типа и размерности.
        :rtype: str or None
        """
        shape_errors = self.data_shape.get_shape_errors(value)
        if shape_errors is not None:
            return shape_errors
        if self.data_shape == DataShape.SCALAR:
            return self.__check_scalar_value(value)
        if self.data_shape == DataShape.LIST:
            return self.__check_list_value(value)
        if self.data_shape == DataShape.MATRIX:
            return self.__check_matrix_value(value)
        return None

    def __check_scalar_value(self, value: Any) -> Optional[str]:
        """Проверяет тип данных для скалярного значения."""
        if self.__data_type.type == float:
            if type(value) not in [int, float]:
                return MISMATCH_VALUE_TYPE_TEMPL.format(self.__data_type)
        elif not isinstance(value, self.__data_type.type):
            return MISMATCH_VALUE_TYPE_TEMPL.format(self.__data_type)

    def __check_list_value(self, value: Any) -> Optional[str]:
        """Проверяет тип данных для элементов списка."""
        for idx, item in enumerate(value):
            if item is not None and self.__data_type.type == float:
                if type(item) not in [int, float]:
                    return MISMATCH_LIST_VALUE_TYPE_TEMPL.format(idx, self.__data_type)
            elif item is not None and not isinstance(item, self.__data_type.type):
                return MISMATCH_LIST_VALUE_TYPE_TEMPL.format(idx, self.__data_type)

    def __check_matrix_value(self, value: Any) -> Optional[str]:
        """Проверяет тип данных для элементов матрицы."""
        for row_idx, row in enumerate(value):
            for item_idx, item in enumerate(row):
                if item is not None and self.__data_type.type == float:
                    if type(item) not in [int, float]:
                        return MISMATCH_MATRIX_VALUE_TYPE_TEMPL.format(
                            item_idx, row_idx, self.__data_type
                        )
                elif item is not None and not isinstance(item, self.__data_type.type):
                    return MISMATCH_MATRIX_VALUE_TYPE_TEMPL.format(
                        item_idx, row_idx, self.__data_type
                    )

    @staticmethod
    def __check_params(
        name: str,
        title: str,
        description: str,
        data_type: DataType,
        data_shape: DataShape,
    ) -> Optional[str]:
        """Проверяет параметры для конструктора класса. Возвращает сообщение
        об ошибке"""
        str_params = [["name", name], ["title", title], ["description", description]]
        for name, value in str_params:
            if not isinstance(value, str):
                return NON_STRING_PARAM_TEMPL.format(name)
            if not value:
                return EMPTY_STRING_PARAM_TEMPL.format(name)
        if not isinstance(data_type, DataType):
            return NOT_DATA_TYPE_MSG
        if not isinstance(data_shape, DataShape):
            return NOT_DATA_SHAPE_MSG
        return None
