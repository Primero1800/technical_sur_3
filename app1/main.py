import json

import uvicorn
import redis

from contextlib import asynccontextmanager

from celery.result import AsyncResult
from fastapi import FastAPI, BackgroundTasks
from starlette import status
from starlette.responses import JSONResponse

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
def get_status(task_id):
    task_result: AsyncResult = AsyncResult(task_id, backend=app_celery.backend)
    # task_name = task_result.get('task_name') if task_result else None
    # print('TASK_NAME ', task_name)
    print('TTTTTTTTTTTTTTTTTTTTTT ', task_result.__dict__)
    print('TTTTTTTTTTTTTTTTTTTTTT ', task_result.name)
    print('TTTTTTTTTTTTTTTTTTTTTT ', task_result.worker)
    print('TTTTTTTTTTTTTTTTTTTTTT ', task_result.result)
    print('TTTTTTTTTTTTTTTTTTTTTT ', task_result.date_done)
    print('TTTTTTTTTTTTTTTTTTTTTT ', task_result.task_id)
    print('TTTTTTTTTTTTTTTTTTTTTT ', task_result.retries)
    print('TTTTTTTTTTTTTTTTTTTTTT ', task_result.info)
    print('TTTTTTTTTTTTTTTTTTTTTT ', task_result)
    result = {
        "task_id": task_id,
        'id': task_result.id,
        "task_status": task_result.status,
        "result": task_result.result,
        "args": task_result.args,
        "kwargs": task_result.kwargs,
        "retries": task_result.retries,
    }
    return JSONResponse(result)


@app.get("/celery/", tags=[settings.tags.TECH_TAG,],)
@app.get("/celery", tags=[settings.tags.TECH_TAG,], include_in_schema=False,)
def get_statuses():

    # keys = app_celery.backend.client.keys()
    keys = redis.StrictRedis(app_celery.conf.result_backend)
    print('KEYS ', keys)

    results = []
    for key in keys:
        value = app_celery.backend.client.get(key)
        print(111111111111111111, key, value, type(value))
        task = json.loads(value)
        print(222222222222222222, key, task, type(task))
        if 'result' in task and isinstance(task['result'], dict):
            print(task['result'])
            if task['result']['app_name'] == '3_sur_app1':
                results.append(task['result'])
        else:
            print("doesnt match ", task)

    return JSONResponse(content=results, status_code=200)


if __name__ == "__main__":
    # gunicorn app1.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
    # uvicorn app1.main:app --host 0.0.0.0 --reload
    uvicorn.run(
        app=settings.run.app1.APP_PATH,
        host=settings.run.app1.APP_HOST,
        port=8080,                                 # original 8000 used in uvicorn server, started from system bash
        reload=settings.run.app1.APP_RELOAD,
    )