import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, DatabaseError

from app1.core import errors
from app1.core.settings import settings
from app1.exceptions import CustomException


logger = logging.getLogger(__name__)


class ExceptionHandlerConfigurer:

    simple_exceptions = [
        ValidationError,
        RequestValidationError,
    ]

    @staticmethod
    def add_simple_exception_handler(exc_class, app:FastAPI):
        @app.exception_handler(exc_class)
        async def simple_exception_handler(request, exc: exc_class):
            exc_argument = exc.errors() if hasattr(exc, "errors") else exc
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Handled by ExceptionHandler",
                    "detail": jsonable_encoder(exc_argument)
                }
            )

    # TODO
    @staticmethod
    def config_exception_handler(app: FastAPI):

        for simple_exception in ExceptionHandlerConfigurer.simple_exceptions:
            ExceptionHandlerConfigurer.add_simple_exception_handler(
                exc_class=simple_exception,
                app=app
            )

        @app.exception_handler(IntegrityError)
        async def integrity_error_exception_handler(request, exc: IntegrityError):
            logger.error("Handled by ExceptionHandler", exc_info=exc)
            return ORJSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": "Handled by ExceptionHandler",
                    "detail": f"Error while operation with database",
                }
            )

        @app.exception_handler(CustomException)
        async def integrity_error_exception_handler(request, exc: CustomException):
            return ORJSONResponse(
                status_code=exc.status_code,
                content={
                    "message": "Handled by ExceptionHandler",
                    "detail": f"{exc.msg} (catched by exception_handler)",
                }
            )

        @app.exception_handler(DatabaseError)
        async def database_error_handler(request, exc: DatabaseError):
            logger.error("Handled by ExceptionHandler", exc_info=exc)
            return ORJSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": "Handled by ExceptionHandler",
                    "detail": "Unexpected error occurred."
                }
            )
