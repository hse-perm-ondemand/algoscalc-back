import pytest

from src.internal.data_dimension import DataTypeEnum


class TestDataTypeEnum:
    """Набор тестов для проверки класса DataTypeEnum"""

    def test_types(self):
        """Проверяет набор допустимых типов данных"""
        assert [int, float, str, bool] == DataTypeEnum.types()

    def test_int(self):
        """Проверяет тип int"""
        dt = DataTypeEnum.INT
        assert dt.name == "INT"
        assert dt.value == "INT"
        assert str(dt) == "int"
        assert dt == DataTypeEnum["INT"]
        assert dt.type == int

    def test_float(self):
        """Проверяет тип float"""
        dt = DataTypeEnum.FLOAT
        assert dt.name == "FLOAT"
        assert dt.value == "FLOAT"
        assert str(dt) == "float"
        assert dt == DataTypeEnum["FLOAT"]
        assert dt.type == float

    def test_str(self):
        """Проверяет тип string"""
        dt = DataTypeEnum.STRING
        assert dt.name == "STRING"
        assert dt.value == "STRING"
        assert str(dt) == "string"
        assert dt == DataTypeEnum["STRING"]
        assert dt.type == str

    def test_bool(self):
        """Проверяет тип bool"""
        dt = DataTypeEnum.BOOL
        assert dt.name == "BOOL"
        assert dt.value == "BOOL"
        assert str(dt) == "bool"
        assert dt == DataTypeEnum["BOOL"]
        assert dt.type == bool


if __name__ == "__main__":
    pytest.main(["-k", "TestDataType"])
