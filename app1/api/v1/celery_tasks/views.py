import json
from celery.result import AsyncResult
from fastapi import APIRouter

from celery_home.config import app_celery
from .schemas import (
    from_raw_result_to_model,
    async_result_to_dict,
    TaskRead
)


router = APIRouter()


@router.get("/test", )
async def test_celery():
    from app1.api.v1.celery_tasks.tasks import test_celery
    test_celery.apply_async()


@router.get("/tasks/{task_id}", )
async def get_status(task_id) -> TaskRead | dict:
    task_result: AsyncResult = AsyncResult(task_id, backend=app_celery.backend)
    model: TaskRead = await from_raw_result_to_model(async_result_to_dict(task_result))
    return model


@router.get("/tasks", )
async def get_statuses() -> list[TaskRead]:

    keys = app_celery.backend.client.keys('celery-task-meta-*')
    result = []
    for key in keys:
        model: TaskRead = await from_raw_result_to_model(json.loads(app_celery.backend.client.get(key)))
        result.append(model)
    return sorted(result, key=lambda x: x.date_done, reverse=True)
