from typing import Any, Union, Optional

from strenum import UppercaseStrEnum
from enum import auto


class DataType(UppercaseStrEnum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()

    @property
    def type(self):
        return DataType.__types_dict()[self]

    @staticmethod
    def types():
        return list(DataType.__types_dict().values())

    def __str__(self):
        return self.name.lower()

    @staticmethod
    def __types_dict():
        return {DataType.INT: int, DataType.FLOAT: float, DataType.STRING: str,
                DataType.BOOL: bool}


class DataShape(UppercaseStrEnum):
    SCALAR = auto()
    LIST = auto()
    MATRIX = auto()

    def get_shape_errors(self, value_to_check: Any) -> Union[str, None]:
        if value_to_check is None:
            return 'The value is None!'
        if self.value == self.SCALAR and type(value_to_check) \
                not in DataType.types():
            return 'The value is not a scalar!'
        if self.value == self.LIST and type(value_to_check) != list:
            return 'The value is not a list!'
        if self.value == self.MATRIX:
            if type(value_to_check) != list:
                return 'The value is not a matrix!'
            if len(value_to_check) == 0:
                return 'The value is not a matrix!'
            for row_idx, row in enumerate(value_to_check):
                if type(row) != list:
                    return f'The type of {row_idx} row in the matrix ' \
                           f'is not a list'
        return None


class DataElement(object):
    def __init__(self, name: str, title: str, description: str,
                 data_type: DataType, data_shape: DataShape,
                 default_value: Any):
        param_errors = DataElement.__check_params(name, title, description,
                                                  data_type, data_shape)
        if param_errors is not None:
            raise ValueError(param_errors)
        self.__name = name
        self.__title = title
        self.__description = description
        self.__data_type = data_type
        self.__data_shape = data_shape
        default_value_errors = self.get_check_value_errors(default_value)
        if default_value_errors is not None:
            raise ValueError(default_value_errors)
        self.__default_value = default_value

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

    def to_dict(self) -> dict[str, Any]:
        return {
            'name': self.__name,
            'title': self.__title,
            'description': self.__description,
            'data_type': str(self.__data_type),
            'data_shape': str(self.__data_shape),
            'default_value': self.__default_value
        }

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
            return 'The type of value is not ' \
                   f'{self.__data_type}!'

    def __check_list_value(self, value: Any) -> Optional[str]:
        for idx, item in enumerate(value):
            if type(item) != self.__data_type.type:
                return f'The type at {idx} position in the list is not ' \
                       f'{self.__data_type}!'

    def __check_matrix_value(self, value: Any) -> Optional[str]:
        for row_idx, row in enumerate(value):
            for item_idx, item in enumerate(row):
                if type(item) != self.__data_type.type:
                    return f'The type at {item_idx} position ' \
                           f'in {row_idx} row in the matrix is not ' \
                           f'{self.__data_type}!'

    @staticmethod
    def __check_params(name: str, title: str, description: str,
                       data_type: DataType,
                       data_shape: DataShape) -> Optional[str]:
        if type(name) != str:
            return 'The name parameter is not a string'
        if not name:
            return 'The name parameter is empty'
        if type(title) != str:
            return 'The title parameter is not a string'
        if not title:
            return 'The title parameter is empty'
        if type(description) != str:
            return 'The description parameter is not a string'
        if not description:
            return 'The description parameter is empty'
        if not isinstance(data_type, DataType):
            return 'The data_type parameter is not a DataType instance'
        if not isinstance(data_shape, DataShape):
            return 'The data_shape parameter is not a DataShape instance'
        return None


if __name__ == '__main__':
    elem = DataElement('test', 'test data', 'some descr', DataType.INT,
                       DataShape.SCALAR, 0)
    print(elem.name)
    print(DataType.INT)
