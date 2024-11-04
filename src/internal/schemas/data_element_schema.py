from pydantic import BaseModel, Field, RootModel

from src.internal.schemas.data_definition_schema import (
    OptionalValueListType,
    OptionalValueMatrixType,
    ValueType,
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


class DataElementsSchema(RootModel):
    root: list[DataElementSchema]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


if __name__ == "__main__":
    data = DataElementSchema(
        name="data",
        value=1,
    )
    print(data.model_dump)
