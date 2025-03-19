import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
from starlette import status
from prometheus_fastapi_instrumentator import Instrumentator

from app1.core.config import (
    AppConfigurer, SwaggerConfigurer, DBConfigurer
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
AppConfigurer.config_validation_exception_handler(app)

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
    from app1.scripts.mail_sender import send_mail

    await send_mail(schema=req, background_tasks=tasks)
    return {
        "status": status.HTTP_200_OK,
        "detail": "Message has been successfully scheduled"
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