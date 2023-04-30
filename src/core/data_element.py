from typing import Any, Optional

from strenum import UppercaseStrEnum
from enum import auto


NON_STRING_PARAM_TEMPL = 'The "{0}" parameter is not a string'
EMPTY_STRING_PARAM_TEMPL = 'The "{0}" parameter is empty'
NOT_DATA_TYPE_MSG = 'The data_type parameter is not a DataType instance'
NOT_DATA_SHAPE_MSG = 'The data_shape parameter is not a DataShape instance'
NONE_VALUE_MSG = 'The value is None'
NOT_SCALAR_VALUE_MSG = 'The value is not a scalar'
NOT_MATRIX_VALUE_MSG = 'The value is not a matrix'
NOT_LIST_VALUE_MSG = 'The value is not a list'
NOT_LIST_ROW_TEMPL = 'The type of {0} row in the matrix is not a list'
MISMATCH_VALUE_TYPE_TEMPL = 'The type of value is not {0}'
MISMATCH_LIST_VALUE_TYPE_TEMPL = 'The type at {0} position in the list ' \
                                 'is not {1}'
MISMATCH_MATRIX_VALUE_TYPE_TEMPL = 'The type at {0} position in {1} row ' \
                                   'in the matrix is not {2}'


class DataType(UppercaseStrEnum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()

    @property
    def type(self) -> type:
        return DataType.__types_dict()[self]

    @staticmethod
    def types() -> list[type]:
        return list(DataType.__types_dict().values())

    def __str__(self) -> str:
        return self.name.lower()

    @staticmethod
    def __types_dict():
        return {DataType.INT: int, DataType.FLOAT: float, DataType.STRING: str,
                DataType.BOOL: bool}


class DataShape(UppercaseStrEnum):
    SCALAR = auto()
    LIST = auto()
    MATRIX = auto()

    def get_shape_errors(self, value_to_check: Any) -> Optional[str]:
        if value_to_check is None:
            return NONE_VALUE_MSG
        if self.value == self.SCALAR and type(value_to_check) \
                not in DataType.types():
            return NOT_SCALAR_VALUE_MSG
        if self.value == self.LIST and type(value_to_check) != list:
            return NOT_LIST_VALUE_MSG
        if self.value == self.MATRIX:
            if type(value_to_check) != list:
                return NOT_MATRIX_VALUE_MSG
            if len(value_to_check) == 0:
                return NOT_MATRIX_VALUE_MSG
            for row_idx, row in enumerate(value_to_check):
                if type(row) != list:
                    return NOT_LIST_ROW_TEMPL.format(row_idx)
        return None

    def __str__(self) -> str:
        return self.name.lower()


class DataElement(object):
    def __init__(self, name: str, title: str, description: str,
                 data_type: DataType, data_shape: DataShape,
                 default_value: Any):
        param_errors = DataElement.__check_params(name, title, description,
                                                  data_type, data_shape)
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
        return f'DataElement: {self.__name}, "{self.__title}", ' \
               f'value: {self.__default_value}'

    @property
    def name(self) -> str:
        return self.__name

    @property
    def title(self) -> str:
        return self.__title

    @property
    def description(self) -> str:
        return self.__description

    @property
    def data_type(self) -> DataType:
        return self.__data_type

    @property
    def data_shape(self) -> DataShape:
        return self.__data_shape

    @property
    def default_value(self) -> Any:
        return self.__default_value

    def get_check_value_errors(self, value: Any) -> Optional[str]:
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
        if type(value) != self.__data_type.type:
            return MISMATCH_VALUE_TYPE_TEMPL.format(self.__data_type)

    def __check_list_value(self, value: Any) -> Optional[str]:
        for idx, item in enumerate(value):
            if item is not None and type(item) != self.__data_type.type:
                return MISMATCH_LIST_VALUE_TYPE_TEMPL.format(idx,
                                                             self.__data_type)

    def __check_matrix_value(self, value: Any) -> Optional[str]:
        for row_idx, row in enumerate(value):
            for item_idx, item in enumerate(row):
                if item is not None and type(item) != self.__data_type.type:
                    return MISMATCH_MATRIX_VALUE_TYPE_TEMPL.format(
                        item_idx, row_idx, self.__data_type)

    @staticmethod
    def __check_params(name: str, title: str, description: str,
                       data_type: DataType,
                       data_shape: DataShape) -> Optional[str]:
        str_params = [['name', name], ['title', title],
                      ['description', description]]
        for name, value in str_params:
            if type(value) != str:
                return NON_STRING_PARAM_TEMPL.format(name)
            if not value:
                return EMPTY_STRING_PARAM_TEMPL.format(name)
        if not isinstance(data_type, DataType):
            return NOT_DATA_TYPE_MSG
        if not isinstance(data_shape, DataShape):
            return NOT_DATA_SHAPE_MSG
        return None
