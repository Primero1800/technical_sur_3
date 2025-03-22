from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class TaskRead(BaseModel):
    id: str
    app_name: Optional[str]
    task_name: Optional[str]
    task_status: str
    returned_value: Optional[Any]
    args: Optional[tuple[Any, ...]]
    kwargs: Optional[dict[str, Any]]
    date_done: Optional[datetime]

    @property
    def result(self):
        return self.returned_value


async def from_raw_result_to_model(raw: dict) -> TaskRead:
    from app1.scripts.time_converter import convert_time
    local_time_str = convert_time(raw['date_done'])
    m_dict: dict[str, Any] = {
        'id': raw['task_id'],
        'task_status': raw['status'],
        'date_done': local_time_str,
    }
    m_app_name: str | None = None
    m_task_name: str | None = None
    m_returned_value: Any | None = None
    m_args: tuple | None = tuple()
    m_kwargs: dict[str, Any] = {}

    if 'result' in raw and isinstance(raw['result'], dict):
        cache_result = raw['result']
        if 'meta' in cache_result:
            if 'app_name' in cache_result['meta']:
                m_app_name = cache_result['meta']['app_name']
            if 'task_name' in cache_result['meta']:
                m_task_name = cache_result['meta']['task_name']
            if 'args' in cache_result['meta']:
                m_args = cache_result['meta']['args']
            if 'kwargs' in cache_result['meta']:
                m_kwargs = cache_result['meta']['kwargs']
        if 'returned_value' in raw['result']:
            m_returned_value = raw['result']['returned_value']

    return TaskRead(
        app_name=m_app_name,
        task_name=m_task_name,
        returned_value=m_returned_value,
        args=m_args,
        kwargs=m_kwargs,
        **m_dict,
    )


def async_result_to_dict(async_result):
    result_dict = {
        'task_id': async_result.id,
        'status': async_result.status,
        'result': async_result.result,
        'date_done': async_result.date_done,
        'traceback': async_result.traceback,
        'children': [async_result_to_dict(child) for child in async_result.children]
    }
    return result_dict
