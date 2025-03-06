import uvicorn
from app1.core.config import AppConfigurer, SwaggerConfigurer
from app1.core.settings import settings

from app1.api import router as router_v1

app = AppConfigurer.create_app(
    docs_url=None,
    redoc_url=None,
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
    return "top here"


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
        app=settings.run.app1.app,
        host=settings.run.app1.host,
        port=settings.run.app1.port,
        reload=settings.run.app1.reload,
    )