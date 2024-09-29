from src.internal.data_dimension.data_shape_enum import DataShapeEnum
from src.internal.data_dimension.data_type_enum import DataTypeEnum


class DataDimension:
    """Класс для описания типа и размерности данных"""

    data_type: DataTypeEnum
    data_shape: DataShapeEnum

    def __init__(self, data_type: DataTypeEnum, data_shape: DataShapeEnum):
        self.data_type = data_type
        self.data_shape = data_shape
