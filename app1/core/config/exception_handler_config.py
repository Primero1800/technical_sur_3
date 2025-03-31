import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, DatabaseError

from app1.core import errors
from app1.exceptions import CustomException


logger = logging.getLogger(__name__)


class ExceptionHandlerConfigurer:
    # TODO
    @staticmethod
    def config_exception_handler(app: FastAPI):
        @app.exception_handler(ValidationError)
        async def validation_error_exception_handler(request, exc: ValidationError):
            exc_argument = exc.errors() if hasattr(exc, "errors") else exc
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Handled by ExceptionHandler",
                    "detail": jsonable_encoder(exc_argument)
                }
            )

        # @app.exception_handler(RequestValidationError)
        # async def validation_exception_handler(request, exc: RequestValidationError):
        #     raise HTTPException(
        #         status_code=settings.app.APP_422_CODE_STATUS,
        #         detail=exc.body,
        #     )

        @app.exception_handler(IntegrityError)
        async def integrity_error_exception_handler(request, exc: IntegrityError):
            logger.error("Handled by ExceptionHandler", exc_info=exc)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{errors.get_message(exc)} - HHHHHHHHHHHHHHHHHHHHAAAAAAAAAAAAAANNNNNNNNNNNNDDDDDDDDDDLLLLLLLLLEEEEEEEEER",
            )

        @app.exception_handler(CustomException)
        async def integrity_error_exception_handler(request, exc: CustomException):
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
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
