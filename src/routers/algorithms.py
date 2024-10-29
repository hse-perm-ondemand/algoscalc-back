import logging

from fastapi import APIRouter, Depends, Request

from src.internal.algorithm_collection import AlgorithmCollection
from src.internal.constants import ALGORITHMS_ENDPOINT
from src.internal.schemas.algorithm_definition_schema import AlgorithmDefinitionSchema
from src.internal.schemas.data_element_schema import DataElementSchema
from src.internal.schemas.definition_schema import DefinitionSchema


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
    :rtype: list[DefinitionSchema]
    """
    return algorithms.get_algorithm_list()


@router.get("/{algorithm_name}")
async def get_algorithm(
    algorithm_name: str, algorithms: AlgorithmCollection = Depends(get_app_algorithms)
) -> AlgorithmDefinitionSchema:
    """Возвращает описание выбранного алгоритма.

    :param algorithm_name: имя алгоритма;
    :type algorithm_name: str
    :return: Описание алгоритма.
    :rtype: AlgorithmDefinitionSchema
    """
    return algorithms.get_algorithm_definition(algorithm_name)


@router.post("/{algorithm_name}/results")
async def get_algorithm_result(
    algorithm_name: str,
    parameters: list[DataElementSchema],
    algorithms: AlgorithmCollection = Depends(get_app_algorithms),
) -> list[DataElementSchema]:
    """Возвращает результат выполнения выбранного алгоритма.

    :param algorithm_name: имя алгоритма;
    :type algorithm_name: str
    :param parameters: значения входных данных для выполнения алгоритма.
    :type parameters: list[DataElementSchema]
    :return: результаты выполнения выбранного алгоритма
    :rtype: list[DataElementSchema]
    """
    return algorithms.get_algorithm_result(algorithm_name, parameters)
