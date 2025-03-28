import logging
from typing import Callable, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette import status

from app1.core.settings import settings
from app1.core import errors


class AppConfigurer:
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.logging.LOGGING_FORMAT,
    )

    @staticmethod
    def create_app(docs_url, redoc_url, lifespan) -> FastAPI:
        app = FastAPI(
            default_response_class=ORJSONResponse,
            lifespan=lifespan,
            docs_url=docs_url,
            redoc_url=redoc_url,
        )
        return app

    @staticmethod
    def get_custom_openapi(subject: FastAPI) -> Callable[[], Dict[str, Any]]:
        def custom_openapi() -> Dict[str, Any]:
            if subject.openapi_schema:
                return subject.openapi_schema
            openapi_schema = get_openapi(
                title=settings.app.APP_TITLE,
                version=settings.app.APP_VERSION,
                description=settings.app.APP_DESCRIPTION,
                routes=subject.routes,
                webhooks=subject.webhooks,
            )
            subject.openapi_schema = openapi_schema
            return subject.openapi_schema

        return custom_openapi

    # TODO
    @staticmethod
    def config_validation_exception_handler(app: FastAPI):
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
        async def validation_exception_handler_constraints(request, exc: IntegrityError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{errors.get_message(exc)} - HHHHHHHHHHHHHHHHHHHHAAAAAAAAAAAAAANNNNNNNNNNNNDDDDDDDDDDLLLLLLLLLEEEEEEEEER",
            )

        # @app.exception_handler(errors.Missing)
        # async def missing_exception_handler(request, exc: errors.Missing):
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=exc.msg
        #     )
