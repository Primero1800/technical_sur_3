import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app1.core.config import (
    AppConfigurer, SwaggerConfigurer, DBConfigurer
)
from app1.core.settings import settings
from app1.api import router as router_v1

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
    router_v1,
    prefix=settings.app.API_V1_PREFIX,
)


SwaggerConfigurer.config_swagger(app, settings.app.APP_TITLE)

######################################################################

SwaggerConfigurer.delete_router_tag(app)
AppConfigurer.config_validation_exception_handler(app)

# ROUTES


@app.get("/", tags=[settings.tags.ROOT_TAG,],)
@app.get("", tags=[settings.tags.ROOT_TAG,], include_in_schema=False,)
def top():
    return f"top here test"


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


if __name__ == "__main__":
    # uvicorn app1.main:app --host 0.0.0.0 --reload
    uvicorn.run(
        app=settings.run.app1.app_path,
        host=settings.run.app1.app_host,
        port=settings.run.app1.app_port,
        reload=settings.run.app1.app_reload,
    )