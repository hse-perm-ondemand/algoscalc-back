import os
import json
import importlib.util
from io import StringIO
from typing import Callable, Any, Optional
import jsonschema
import unittest

from src.core.data_element import DataElement, DataType, DataShape
from src.core.algorithm import Algorithm


class AlgorithmBuilder:
    NAME = 'name'
    TITLE = 'title'
    DESCRIPTION = 'description'
    PARAMETERS = 'parameters'
    OUTPUTS = 'outputs'
    DATA_TYPE = 'data_type'
    DATA_SHAPE = 'data_shape'
    DEFAULT_VALUE = 'default_value'
    EXECUTE_TIMEOUT = 'execute_timeout'

    def __init__(self, definition_file_name: str, function_file_name: str,
                 test_file_name: str, schema_file_path: str,
                 algorithm_config: dict[str, Any]):
        param_errors = AlgorithmBuilder.__check_params(definition_file_name,
                                                       function_file_name,
                                                       test_file_name,
                                                       schema_file_path)
        if param_errors is not None:
            raise ValueError(param_errors)
        self.__definition_file_name: str = definition_file_name
        self.__function_file_name: str = function_file_name
        self.__test_file_name: str = test_file_name
        self.__schema_file_path: str = schema_file_path
        self.__algorithm_config: dict[str, Any] = algorithm_config

    def build_algorithm(self, path: str) -> Algorithm:
        with open(path + '/' + self.__definition_file_name,
                  'r') as def_file:
            definition = json.load(def_file)
        self.__validate_definition_raises_ex(definition)
        name = os.path.split(path)[-1]
        alg = Algorithm(name, definition[self.TITLE],
                        definition[self.DESCRIPTION],
                        self.__algorithm_config[self.EXECUTE_TIMEOUT])
        for param_def in definition[self.PARAMETERS]:
            alg.add_parameter(self.__get_data_element(param_def))
        for output_def in definition[self.OUTPUTS]:
            alg.add_output(self.__get_data_element(output_def))
        if not self.__test_function(path):
            raise RuntimeError('Unit-test for the algorithm method was failed!')
        alg.add_execute_method(self.__get_function(path))
        return alg

    def __validate_definition_raises_ex(self, definition: dict[str, Any]) \
            -> None:
        with open(self.__schema_file_path, 'r') as schema_file:
            schema = json.load(schema_file)
        jsonschema.validate(definition, schema)

    def __get_data_element(self,
                           data_element_def: dict[str, Any]) -> DataElement:
        return DataElement(data_element_def[self.NAME],
                           data_element_def[self.TITLE],
                           data_element_def[self.DESCRIPTION],
                           DataType[data_element_def[self.DATA_TYPE]],
                           DataShape[data_element_def[self.DATA_SHAPE]],
                           data_element_def[self.DEFAULT_VALUE])

    def __get_function(self, path: str) -> Callable:
        file_name = self.__function_file_name
        spec = importlib.util.spec_from_file_location(file_name,
                                                      path + '/' + file_name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.main

    def __test_function(self, path: str) -> bool:
        file_name = self.__test_file_name
        spec = importlib.util.spec_from_file_location(file_name,
                                                      path + '/' + file_name)
        test_case = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_case)
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(test_case.TestCase))
        sio = StringIO()
        runner = unittest.TextTestRunner(sio, verbosity=0)
        test_result = runner.run(suite)
        return test_result.wasSuccessful()

    @staticmethod
    def __check_params(definition_file_name: str, function_file_name: str,
                       test_file_name: str, schema_file_path: str) \
            -> Optional[str]:
        if type(definition_file_name) != str:
            return 'The definition_file_name parameter is not a string'
        if not definition_file_name:
            return 'The definition_file_name parameter is empty'
        if type(function_file_name) != str:
            return 'The function_file_name parameter is not a string'
        if not function_file_name:
            return 'The function_file_name parameter is empty'
        if type(test_file_name) != str:
            return 'The test_file_name parameter is not a string'
        if not test_file_name:
            return 'The test_file_name parameter is empty'
        if type(schema_file_path) != str:
            return 'The schema_file_path parameter is not a string'
        if not schema_file_path:
            return 'The schema_file_path parameter is empty'
        return None
