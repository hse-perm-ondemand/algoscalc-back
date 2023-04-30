import unittest
import os
import json
from shutil import rmtree
from jsonschema.exceptions import ValidationError

from src.core_tests.constants import FOLDER_PATH, FIB_DEF, FIB_FUNC, FIB_TESTS,\
    WRONG_FIB_TESTS, DEFINITION_FILE_NAME, FUNCTION_FILE_NAME, TEST_FILE_NAME,\
    SCHEMA_FILE_PATH, ALGORITHM_CONFIG, LOG_CONFIG_STUB
from src.core.algorithm_builder import AlgorithmBuilder, UNIT_TEST_FAILED_MSG,\
    NON_STRING_PARAM_TEMPL, EMPTY_STRING_PARAM_TEMPL


class AlgorithmBuilderTest(unittest.TestCase):
    builder = AlgorithmBuilder(DEFINITION_FILE_NAME, FUNCTION_FILE_NAME,
                               TEST_FILE_NAME, SCHEMA_FILE_PATH,
                               ALGORITHM_CONFIG, LOG_CONFIG_STUB)

    @classmethod
    def setUpClass(cls) -> None:
        if os.path.exists(os.path.basename(__file__)):
            os.chdir('../..')
        if not os.path.exists(FOLDER_PATH):
            os.mkdir(FOLDER_PATH)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(FOLDER_PATH):
            os.removedirs(FOLDER_PATH)

    def tearDown(self) -> None:
        if os.path.exists(FOLDER_PATH):
            for file in os.listdir(FOLDER_PATH):
                path = FOLDER_PATH + '/' + file
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    rmtree(path)

    def write_file(self, file_name, text):
        with open(FOLDER_PATH + '/' + file_name, 'w') as file:
            file.write(text)

    def write_json(self, file_name, json_text):
        with open(FOLDER_PATH + '/' + file_name, 'w') as file:
            json.dump(json_text, file)

    def test_non_string_definition(self):
        with self.assertRaises(ValueError) as error:
            AlgorithmBuilder(100500, FUNCTION_FILE_NAME, TEST_FILE_NAME,
                             SCHEMA_FILE_PATH, ALGORITHM_CONFIG,
                             LOG_CONFIG_STUB)
        self.assertEqual(NON_STRING_PARAM_TEMPL.format('definition_file_name'),
                         str(error.exception))

    def test_empty_definition(self):
        with self.assertRaises(ValueError) as error:
            AlgorithmBuilder('', FUNCTION_FILE_NAME, TEST_FILE_NAME,
                             SCHEMA_FILE_PATH, ALGORITHM_CONFIG,
                             LOG_CONFIG_STUB)
        self.assertEqual(EMPTY_STRING_PARAM_TEMPL.format('definition_file_name'),
                         str(error.exception))

    def test_non_string_function(self):
        with self.assertRaises(ValueError) as error:
            AlgorithmBuilder(DEFINITION_FILE_NAME, 123, TEST_FILE_NAME,
                             SCHEMA_FILE_PATH, ALGORITHM_CONFIG,
                             LOG_CONFIG_STUB)
        self.assertEqual(NON_STRING_PARAM_TEMPL.format('function_file_name'),
                         str(error.exception))

    def test_empty_function(self):
        with self.assertRaises(ValueError) as error:
            AlgorithmBuilder(DEFINITION_FILE_NAME, '', TEST_FILE_NAME,
                             SCHEMA_FILE_PATH, ALGORITHM_CONFIG,
                             LOG_CONFIG_STUB)
        self.assertEqual(EMPTY_STRING_PARAM_TEMPL.format('function_file_name'),
                         str(error.exception))

    def test_non_string_test(self):
        with self.assertRaises(ValueError) as error:
            AlgorithmBuilder(DEFINITION_FILE_NAME, FUNCTION_FILE_NAME, 1.,
                             SCHEMA_FILE_PATH, ALGORITHM_CONFIG,
                             LOG_CONFIG_STUB)
        self.assertEqual(NON_STRING_PARAM_TEMPL.format('test_file_name'),
                         str(error.exception))

    def test_empty_test(self):
        with self.assertRaises(ValueError) as error:
            AlgorithmBuilder(DEFINITION_FILE_NAME, FUNCTION_FILE_NAME, '',
                             SCHEMA_FILE_PATH, ALGORITHM_CONFIG,
                             LOG_CONFIG_STUB)
        self.assertEqual(EMPTY_STRING_PARAM_TEMPL.format('test_file_name'),
                         str(error.exception))

    def test_non_string_schema(self):
        with self.assertRaises(ValueError) as error:
            AlgorithmBuilder(DEFINITION_FILE_NAME, FUNCTION_FILE_NAME,
                             TEST_FILE_NAME, [], ALGORITHM_CONFIG,
                             LOG_CONFIG_STUB)
        self.assertEqual(NON_STRING_PARAM_TEMPL.format('schema_file_path'),
                         str(error.exception))

    def test_empty_schema(self):
        with self.assertRaises(ValueError) as error:
            AlgorithmBuilder(DEFINITION_FILE_NAME, FUNCTION_FILE_NAME,
                             TEST_FILE_NAME, '', ALGORITHM_CONFIG,
                             LOG_CONFIG_STUB)
        self.assertEqual(EMPTY_STRING_PARAM_TEMPL.format('schema_file_path'),
                         str(error.exception))

    def test_build(self):
        self.write_json(DEFINITION_FILE_NAME, FIB_DEF)
        self.write_file(FUNCTION_FILE_NAME, FIB_FUNC)
        self.write_file(TEST_FILE_NAME, FIB_TESTS)
        alg = self.builder.build_algorithm(FOLDER_PATH)
        self.assertIsNone(alg.get_test_errors())

    def test_build_wrong_def(self):
        fib_def = FIB_DEF.copy()
        fib_def['title'] = None
        self.write_json(DEFINITION_FILE_NAME, fib_def)
        self.write_file(FUNCTION_FILE_NAME, FIB_FUNC)
        self.write_file(TEST_FILE_NAME, FIB_TESTS)
        self.assertRaises(ValidationError, self.builder.build_algorithm,
                          FOLDER_PATH)

    def test_build_failed_test(self):
        self.write_json(DEFINITION_FILE_NAME, FIB_DEF)
        self.write_file(FUNCTION_FILE_NAME, FIB_FUNC)
        self.write_file(TEST_FILE_NAME, WRONG_FIB_TESTS)
        self.assertRaisesRegex(RuntimeError, UNIT_TEST_FAILED_MSG,
                               self.builder.build_algorithm, FOLDER_PATH)

    def test_build_missing_def(self):
        self.write_file(FUNCTION_FILE_NAME, FIB_FUNC)
        self.write_file(TEST_FILE_NAME, FIB_TESTS)
        self.assertRaises(FileNotFoundError, self.builder.build_algorithm,
                          FOLDER_PATH)

    def test_build_missing_func(self):
        self.write_json(DEFINITION_FILE_NAME, FIB_DEF)
        self.write_file(TEST_FILE_NAME, FIB_TESTS)
        self.assertRaises(FileNotFoundError, self.builder.build_algorithm,
                          FOLDER_PATH)

    def test_build_missing_tests(self):
        self.write_json(DEFINITION_FILE_NAME, FIB_DEF)
        self.write_file(FUNCTION_FILE_NAME, FIB_FUNC)
        self.assertRaises(FileNotFoundError, self.builder.build_algorithm,
                          FOLDER_PATH)


if __name__ == '__main__':
    unittest.main()
