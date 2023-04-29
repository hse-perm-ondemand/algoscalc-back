import unittest
import os
import json
from shutil import rmtree
from jsonschema.exceptions import ValidationError

from src.core_tests.constants import FOLDER_PATH, FIB_DEF, FIB_FUNC, FIB_TESTS,\
    DEFINITION_FILE_NAME, FUNCTION_FILE_NAME, TEST_FILE_NAME, SCHEMA_FILE_PATH,\
    ALGORITHM_CONFIG
from src.core.algorithm_builder import AlgorithmBuilder


class AlgorithmBuilderTest(unittest.TestCase):
    builder = AlgorithmBuilder(DEFINITION_FILE_NAME, FUNCTION_FILE_NAME,
                               TEST_FILE_NAME, SCHEMA_FILE_PATH,
                               ALGORITHM_CONFIG)

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

    def test_non_string_definition(self):
        self.assertRaisesRegex(ValueError, 'The definition_file_name '
                                           'parameter is not a string',
                               AlgorithmBuilder.__init__, None, 100500,
                               FUNCTION_FILE_NAME, TEST_FILE_NAME,
                               SCHEMA_FILE_PATH, ALGORITHM_CONFIG)

    def test_empty_definition(self):
        self.assertRaisesRegex(ValueError, 'The definition_file_name '
                                           'parameter is empty',
                               AlgorithmBuilder.__init__, None, '',
                               FUNCTION_FILE_NAME, TEST_FILE_NAME,
                               SCHEMA_FILE_PATH, ALGORITHM_CONFIG)

    def test_non_string_function(self):
        self.assertRaisesRegex(ValueError, 'The function_file_name '
                                           'parameter is not a string',
                               AlgorithmBuilder.__init__, None,
                               DEFINITION_FILE_NAME, 123, TEST_FILE_NAME,
                               SCHEMA_FILE_PATH, ALGORITHM_CONFIG)
    def test_empty_function(self):
        self.assertRaisesRegex(ValueError, 'The function_file_name '
                                           'parameter is empty',

                               AlgorithmBuilder.__init__, None,
                               DEFINITION_FILE_NAME, '', TEST_FILE_NAME,
                               SCHEMA_FILE_PATH, ALGORITHM_CONFIG)
    def test_non_string_test(self):
        self.assertRaisesRegex(ValueError, 'The test_file_name '
                                           'parameter is not a string',
                               AlgorithmBuilder.__init__, None,
                               DEFINITION_FILE_NAME, FUNCTION_FILE_NAME, 1.,
                               SCHEMA_FILE_PATH, ALGORITHM_CONFIG)

    def test_empty_test(self):
        self.assertRaisesRegex(ValueError, 'The test_file_name '
                                           'parameter is empty',
                               AlgorithmBuilder.__init__, None,
                               DEFINITION_FILE_NAME, FUNCTION_FILE_NAME, '',
                               SCHEMA_FILE_PATH, ALGORITHM_CONFIG)
    def test_non_string_schema(self):
        self.assertRaisesRegex(ValueError, 'The schema_file_path '
                                           'parameter is not a string',
                               AlgorithmBuilder.__init__, None,
                               DEFINITION_FILE_NAME, FUNCTION_FILE_NAME,
                               TEST_FILE_NAME, [], ALGORITHM_CONFIG)

    def test_empty_schema(self):
        self.assertRaisesRegex(ValueError, 'The schema_file_path '
                                           'parameter is empty',
                               AlgorithmBuilder.__init__, None,
                               DEFINITION_FILE_NAME, FUNCTION_FILE_NAME,
                               TEST_FILE_NAME, '', ALGORITHM_CONFIG)

    def test_build(self):
        with open(FOLDER_PATH + '/' + DEFINITION_FILE_NAME, 'w') as def_file:
            json.dump(FIB_DEF, def_file)
        with open(FOLDER_PATH + '/' + FUNCTION_FILE_NAME, 'w') as func_file:
            func_file.write(FIB_FUNC)
        with open(FOLDER_PATH + '/' + TEST_FILE_NAME, 'w') as test_file:
            test_file.write(FIB_TESTS)
        alg = self.builder.build_algorithm(FOLDER_PATH)
        self.assertIsNone(alg.get_test_errors())

    def test_build_wrong_def(self):
        fib_def = FIB_DEF.copy()
        fib_def['title'] = None
        with open(FOLDER_PATH + '/' + DEFINITION_FILE_NAME, 'w') as def_file:
            json.dump(fib_def, def_file)
        with open(FOLDER_PATH + '/' + FUNCTION_FILE_NAME, 'w') as func_file:
            func_file.write(FIB_FUNC)
        with open(FOLDER_PATH + '/' + TEST_FILE_NAME, 'w') as test_file:
            test_file.write(FIB_TESTS)
        self.assertRaisesRegex(ValidationError, "None is not of type 'string'",
                               self.builder.build_algorithm, FOLDER_PATH)

    def test_build_missing_def(self):
        with open(FOLDER_PATH + '/' + FUNCTION_FILE_NAME, 'w') as func_file:
            func_file.write(FIB_FUNC)
        with open(FOLDER_PATH + '/' + TEST_FILE_NAME, 'w') as test_file:
            test_file.write(FIB_TESTS)
        self.assertRaises(FileNotFoundError, self.builder.build_algorithm,
                          FOLDER_PATH)

    def test_build_missing_func(self):
        with open(FOLDER_PATH + '/' + DEFINITION_FILE_NAME, 'w') as def_file:
            json.dump(FIB_DEF, def_file)
        with open(FOLDER_PATH + '/' + TEST_FILE_NAME, 'w') as test_file:
            test_file.write(FIB_TESTS)
        self.assertRaises(FileNotFoundError, self.builder.build_algorithm,
                          FOLDER_PATH)

    def test_build_missing_tests(self):
        with open(FOLDER_PATH + '/' + DEFINITION_FILE_NAME, 'w') as def_file:
            json.dump(FIB_DEF, def_file)
        with open(FOLDER_PATH + '/' + FUNCTION_FILE_NAME, 'w') as func_file:
            func_file.write(FIB_FUNC)
        self.assertRaises(FileNotFoundError, self.builder.build_algorithm,
                          FOLDER_PATH)


if __name__ == '__main__':
    unittest.main()
