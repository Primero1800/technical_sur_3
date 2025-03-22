from datetime import datetime
from enum import Enum
from typing import Optional

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
        populate_by_name = True           # разрешить заполнять поля по их именам

    @staticmethod
    def operation(operation_id):
        if operation_id in _operations:
            return _operations[operation_id]
        return None

    @staticmethod
    def get_dicts_to_filter(filter_dict: dict):
        op_dict, val_dict = {}, {}
        for key, value in filter_dict.items():
            key_splitted = key.split('__')
            field = key_splitted[0]
            condition = key_splitted[-1]
            operation = TaskFilter.operation(condition)
            if operation:
                op_dict[field] = operation
                val_dict[field] = value
        return op_dict, val_dict

    @staticmethod
    def is_matches(model_dict: dict, op_dict: dict, val_dict: dict):
        for key, func in op_dict.items():
            if key in model_dict:
                if key == "date_done":
                    print('DATE_DONE_FOUND ', model_dict[key])
                    from app1.scripts.time_converter import convert_naive_time_to_aware
                    val_dict[key] = convert_naive_time_to_aware(val_dict[key])
                if (not model_dict[key] and key != 'returned_value') or not func(model_dict[key], val_dict[key]):
                    return False
        return True


