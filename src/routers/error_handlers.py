from logging import Logger
from fastapi import FastAPI, HTTPException, Request

from src.internal.errors.exceptions import (
    AlgorithmError,
    AlgorithmNotFoundError,
    AlgorithmTypeError,
    AlgorithmValueError,
)
from src.internal.errors import ErrorMessageEnum as ErrMsg


def init_error_handlers(app: FastAPI, logger: Logger):
    @app.exception_handler(AlgorithmNotFoundError)
    def handle_not_found_error(request: Request, err: AlgorithmNotFoundError):
        raise HTTPException(
            status_code=404,
            detail=err.message,
        )

    @app.exception_handler(AlgorithmValueError)
    def handle_value_error(request: Request, err: AlgorithmValueError):
        raise HTTPException(
            status_code=400,
            detail=err.message,
        )

    @app.exception_handler(AlgorithmTypeError)
    def handle_type_error(request: Request, err: AlgorithmTypeError):
        raise HTTPException(
            status_code=400,
            detail=err.message,
        )

    @app.exception_handler(AlgorithmError)
    def handle_algorithm_error(request: Request, err: AlgorithmError):
        raise HTTPException(
            status_code=500,
            detail=err.message,
        )

    @app.exception_handler(Exception)
    def handle_unexpected_error(request: Request, err: Exception):
        if logger:
            logger.error(str(err))
        raise HTTPException(
            status_code=500,
            detail=ErrMsg.UNEXPECTED_ERROR,
        )
