from typing import Self

from pydantic import ConfigDict, model_validator

from src.internal.data_dimension.data_dimension import DataDimension
from src.internal.data_dimension.data_dimension_checker import DataDimensionChecker
from src.internal.data_dimension.data_shape_enum import DataShapeEnum
from src.internal.data_dimension.data_type_enum import DataTypeEnum
from src.internal.schemas.definition_schema import DefinitionSchema

ValueType = int | float | str | bool
ValueListType = list[ValueType]
OptionalValueListType = list[ValueType] | None
ValueMatrixType = list[OptionalValueListType]
OptionalValueMatrixType = ValueMatrixType | None


class DataDefinitionSchema(DefinitionSchema, DataDimension):
    """Класс представляет описание элемента входных или выходных данных для алгоритма"""

    model_config = ConfigDict(frozen=True)

    data_type: DataTypeEnum
    data_shape: DataShapeEnum
    default_value: ValueType | ValueListType | ValueMatrixType

    def __str__(self) -> str:
        """Возвращает строковое представление экземпляра класса"""
        return (
            f'DataDefinition: {self.name}, "{self.title}", '
            f"value: {self.default_value}"
        )

    @model_validator(mode="after")
    def validate_default_value(self) -> Self:
        """Проверяет, что значение по умолчанию соответствует указанным типу
        и размерности данных"""
        error = DataDimensionChecker.check_value(self, self.default_value)
        if error:
            raise ValueError(error)
        return self


if __name__ == "__main__":
    data = DataDefinitionSchema(
        name="data",
        title="Data",
        description="Input data",
        data_type=DataTypeEnum.INT,
        data_shape=DataShapeEnum.SCALAR,
        default_value=1,
    )
    print(data.model_dump)
