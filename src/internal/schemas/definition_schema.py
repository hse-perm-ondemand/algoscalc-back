from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class DefinitionSchema(BaseModel):
    """Класс представляет описание объекта."""

    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    description: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
