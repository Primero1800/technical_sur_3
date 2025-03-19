from functools import wraps
from typing import Callable, Any

from prometheus_async.aio import count_exceptions, time
from prometheus_client import Counter, Histogram

EXECUTION_TIME = Histogram(
    "task_execution_seconds",
    "Task execution time",
    labelnames=["task_name"],  # чтобы в метриках видеть название фоновой задачи
)
TASKS_FAILED = Counter(
    "tasks_failed",
    "Tasks failed",
    labelnames=["task_name"],  # чтобы в метриках видеть название фоновой задачи
)


# декоратор для удобного сбора метрик
def export_task_metrics(func: Callable) -> Callable:
    task_name = func.__name__

    @count_exceptions(TASKS_FAILED.labels(task_name=task_name))  # подсчет количества ошибок
    @time(EXECUTION_TIME.labels(task_name=task_name))  # подсчет времени выполнения
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper
