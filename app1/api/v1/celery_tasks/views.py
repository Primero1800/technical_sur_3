import json
from typing import Optional

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, Query

from celery_home.config import app_celery
from .filters import TaskFilter
from . import crud
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
async def get_statuses(
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0),
    sort_by: Optional[str] = None,
    task_filter: TaskFilter = Depends(TaskFilter),
) -> list[TaskRead]:

    result_full = await crud.get_all_tasks(
        task_filter=task_filter,
        backend_client=app_celery.backend.client
    )

    from app1.scripts.pagination import paginate_result
    return await paginate_result(
        query_list=result_full,
        page=page,
        size=size,
        sort_by=sort_by,
    )




