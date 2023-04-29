import os


FOLDER_PATH = os.getcwd() + '/algorithm_builder'
COLLECTION_FOLDER_PATH = os.getcwd() + '/algorithm_collection'
DEFINITION_FILE_NAME = 'definition.json'
FUNCTION_FILE_NAME = 'function.py'
TEST_FILE_NAME = 'tests.py'
NONE_VALUE_MSG = 'The value is None!'
NOT_MATRIX_VALUE_MSG = 'The value is not a matrix!'
NOT_LIST_VALUE_MSG = 'The value is not a list!'
SCHEMA_FILE_PATH = 'src/core/schemas/algorithm_schema.json'
PATH_CONFIG = {
    'definition_file_name': 'definition.json',
    'function_file_name': 'function.py',
    'test_file_name': 'tests.py',
    'json_schema_file_path': 'src/core/schemas/algorithm_schema.json',
    'algorithms_catalog_path': 'src/algorithms'
  }
ALGORITHM_CONFIG = {'execute_timeout': 5}
FIB_TITLE = 'Числа Фибоначчи'
FIB_DEF = {
  "title": FIB_TITLE,
  "description": "Вычисление n-го числа Фибоначчи",
  "parameters": [
    {
      "name": "n",
      "title": "Номер числа Фибоначчи",
      "description": "Введите целое положительное число больше единицы",
      "data_type": "INT",
      "data_shape": "SCALAR",
      "default_value": 1
    }
  ],
  "outputs": [
    {
      "name": "result",
      "title": "Число Фибоначчи",
      "description": "Число Фибоначчи с номером n",
      "data_type": "INT",
      "data_shape": "SCALAR",
      "default_value": 1
    }
  ]
}
FIB_FUNC = """def fibonacci(n: int) -> int:
    if n == 1 or n == 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)
def main(n: int):
    return {'result': fibonacci(n)}"""
FIB_TESTS = """import unittest
from algorithms.fibonacci.function import fibonacci
class TestCase(unittest.TestCase):
    numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    def test_fibonacci(self):
        for index, number in enumerate(self.numbers):
            self.assertEqual(fibonacci(index + 1), number)"""
