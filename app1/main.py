from json import JSONDecodeError

import pytz
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks, Request, Response, Body
from fastapi.responses import ORJSONResponse
from pydantic import Json
from starlette import status
from starlette.datastructures import Headers
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse
from starlette.types import Scope, Receive, Send, ASGIApp

from app1.core.config import (
    AppConfigurer,
    SwaggerConfigurer,
    DBConfigurer,
    ExceptionHandlerConfigurer,
)
from app1.core.settings import settings
from app1.api import (
    router as router_api,
    webhooks_router,
)

from app1.scripts.scrypt_schemas.email import CustomMessageSchema
from prometheus.config import add_metrics_root


# Initialization


@asynccontextmanager
async def lifespan(application: FastAPI):
    # startup
    yield
    # shutdown
    await DBConfigurer.dispose()


app = AppConfigurer.create_app(
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

app.openapi = AppConfigurer.get_custom_openapi(app)


# Timezone

moscow_tz = pytz.timezone(settings.app.APP_TIMEZONE)


# ROUTERS

app.include_router(
    router_api,
    prefix=settings.app.API_PREFIX,
)
app.webhooks = webhooks_router.routes

SwaggerConfigurer.config_swagger(app, settings.app.APP_TITLE)


# /metrics
add_metrics_root(
    app=app,
    tags=[settings.tags.TECH_TAG,],
)

######################################################################

SwaggerConfigurer.delete_router_tag(app)

# uncomment, if need custom exception_handler
ExceptionHandlerConfigurer.config_exception_handler(app)

# ROUTES


@app.get("/", tags=[settings.tags.ROOT_TAG,],)
@app.get("", tags=[settings.tags.ROOT_TAG,], include_in_schema=False,)
def top():
    return f"top here test {settings.auth.TRANSPORT_TOKEN_URL}"


@app.get("/echo/{thing}/", tags=[settings.tags.TECH_TAG,],)
@app.get("/echo/{thing}", tags=[settings.tags.TECH_TAG,], include_in_schema=False,)
def echo(thing):
    return " ".join([thing for _ in range(3)])


@app.get("/routes/", tags=[settings.tags.TECH_TAG,],)
@app.get("/routes",  tags=[settings.tags.TECH_TAG,], include_in_schema=False,)
async def get_routes_endpoint():
    return await SwaggerConfigurer.get_routes(
        application=app,
    )


@app.post("/test-mailer/", tags=[settings.tags.TECH_TAG,],)
@app.post("/test-mailer",  tags=[settings.tags.TECH_TAG,], include_in_schema=False,)
async def test_mailer(
        req: CustomMessageSchema, tasks: BackgroundTasks
):
    from app1.scripts.mail_sender.utils import send_mail

    await send_mail(schema=req, background_tasks=tasks)
    return {
        "status": status.HTTP_200_OK,
        "detail": "Message has been successfully scheduled"
    }


# TEMPORARY FRAGMENT

from app1.core.sessions.views_temp import router as temp_router
app.include_router(
    temp_router,
    tags=[settings.tags.TECH_TAG,]
)


@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    request.headers._list.append(("x-custom-header11".encode(), "CustomHeaderValue11".encode()))
    response = await call_next(request)
    # response.headers["X-Custom-Header2"] = "CustomHeaderValue2"
    return response


@app.post("/request-response/", tags=[settings.tags.TECH_TAG,],)
@app.post("/request-response/", tags=[settings.tags.TECH_TAG,], include_in_schema=False,)
async def request_response(
        request: Request,
        response: Response,
):
    return {
        "request": dict(request.headers),  # преобразуем в dict для сериализации
        "response": {
            "headers": dict(response.headers),  # преобразуем в dict для сериализации
            "status_code": response.status_code,  # добавляем статус
        },
    }



if __name__ == "__main__":
    # gunicorn app1.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
    # uvicorn app1.main:app --host 0.0.0.0 --reload
    uvicorn.run(
        app=settings.run.app1.APP_PATH,
        host=settings.run.app1.APP_HOST,
        port=8080,                                 # original 8000 used in uvicorn server, started from system bash
        reload=settings.run.app1.APP_RELOAD,
    )