from datetime import datetime, timedelta

import pytz
from fastapi.encoders import jsonable_encoder
from fastapi_sessions.backends.session_backend import SessionModel
from fastapi_sessions.frontends.session_frontend import ID

from app1.core.config import DBConfigurer
from app1.core.models import Session
from app1.core.sessions.utils import jwt_encode
from app1.core.settings import settings


async def get(
    session_id: ID
) -> Session:
    async with DBConfigurer.Session() as session:
        orm_model: Session = await session.get(Session, session_id)
        return orm_model


async def create(
    session_id: ID,
    data: SessionModel
):

    data_dict = data.model_dump()
    data_dict['data'] = jwt_encode(
        payload=jsonable_encoder(data_dict['data'])
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
        session.add(orm_model)
        await session.commit()
        await session.refresh(orm_model)
        return orm_model


async def delete(
    session_id: ID
):
    orm_model: Session = await get(session_id)

    async with DBConfigurer.Session() as session:
        session.delete(orm_model)
        await session.commit()

