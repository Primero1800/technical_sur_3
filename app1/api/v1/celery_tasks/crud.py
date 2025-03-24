import json
from typing import Any

from .filters import TaskFilter
from .schemas import (
    TaskRead,
    from_raw_result_to_model,
)


async def get_all_tasks(
    task_filter: TaskFilter,
    backend_client: Any | None,
):
    result = []
    if not backend_client:
        return result

    keys = backend_client.keys('celery-task-meta-*')

    filter_dict = task_filter.model_dump(exclude_none=True, exclude_unset=True)
    op_dict = TaskFilter.get_dicts_to_filter(filter_dict)

    for task_key in keys:
        model: TaskRead = await from_raw_result_to_model(json.loads(backend_client.get(task_key)))
        model_dict = model.model_dump()

        if TaskFilter.is_matches(
                model_dict=model_dict,
                op_dict=op_dict,
        ):
            result.append(model)

    return sorted(result, key=lambda x: x.date_done, reverse=True)
