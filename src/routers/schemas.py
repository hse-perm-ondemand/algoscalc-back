from pydantic import BaseModel, Field

from src.internal.schemas.definition_schema import DefinitionSchema


class AlgorithmsPageSchema(BaseModel):
    """Класс для постраничного вывода объектов."""

    items: list[DefinitionSchema] = Field(..., description="Список объектов на текущей странице")
    total: int = Field(..., description="Общее количество объектов")
    page: int = Field(..., description="Номер текущей страницы")
    size: int = Field(..., description="Максимальное количество объектов на странице")
    pages: int = Field(..., description="Общее количество страниц")

class PaginateInputSchema(BaseModel):
    """Класс для параметров постраничного вывода данных."""
    page: int = Field(1, ge=1, description="Номер страницы, должен быть больше или равен 1")
    size: int = Field(50, ge=1, le=100, description="Количество объектов на странице, должно быть от 1 до 100")
