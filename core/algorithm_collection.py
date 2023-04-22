import os
from typing import Any, Union

from core.algorithm import Algorithm
from core.algorithm_builder import AlgorithmBuilder


class AlgorithmCollection:
    def __init__(self, path_config: dict[str, str],
                 algorithm_config: dict[str, Union[str, int]]):
        self.__algorithms: dict[str, Algorithm] = {}
        builder = AlgorithmBuilder(path_config['definition_file_name'],
                                   path_config['function_file_name'],
                                   path_config['test_file_name'],
                                   path_config['json_schema_file_path'],
                                   algorithm_config)
        catalog_path = path_config['algorithms_catalog_path']
        for obj in os.listdir(catalog_path):
            alg_path = catalog_path + '/' + obj
            if os.path.isdir(alg_path):
                alg = builder.build_algorithm(alg_path)
                self.__algorithms[alg.name] = alg
        if len(self.__algorithms) == 0:
            raise RuntimeError('No algorithm was found')

    def has_algorithm(self, algorithm_name: str) -> bool:
        return algorithm_name in self.__algorithms

    def get_name_title_dict(self) -> dict[str, str]:
        return {name: alg.title for name, alg in self.__algorithms.items()}

    def get_algorithm_dict(self, algorithm_name: str) -> dict[str: Any]:
        if algorithm_name not in self.__algorithms:
            raise ValueError(f'Algorithm named "{algorithm_name}" '
                             'does not exists')
        return self.__algorithms[algorithm_name].to_dict()

    def get_algorithm_result(self, algorithm_name: str,
                             params: dict[str, Any]) -> dict[str, Any]:
        if algorithm_name not in self.__algorithms:
            raise ValueError(f'Algorithm named "{algorithm_name}" '
                             'does not exists')
        return self.__algorithms[algorithm_name].execute(params)
