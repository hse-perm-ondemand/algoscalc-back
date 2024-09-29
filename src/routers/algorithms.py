import logging

from fastapi import APIRouter, Depends, Request

from src.internal.algorithm_collection import AlgorithmCollection
from src.internal.constants import ALGORITHMS_ENDPOINT
from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.errors import ErrorMessageTemplateEnum as ErrMsgTmpl
from src.internal.schemas.definition_schema import DefinitionSchema
from src.routers.schemas import (
    AnswerAlgorithmDefinition,
    AnswerOutputs,
    Data,
    Outputs,
    Parameters,
)


def get_app_algorithms(request: Request) -> AlgorithmCollection:
    return request.app.state.algorithms


router = APIRouter(
    prefix=ALGORITHMS_ENDPOINT,
)
logger = logging.getLogger(__name__)


@router.get("/")
async def get_algorithms(
    algorithms: AlgorithmCollection = Depends(get_app_algorithms),
) -> list[DefinitionSchema]:
    """Возвращает список имеющихся алгоритмов.

    :return: список имеющихся алгоритмов.
    :rtype: list[BaseEntityModel]
    """
    return algorithms.get_algorithm_list()


@router.get("/{algorithm_name}")
async def get_algorithm(
    algorithm_name: str, algorithms: AlgorithmCollection = Depends(get_app_algorithms)
) -> AnswerAlgorithmDefinition:
    """Возвращает описание выбранного алгоритма.

    :param algorithm_name: имя алгоритма;
    :type algorithm_name: str
    :return: Описание алгоритма.
    :rtype: AnswerAlgorithmDefinition
    """
    if not algorithms.has_algorithm(algorithm_name):
        return AnswerAlgorithmDefinition(
            errors=ErrMsgTmpl.ALGORITHM_NOT_EXISTS.format(algorithm_name),
            result=None,
        )
    try:
        return AnswerAlgorithmDefinition(
            result=algorithms.get_algorithm_definition(algorithm_name), errors=None
        )
    except Exception as error:
        logger.warning(str(error))
        return AnswerAlgorithmDefinition(errors=str(error), result=None)


@router.post("/{algorithm_name}")
async def get_algorithm_result(
    algorithm_name: str,
    parameters: Parameters,
    algorithms: AlgorithmCollection = Depends(get_app_algorithms),
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
            errors=ErrMsgTmpl.ALGORITHM_NOT_EXISTS.format(algorithm_name),
            result=None,
        )
    params = parameters.get_params_to_execute()
    try:
        results = algorithms.get_algorithm_result(algorithm_name, params)
        outputs = []
        for name, value in results.items():
            outputs.append(Data(name=name, value=value))
        return AnswerOutputs(result=Outputs(outputs=outputs), errors=None)
    except TimeoutError:
        logger.warning(ErrMsg.TIME_OVER_MSG)
        return AnswerOutputs(result=None, errors=ErrMsg.TIME_OVER_MSG)
    except Exception as error:
        logger.warning(str(error))
        return AnswerOutputs(result=None, errors=str(error))
