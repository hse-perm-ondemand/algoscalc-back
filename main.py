from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import json


from core.algorithm_collection import AlgorithmCollection


CONFIG_FILE_PATH = "config.json"
RESULT = 'result'
ERRORS = 'errors'

with open(CONFIG_FILE_PATH, 'r') as conf_file:
    config = json.load(conf_file)
path_config = config['path_config']
algorithm_config = config['algorithm_config']

algorithms = AlgorithmCollection(path_config, algorithm_config)

app = FastAPI()


class Parameter(BaseModel):
    name: str
    value: Union[int, float, str, bool,
                 list[Union[int, float, str, bool,
                            list[Union[int, float, str, bool]]]]]


class Parameters(BaseModel):
    parameters: list[Parameter]

    def get_params_to_execute(self):
        return {param.name: param.value for param in self.parameters}


@app.get("/api/algorithms")
async def get_algorithms():
    return algorithms.get_name_title_dict()


@app.get("/api/algorithms/{algorithm_name}")
async def get_algorithm(algorithm_name: str):
    answer = {RESULT: None, ERRORS: None}
    if not algorithms.has_algorithm(algorithm_name):
        answer[ERRORS] = f'Algorithm named "{algorithm_name}" does not exists'
        return answer
    try:
        answer[RESULT] = algorithms.get_algorithm_dict(algorithm_name)
    except Exception as ex:
        answer[ERRORS] = str(ex)
    return answer


@app.post("/api/algorithms/{algorithm_name}")
async def get_algorithm_result(algorithm_name: str, parameters: Parameters):
    answer = {RESULT: None, ERRORS: None}
    if not algorithms.has_algorithm(algorithm_name):
        answer[ERRORS] = f'Algorithm named "{algorithm_name}" does not exists'
        return answer
    params = parameters.get_params_to_execute()
    try:
        answer[RESULT] = algorithms.get_algorithm_result(algorithm_name, params)
    except TimeoutError:
        answer[ERRORS] = 'The time for algorithm execution is over'
    except RuntimeError as ex:
        answer[ERRORS] = str(ex)
    return answer
