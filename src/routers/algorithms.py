import logging
import math

from fastapi import APIRouter, Body, Depends, Path, Request

from src.internal.algorithm_collection import AlgorithmCollection
from src.internal.constants import ALGORITHMS_ENDPOINT
from src.internal.schemas.algorithm_definition_schema import AlgorithmDefinitionSchema
from src.internal.schemas.data_element_schema import DataElementsSchema
from src.routers.schemas import AlgorithmsPageSchema, PaginateInputSchema


def get_app_algorithms(request: Request) -> AlgorithmCollection:
    return request.app.state.algorithms


router = APIRouter(
    prefix=ALGORITHMS_ENDPOINT,
)
logger = logging.getLogger(__name__)


@router.get(
    "/",
    response_model=AlgorithmsPageSchema,
    summary="Получить алгоритмы",
    description="Возвращает список имеющихся алгоритмов с постраничным выводом.",
    response_description="Список алгоритмов с информацией о постраничном выводе.",
)
async def get_algorithms(
    paginate: PaginateInputSchema = Depends(),
    algorithms: AlgorithmCollection = Depends(get_app_algorithms),
) -> AlgorithmsPageSchema:
    offset_min = (paginate.page - 1) * paginate.size
    offset_max = paginate.page * paginate.size
    algorithm_list = algorithms.get_algorithm_list()

    return AlgorithmsPageSchema(
        items=algorithm_list[offset_min:offset_max],
        total=len(algorithm_list),
        page=paginate.page,
        size=paginate.size,
        pages=math.ceil(len(algorithm_list) / paginate.size),
    )


@router.get(
    "/{algorithm_name}",
    response_model=AlgorithmDefinitionSchema,
    summary="Получить описание алгоритма",
    description="Возвращает информацию об алгоритме по его названию.",
    response_description="Информация об алгоритме.",
)
async def get_algorithm(
    algorithm_name: str = Path(..., description="Название алгоритма"),
    algorithms: AlgorithmCollection = Depends(get_app_algorithms),
) -> AlgorithmDefinitionSchema:
    return algorithms.get_algorithm_definition(algorithm_name)


@router.post(
    "/{algorithm_name}/results",
    response_model=DataElementsSchema,
    summary="Получить результат выполнения алгоритма",
    description="Возвращает результат выполнения выбранного алгоритма.",
    response_description="Результаты выполнения алгоритма.",
)
async def get_algorithm_result(
    parameters: DataElementsSchema = Body(
        ..., description="Значения параметров для выполнения алгоритма"
    ),
    algorithm_name: str = Path(..., description="Название алгоритма"),
    algorithms: AlgorithmCollection = Depends(get_app_algorithms),
) -> DataElementsSchema:
    return algorithms.get_algorithm_result(algorithm_name, parameters)
