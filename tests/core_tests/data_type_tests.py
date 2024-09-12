import unittest

from src.core.data_element import DataType


class DataTypeTests(unittest.TestCase):
    def test_types(self):
        self.assertEqual([int, float, str, bool], DataType.types())

    def test_int(self):
        dt = DataType.INT
        self.assertEqual(dt.name, "INT")
        self.assertEqual(dt.value, "INT")
        self.assertEqual(str(dt), "int")
        self.assertEqual(dt, DataType["INT"])
        self.assertEqual(dt.type, int)

    def test_float(self):
        dt = DataType.FLOAT
        self.assertEqual(dt.name, "FLOAT")
        self.assertEqual(dt.value, "FLOAT")
        self.assertEqual(str(dt), "float")
        self.assertEqual(dt, DataType["FLOAT"])
        self.assertEqual(dt.type, float)

    def test_str(self):
        dt = DataType.STRING
        self.assertEqual(dt.name, "STRING")
        self.assertEqual(dt.value, "STRING")
        self.assertEqual(str(dt), "string")
        self.assertEqual(dt, DataType["STRING"])
        self.assertEqual(dt.type, str)

    def test_bool(self):
        dt = DataType.BOOL
        self.assertEqual(dt.name, "BOOL")
        self.assertEqual(dt.value, "BOOL")
        self.assertEqual(str(dt), "bool")
        self.assertEqual(dt, DataType["BOOL"])
        self.assertEqual(dt.type, bool)


if __name__ == "__main__":
    unittest.main()
