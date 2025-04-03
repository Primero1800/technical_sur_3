from datetime import datetime, timedelta

import pytz
from fastapi.encoders import jsonable_encoder
from fastapi_sessions.backends.session_backend import SessionModel
from fastapi_sessions.frontends.session_frontend import ID

from app1.core.config import DBConfigurer
from app1.core.models import Session
from app1.core.sessions.utils import jwt_encode, jwt_decode
from app1.core.settings import settings
from app1.scripts.convert_dates_back import convert_dates


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
        await session.delete(orm_model)
        await session.commit()


async def decode_data_to_dict(
    data: dict | Session,
) -> dict:

    if isinstance(data, Session):
        data = data.to_dict()

    data['data'] = jwt_decode(
        token_cred=data['data'],
    )
    convert_dates(data['data'])
    return data

