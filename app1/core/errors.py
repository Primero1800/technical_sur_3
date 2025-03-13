from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status


class Missing(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class Duplicate(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class Validation(Exception):
    def __init__(self, msg: str):
        self.msg = msg


def get_message(instance):
    msg = str(instance.orig)
    return msg.split('DETAIL:')[-1].strip() if 'DETAIL' in msg else str(instance)


async def staff_only_403_exception(detail: str | None = None):
    detail = "Staff only allowed" or detail
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail
    )
