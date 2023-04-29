import os
import json
from fastapi import FastAPI

from src.core.algorithm_collection import AlgorithmCollection
from src.api_models import AlgorithmTitle, Algorithms, DataDefinition, \
    AlgorithmDefinition, Data, Parameters, Outputs, AnswerOutputs, \
    AnswerAlgorithmDefinition
from src.constants import APP_CONFIG_FILE_PATH, PATH_CONFIG, ALGORITHM_CONFIG, \
    IS_TEST_APP, EXECUTE_TIMEOUT


with open(APP_CONFIG_FILE_PATH, 'r') as conf_file:
    config = json.load(conf_file)
path_config = config[PATH_CONFIG]
algorithm_config = config[ALGORITHM_CONFIG]
if bool(os.environ.get(IS_TEST_APP)):
    algorithm_config[EXECUTE_TIMEOUT] = 0
algorithms = AlgorithmCollection(path_config, algorithm_config)

app = FastAPI()


@app.get("/api/algorithms")
async def get_algorithms() -> Algorithms:
    res = Algorithms(algorithms=[])
    for name, title in algorithms.get_name_title_dict().items():
        res.algorithms.append(AlgorithmTitle(name=name, title=title))
    return res


@app.get("/api/algorithms/{algorithm_name}")
async def get_algorithm(algorithm_name: str) -> AnswerAlgorithmDefinition:
    answer = AnswerAlgorithmDefinition()
    if not algorithms.has_algorithm(algorithm_name):
        answer.errors = f'Algorithm named "{algorithm_name}" does not exists'
        return answer
    try:
        alg = algorithms.get_algorithm(algorithm_name)
        params = []
        outputs = []
        for param in alg.parameters:
            params.append(
                DataDefinition(name=param.name, title=param.title,
                               description=param.description,
                               data_type=str(param.data_type),
                               data_shape=str(param.data_shape),
                               default_value=param.default_value))
        for output in alg.outputs:
            outputs.append(
                DataDefinition(name=output.name, title=output.title,
                               description=output.description,
                               data_type=str(output.data_type),
                               data_shape=str(output.data_shape),
                               default_value=output.default_value))
        alg_def = AlgorithmDefinition(name=alg.name, title=alg.title,
                                      description=alg.description,
                                      parameters=params, outputs=outputs)
        answer.result = alg_def
    except Exception as ex:
        answer.errors = str(ex)
    return answer


@app.post("/api/algorithms/{algorithm_name}")
async def get_algorithm_result(algorithm_name: str, parameters: Parameters) \
        -> AnswerOutputs:
    answer = AnswerOutputs()
    if not algorithms.has_algorithm(algorithm_name):
        answer.errors = f'Algorithm named "{algorithm_name}" does not exists'
        return answer
    params = parameters.get_params_to_execute()
    try:
        results = algorithms.get_algorithm_result(algorithm_name, params)
        outputs = []
        for name, value in results.items():
            outputs.append(Data(name=name, value=value))
        answer.result = Outputs(outputs=outputs)
    except TimeoutError:
        answer.errors = 'The time for algorithm execution is over'
    except Exception as ex:
        answer.errors = str(ex)
    return answer
