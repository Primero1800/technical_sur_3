import logging
from datetime import datetime, timedelta
from sqlite3 import IntegrityError
from typing import List, Sequence

import pytz
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi_sessions.backends.session_backend import SessionModel
from fastapi_sessions.frontends.session_frontend import ID
from sqlalchemy import select, Result

from app1.core.config import DBConfigurer
from app1.core.models import Session
from app1.core.sessions.utils import jwt_encode, jwt_decode
from app1.core.settings import settings
from app1.exceptions import CustomException
from app1.scripts.convert_dates_back import convert_dates


CLASS = "Session"
CLASS_ = "session"


logger = logging.getLogger(__name__)


async def get(
    session_id: ID
) -> Session | None:
    async with DBConfigurer.Session() as session:
        orm_model: Session = await session.get(Session, session_id)
        return orm_model


async def get_all_raw() -> List[Session] | Sequence[Session]:
    async with DBConfigurer.Session() as session:
        stmt = select(Session).order_by(Session.expired_at)
        result: Result = await session.execute(stmt)
        orm_models = result.scalars().all()
        return orm_models


async def get_all() -> list:
    orm_models = await get_all_raw()
    result = []
    for orm_model in orm_models:
        try:
            data = await decode_data_to_dict(orm_model)
            result.append(data)
        except CustomException:
            raise
    return result




async def create(
    session_id: ID,
    data: SessionModel
):
    data_dict = data.model_dump()
    try:
        data_dict['data'] = jwt_encode(
            payload=jsonable_encoder(data_dict['data'])
        )
    except Exception as exc:
        logger.error('Error while encoding session data to token to store in database Session', exc_info=exc)
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="Error while encoding session data to token to store in database Session"
        )

    orm_model: Session = Session(
        session_id=session_id,
        expired_at=datetime.now(
            tz=pytz.timezone(settings.app.APP_TIMEZONE)
        ) + timedelta(
            seconds=settings.sessions.SESSIONS_MAX_AGE
        ),
        **data_dict
    )
    async with DBConfigurer.Session() as session:
        try:
            session.add(orm_model)
            await session.commit()
            await session.refresh(orm_model)
        except IntegrityError as exc:
            logger.error("Error while storing orm_model Session to database", exc_info=exc)
            raise CustomException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg=f"Error while storing orm_model Session to database"
            )
        return orm_model


async def update(
    session_id: ID,
    data: SessionModel,
):
    data_dict = data.model_dump() if not isinstance(data, dict) else data

    try:
        data_dict['data'] = jwt_encode(
            payload=jsonable_encoder(data_dict['data'])
        )
    except Exception as exc:
        logger.error("Error while encoding data to token from dict for Session", exc_info=exc)
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="Error while encoding data to token from dict for Session",
        )

    async with DBConfigurer.Session() as session:

        orm_model: Session = await session.get(Session, session_id)
        if not orm_model:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                msg=f"{CLASS} with session_id={session_id} not found"
            )

        for key, val in data_dict.items():
            setattr(orm_model, key, val)
        orm_model.expired_at = datetime.now(
                tz=pytz.timezone(settings.app.APP_TIMEZONE)
            ) + timedelta(
                seconds=settings.sessions.SESSIONS_MAX_AGE
            )

        logger.warning(f"Editing {orm_model!r} in database")
        try:
            await session.commit()
            await session.refresh(orm_model)
        except IntegrityError as exc:
            logger.error(f"Error while editing orm_model Session in database", exc_info=exc)
            raise CustomException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg=f"Error while editing orm_model Session in database"
            )


async def delete(
    session_id: ID
):
    orm_model: Session = await get(session_id)
    if not orm_model:
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            msg=f"{CLASS} with session_id={session_id} not found"
        )
    async with DBConfigurer.Session() as session:
        await session.delete(orm_model)
        await session.commit()


async def decode_data_to_dict(
    data: dict | Session,
) -> dict:

    if isinstance(data, Session):
        data = data.to_dict()
    try:
        data['data'] = jwt_decode(
            token_cred=data['data'],
        )
        convert_dates(data['data'])
    except Exception as exc:
        logger.error("Error while decoding data to dict", exc_info=exc)
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="Error while decoding data to dict",
        )
    return data

