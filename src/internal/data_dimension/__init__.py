"""Классы пакета описывают тип и размерность для входных и выходных данных
алгоритмов, представляет возможность проверки данных на на соответствие
указанным типу и размерности."""

from .data_shape_enum import DataShapeEnum
from .data_type_enum import DataTypeEnum

__all__ = ["DataShapeEnum", "DataTypeEnum"]
