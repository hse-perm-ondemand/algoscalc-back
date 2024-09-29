from enum import auto

from strenum import UppercaseStrEnum


class DataTypeEnum(UppercaseStrEnum):
    """Перечисление представляет допустимые типы данных для входных и выходных данных
    алгоритмов. Элементы перечисления INT, FLOAT, STRING, BOOL соответствуют типам
    данных int, float, str, bool.

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
        return DataTypeEnum.__types_dict()[self]

    @staticmethod
    def types() -> list[type]:
        """Возвращает список допустимых типов данных.

        :return: список допустимых типов данных.
        :rtype: list[type]
        """
        return list(DataTypeEnum.__types_dict().values())

    def __str__(self) -> str:
        """Возвращает строковое представление экземпляра класса."""
        return self.name.lower()

    @staticmethod
    def __types_dict():
        """Возвращает словарь соответствия типам данных."""
        return {
            DataTypeEnum.INT: int,
            DataTypeEnum.FLOAT: float,
            DataTypeEnum.STRING: str,
            DataTypeEnum.BOOL: bool,
        }
