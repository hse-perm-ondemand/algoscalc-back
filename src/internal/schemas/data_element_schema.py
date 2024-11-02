from pydantic import BaseModel, Field

from src.internal.schemas.data_definition_schema import (
    ValueType,
    OptionalValueMatrixType,
    OptionalValueListType,
)


class DataElementSchema(BaseModel):
    """Класс представляет фактическое значение элемента входных/выходных данных.

    :param name: уникальное имя элемента входных/выходных данных;
    :type name: str
    :param value: фактическое значение.
    :type value: int, float, str, bool либо список или двумерная
        матрица с элементами указанных типов.
    """

    name: str
    value: ValueType | OptionalValueListType | OptionalValueMatrixType = Field(
        ..., union_mode="smart"
    )

    def __str__(self) -> str:
        """Возвращает строковое представление экземпляра класса"""
        return f"DataElement: {self.name}, value: {self.value}"


if __name__ == "__main__":
    data = DataElementSchema(
        name="data",
        value=1,
    )
    print(data.model_dump)
