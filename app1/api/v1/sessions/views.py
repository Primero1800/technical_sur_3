import logging
from datetime import datetime
from typing import Any, Dict
from uuid import uuid4, UUID

import pytz
from fastapi import APIRouter, Response, Depends, status

from app1.core.auth.fastapi_users_config import current_user_or_none
from app1.core.sessions import fastapi_session_config as fs


logger = logging.getLogger(__name__)


router = APIRouter()


@router.post(
    "/create_session",
)
async def create_session(
    response: Response,
    user: Any = Depends(current_user_or_none),
):

    user_session_uuid = uuid4()

    data = fs.SessionData(
        user_id=user.id if user else None,
        user_email=user.email if user else None,
        data={
            "day": "monday",
            "time": datetime.now(tz=pytz.timezone("Europe/Moscow"))
    })

    await fs.backend.create(user_session_uuid, data)
    fs.cookie.attach_to_response(response, user_session_uuid)

    username = user.email if user and hasattr(user, "email") else "Anonimous"
    response.status_code = status.HTTP_200_OK
    return {
        "user": username,
        "response": {
            "headers": response.headers,
            "status": response.status_code,
        }
    }


@router.get(
    "/whoami",
    dependencies=[Depends(fs.cookie)],
    response_model=fs.SessionData,
)
async def whoami(
    session_data: fs.SessionData = Depends(fs.verifier),
):
    decoded_session_data = await fs.backend.normalize_data_from_db(session_data)
    return decoded_session_data


@router.post(
    "/delete_session",
)
async def del_session(
    response: Response,
    session_id: UUID = Depends(fs.cookie),
):
    await fs.backend.delete(session_id)
    fs.cookie.delete_from_response(response)
    return "deleted session"


@router.post(
    "/update_session",
    dependencies=[Depends(fs.cookie)]
)
async def update_session(
    data: Dict[str, Any],
    session_id: UUID = Depends(fs.cookie),
    session_data: fs.SessionData = Depends(fs.verifier)
):

    session_data.data.update(data)
    await fs.backend.update(session_id, session_data)

    return "session updated"


@router.post(
    "/clear_session",
    dependencies=[Depends(fs.cookie)]
)
async def update_session(
        session_id: UUID = Depends(fs.cookie),
        session_data: fs.SessionData = Depends(fs.verifier)
):
    session_data.data.clear()
    await fs.backend.update(session_id, session_data)

    return "session cleared"
