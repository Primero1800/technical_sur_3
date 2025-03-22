import json
from celery.result import AsyncResult
from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends

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
    print(filter_dict)

    op_dict, val_dict = {}, {}
    for key, value in filter_dict.items():
        key_splitted = key.split('__')
        field = key_splitted[0]
        condition = key_splitted[-1]
        operation = TaskFilter.operation(condition)
        print(field, condition, operation)
        if operation:
            op_dict[field] = operation
            val_dict[field] = value

    print(op_dict)
    print()


    for task_key in keys:
        model: TaskRead = await from_raw_result_to_model(json.loads(app_celery.backend.client.get(task_key)))

        model_dict = model.model_dump()

        match = True
        for key, func in op_dict.items():
            if key in model_dict:
                print('FOUND ', key)
                print('x=', model_dict[key], 'y=', val_dict[key], func)
                if (not model_dict[key] and key != 'returned_value') or not func(model_dict[key], val_dict[key]):
                    match = False
                    print('breaked')
                    break
        if match:
            result.append(model)

    return sorted(result, key=lambda x: x.date_done, reverse=True)
