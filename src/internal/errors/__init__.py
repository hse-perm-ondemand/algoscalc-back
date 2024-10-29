"""В пакете представлены классы для обработки ошибок."""

from .error_message_enum import ErrorMessageEnum
from .error_message_template_enum import ErrorMessageTemplateEnum
from .exceptions import (
    AlgorithmError,
    AlgorithmValueError,
    AlgorithmTypeError,
    AlgorithmTimeoutError,
    AlgorithmRuntimeError,
    AlgorithmNotFoundError,
    AlgorithmUnexpectedError,
)

__all__ = [
    "ErrorMessageEnum",
    "ErrorMessageTemplateEnum",
    "AlgorithmError",
    "AlgorithmValueError",
    "AlgorithmTypeError",
    "AlgorithmTimeoutError",
    "AlgorithmRuntimeError",
    "AlgorithmNotFoundError",
    "AlgorithmUnexpectedError",
]
