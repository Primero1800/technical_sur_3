from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field, BaseModel


class StatusType(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PENDING = "PENDING"
    RETRY = "RETRY"
    STARTED = "STARTED"

_operations = {
    "neq": lambda x, y: x != y,
    "eq": lambda x, y: x == y,
    "gt": lambda x, y: x > y,
    "gte": lambda x, y: x >= y,
    "in": lambda x, y: x in y,
    "lt": lambda x, y: x < y,
    "lte": lambda x, y: x <= y,
    "not_in": lambda x, y: x not in y,
    "nin": lambda x, y: x not in y,
    "contains": lambda x, y: y in x,
    "isnull": lambda x, y: (y is False and x not in (None, False)) or (y is True and x in (None, False)),
}


class TaskFilter(BaseModel):

    task_name__contains: Optional[str] = Field(default=None)
    task_status__eq: Optional[StatusType] = Field(default=None)
    returned_value__isnull: Optional[bool] = Field(default=None)
    date_done__gte: Optional[datetime] = Field(default=None)

    # class Constants(Filter.Constants):
    #     model = Product

    class Config:
        allow_population_by_field_name = True           # разрешить заполнять поля по их именам

    @staticmethod
    def operation(operation_id):
        if operation_id in _operations:
            return _operations[operation_id]
        return None


