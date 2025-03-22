import json
from celery.result import AsyncResult
from fastapi import APIRouter, Depends

from celery_home.config import app_celery
from .filters import TaskFilter
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
async def get_statuses(task_filter: TaskFilter = Depends(TaskFilter)) -> list[TaskRead]:

    keys = app_celery.backend.client.keys('celery-task-meta-*')

    result = []
    filter_dict = task_filter.model_dump(exclude_none=True, exclude_unset=True)
    op_dict, val_dict = TaskFilter.get_dicts_to_filter(filter_dict)

    for task_key in keys:
        model: TaskRead = await from_raw_result_to_model(json.loads(app_celery.backend.client.get(task_key)))
        model_dict = model.model_dump()

        if TaskFilter.is_matches(
            model_dict=model_dict,
            op_dict=op_dict,
            val_dict=val_dict,
        ):
            result.append(model)

    return sorted(result, key=lambda x: x.date_done, reverse=True)
