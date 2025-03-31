from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app1.core import errors
from app1.exceptions import CustomException


class ExceptionHandlerConfigurer:
    # TODO
    @staticmethod
    def config_exception_handler(app: FastAPI):
        @app.exception_handler(ValidationError)
        async def validation_error_exception_handler(request, exc: ValidationError):
            exc_argument = exc.errors() if hasattr(exc, "errors") else exc
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=jsonable_encoder(exc_argument)
            )

        # @app.exception_handler(RequestValidationError)
        # async def validation_exception_handler(request, exc: RequestValidationError):
        #     raise HTTPException(
        #         status_code=settings.app.APP_422_CODE_STATUS,
        #         detail=exc.body,
        #     )

        @app.exception_handler(IntegrityError)
        async def integrity_error_exception_handler(request, exc: IntegrityError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{errors.get_message(exc)} - HHHHHHHHHHHHHHHHHHHHAAAAAAAAAAAAAANNNNNNNNNNNNDDDDDDDDDDLLLLLLLLLEEEEEEEEER",
            )

        @app.exception_handler(CustomException)
        async def integrity_error_exception_handler(request, exc: CustomException):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{exc.msg} (catched by exception_handler)",
            )

        # @app.exception_handler(errors.Missing)
        # async def missing_exception_handler(request, exc: errors.Missing):
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=exc.msg
        #     )
