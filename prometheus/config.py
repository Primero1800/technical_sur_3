from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


def add_metrics_root(
        app: FastAPI,
        tags: list[str],
        endpoint: str = "/metrics",
        include_in_schema: bool = True
):
    Instrumentator().instrument(app).expose(
        app=app, endpoint=endpoint, tags=tags,
        include_in_schema=include_in_schema
    )
