import json

import uvicorn
import redis

from contextlib import asynccontextmanager

from celery.result import AsyncResult
from fastapi import FastAPI, BackgroundTasks
from starlette import status
from starlette.responses import JSONResponse

from app1.celery_tasks.schemas import (
    TaskRead,
    from_raw_result_to_model,
    async_result_to_dict,
)
from app1.core.config import (
    AppConfigurer, SwaggerConfigurer, DBConfigurer
)
from app1.core.settings import settings
from app1.api import (
    router as router_api,
    webhooks_router,
)

from app1.scripts.scrypt_schemas.email import CustomMessageSchema
from celery_home.config import app_celery
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
    from app1.scripts.mail_sender.utils import send_mail

    await send_mail(schema=req, background_tasks=tasks)
    return {
        "status": status.HTTP_200_OK,
        "detail": "Message has been successfully scheduled"
    }


@app.get("/celery-test/", tags=[settings.tags.TECH_TAG,],)
@app.get("/celery-test", tags=[settings.tags.TECH_TAG,], include_in_schema=False,)
async def test_celery():
    from app1.celery_tasks.tasks import test_celery
    test_celery.apply_async()


@app.get("/celery/{task_id}/", tags=[settings.tags.TECH_TAG,],)
@app.get("/celery/{task_id}", tags=[settings.tags.TECH_TAG,], include_in_schema=False,)
async def get_status(task_id) -> TaskRead | dict:

    task_result: AsyncResult = AsyncResult(task_id, backend=app_celery.backend)
    # print('STTTTTTTTTTTTTTART ', task_result.result)
    # model: TaskRead = await from_raw_result_to_model(task_result.__dict__)
    model: TaskRead = await from_raw_result_to_model(async_result_to_dict(task_result))
    return model


@app.get("/celery/", tags=[settings.tags.TECH_TAG,],)
@app.get("/celery", tags=[settings.tags.TECH_TAG,], include_in_schema=False,)
async def get_statuses() -> list[TaskRead]:

    keys = app_celery.backend.client.keys('celery-task-meta-*')

    print('KEYS ', keys)

    result = []
    for key in keys:
        print()
        print(json.loads(app_celery.backend.client.get(key)))
                    # {
                    # 'status': 'SUCCESS',
                    #  'result': {
                    #           'meta': {'app_name': '3_sur_app1', 'task_name': 'task_test_celery'}, 'return': [12, True]
                    #           },
                    #  'traceback': None, 'children': [],
                    #  'date_done': '2025-03-21T14:08:54.084711+00:00',
                    #  'task_id': '468f313a-ab06-4df5-953c-03806ddcc001'
                    #  }
        print()
        model: TaskRead = await from_raw_result_to_model(json.loads(app_celery.backend.client.get(key)))
        result.append(model)

    return result


if __name__ == "__main__":
    # gunicorn app1.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
    # uvicorn app1.main:app --host 0.0.0.0 --reload
    uvicorn.run(
        app=settings.run.app1.APP_PATH,
        host=settings.run.app1.APP_HOST,
        port=8080,                                 # original 8000 used in uvicorn server, started from system bash
        reload=settings.run.app1.APP_RELOAD,
    )