"""Реализация API для онлайн-калькулятора с использованием фреймворка FastAPI.
"""

import json
import logging.config
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import (
    ALGORITHM_CONFIG,
    ALGORITHMS_ENDPOINT,
    APP_CONFIG_FILE_PATH,
    EXECUTE_TIMEOUT,
    IS_TEST_APP,
    LOG_CONFIG_FILE_PATH,
    PATH_CONFIG,
    TIME_OVER_MSG,
)
from src.api_models import (
    AlgorithmDefinition,
    Algorithms,
    AlgorithmTitle,
    AnswerAlgorithmDefinition,
    AnswerOutputs,
    Data,
    DataDefinition,
    Outputs,
    Parameters,
)
from src.core.algorithm_collection import (
    ALGORITHM_NOT_EXISTS_TEMPL,
    AlgorithmCollection,
)

if os.path.exists("../" + LOG_CONFIG_FILE_PATH):
    os.chdir("..")
with open(LOG_CONFIG_FILE_PATH, "r") as log_conf_file:
    log_config = json.load(log_conf_file)
file_path = None
try:
    file_path = log_config["handlers"]["file_handler"]["filename"]
except KeyError:
    pass
if file_path:
    folder = os.path.split(file_path)[0]
    if not os.path.isdir(folder):
        os.mkdir(folder)
logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.info("Start app")

with open(APP_CONFIG_FILE_PATH, "r") as conf_file:
    config = json.load(conf_file)
path_config = config[PATH_CONFIG]
algorithm_config = config[ALGORITHM_CONFIG]
if bool(os.environ.get(IS_TEST_APP)):
    algorithm_config[EXECUTE_TIMEOUT] = 0

algorithms = AlgorithmCollection(path_config, algorithm_config, log_config)

app = FastAPI()
web_config = config["web_config"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=web_config["cors"]["origins"],
    allow_credentials=web_config["cors"]["credentials"],
    allow_methods=web_config["cors"]["methods"],
    allow_headers=web_config["cors"]["headers"],
)


@app.get(ALGORITHMS_ENDPOINT)
async def get_algorithms() -> Algorithms:
    """Возвращает список имеющихся алгоритмов.

    :return: список имеющихся алгоритмов.
    :rtype: Algorithms
    """
    res = Algorithms(algorithms=[])
    for name, title in algorithms.get_name_title_dict().items():
        res.algorithms.append(AlgorithmTitle(name=name, title=title))
    return res


@app.get(ALGORITHMS_ENDPOINT + "/{algorithm_name}")
async def get_algorithm(algorithm_name: str) -> AnswerAlgorithmDefinition:
    """Возвращает описание выбранного алгоритма.

    :param algorithm_name: имя алгоритма;
    :type algorithm_name: str
    :return: Описание алгоритма.
    :rtype: AnswerAlgorithmDefinition
    """
    if not algorithms.has_algorithm(algorithm_name):
        return AnswerAlgorithmDefinition(
            errors=ALGORITHM_NOT_EXISTS_TEMPL.format(algorithm_name), result=None
        )
    try:
        alg = algorithms.get_algorithm(algorithm_name)
        params = []
        outputs = []
        for param in alg.parameters:
            params.append(
                DataDefinition(
                    name=param.name,
                    title=param.title,
                    description=param.description,
                    data_type=str(param.data_type),
                    data_shape=str(param.data_shape),
                    default_value=param.default_value,
                )
            )
        for output in alg.outputs:
            outputs.append(
                DataDefinition(
                    name=output.name,
                    title=output.title,
                    description=output.description,
                    data_type=str(output.data_type),
                    data_shape=str(output.data_shape),
                    default_value=output.default_value,
                )
            )
        alg_def = AlgorithmDefinition(
            name=alg.name,
            title=alg.title,
            description=alg.description,
            parameters=params,
            outputs=outputs,
        )
        return AnswerAlgorithmDefinition(result=alg_def, errors=None)
    except Exception as error:
        logger.warning(str(error))
        return AnswerAlgorithmDefinition(errors=str(error), result=None)


@app.post(ALGORITHMS_ENDPOINT + "/{algorithm_name}")
async def get_algorithm_result(
    algorithm_name: str, parameters: Parameters
) -> AnswerOutputs:
    """Возвращает результат выполнения выбранного алгоритма.

    :param algorithm_name: имя алгоритма;
    :type algorithm_name: str
    :param parameters: значения входных данных для выполнения алгоритма.
    :type parameters: Parameters
    :return: результат выполнения выбранного алгоритма
    :rtype: AnswerOutputs
    """
    if not algorithms.has_algorithm(algorithm_name):
        return AnswerOutputs(
            errors=ALGORITHM_NOT_EXISTS_TEMPL.format(algorithm_name), result=None
        )
    params = parameters.get_params_to_execute()
    try:
        results = algorithms.get_algorithm_result(algorithm_name, params)
        outputs = []
        for name, value in results.items():
            outputs.append(Data(name=name, value=value))
        return AnswerOutputs(result=Outputs(outputs=outputs), errors=None)
    except TimeoutError:
        logger.warning(TIME_OVER_MSG)
        return AnswerOutputs(result=None, errors=TIME_OVER_MSG)
    except Exception as error:
        logger.warning(str(error))
        return AnswerOutputs(result=None, errors=str(error))


def start():
    """Запуск приложения."""
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    start()
