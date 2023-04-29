import unittest
import os
import json
from shutil import rmtree

from src.core_tests.constants import COLLECTION_FOLDER_PATH, PATH_CONFIG,\
    ALGORITHM_CONFIG, DEFINITION_FILE_NAME, FUNCTION_FILE_NAME, TEST_FILE_NAME,\
    FIB_DEF, FIB_FUNC, FIB_TESTS
from src.core.algorithm_collection import AlgorithmCollection
from src.core.algorithm import Algorithm


class AlgorithmCollectionTests(unittest.TestCase):
    path_config = PATH_CONFIG
    path_config['algorithms_catalog_path'] = COLLECTION_FOLDER_PATH

    @classmethod
    def setUpClass(cls) -> None:
        if os.path.exists(os.path.basename(__file__)):
            os.chdir('../..')
        if not os.path.exists(COLLECTION_FOLDER_PATH):
            os.mkdir(COLLECTION_FOLDER_PATH)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(COLLECTION_FOLDER_PATH):
            os.removedirs(COLLECTION_FOLDER_PATH)

    def tearDown(self) -> None:
        if os.path.exists(COLLECTION_FOLDER_PATH):
            for file in os.listdir(COLLECTION_FOLDER_PATH):
                path = COLLECTION_FOLDER_PATH + '/' + file
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    rmtree(path)

    def test_empty_catalog(self):
        with self.assertRaises(RuntimeError) as error:
            AlgorithmCollection(self.path_config, ALGORITHM_CONFIG)
        self.assertEqual(str(error.exception), 'No algorithm was found')

    def test_single_algorithm(self):
        name = 'test_single'
        self.create_files(name)
        algorithms = AlgorithmCollection(self.path_config, ALGORITHM_CONFIG)
        self.assertEqual(algorithms.get_name_title_dict(),
                         {'test_single': 'Числа Фибоначчи'})
        alg = algorithms.get_algorithm(name)
        self.assertIsInstance(alg, Algorithm)
        self.assertEqual(alg.name, name)
        self.assertEqual(algorithms.get_algorithm_result(name, {'n': 20}),
                         {'result': 6765})
        self.assertTrue(algorithms.has_algorithm(name))

    def test_double_algorithms(self):
        names = ['test1', 'test2']
        for name in names:
            self.create_files(name)
        algorithms = AlgorithmCollection(self.path_config, ALGORITHM_CONFIG)
        self.assertEqual(algorithms.get_name_title_dict(),
                         {'test1': 'Числа Фибоначчи',
                          'test2': 'Числа Фибоначчи'})

    def test_triple_algorithms(self):
        names = ['test1', 'test2', 'test3']
        for name in names:
            self.create_files(name)
        algorithms = AlgorithmCollection(self.path_config, ALGORITHM_CONFIG)
        self.assertEqual(algorithms.get_name_title_dict(),
                         {'test1': 'Числа Фибоначчи',
                          'test2': 'Числа Фибоначчи',
                          'test3': 'Числа Фибоначчи'})

    def test_algorithm_not_exists(self):
        name = 'test_single'
        wrong_name = 'wrong_name'
        self.create_files(name)
        algorithms = AlgorithmCollection(self.path_config, ALGORITHM_CONFIG)
        self.assertFalse(algorithms.has_algorithm(wrong_name))
        self.assertRaisesRegex(ValueError, f'Algorithm named "{wrong_name}" '
                                           f'does not exists',
                               algorithms.get_algorithm, wrong_name)
        self.assertRaisesRegex(ValueError, f'Algorithm named "{wrong_name}" '
                                           f'does not exists',
                               algorithms.get_algorithm_result, wrong_name,
                               {'n': 20})

    def create_files(self, name: str) -> None:
        path = COLLECTION_FOLDER_PATH + '/' + name
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path + '/' + DEFINITION_FILE_NAME, 'w') as def_file:
            json.dump(FIB_DEF, def_file)
        with open(path + '/' + FUNCTION_FILE_NAME, 'w') as func_file:
            func_file.write(FIB_FUNC)
        with open(path + '/' + TEST_FILE_NAME, 'w') as test_file:
            test_file.write(FIB_TESTS)


if __name__ == '__main__':
    unittest.main()
