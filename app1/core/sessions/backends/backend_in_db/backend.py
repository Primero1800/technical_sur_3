from typing import Dict, Generic

from fastapi_sessions.backends.session_backend import (
    BackendError,
    SessionBackend,
    SessionModel,
)
from fastapi_sessions.frontends.session_frontend import ID
from sqlalchemy.ext.asyncio import AsyncSession

from app1.exceptions import CustomException
from . import crud


class InDBBackend(Generic[ID, SessionModel], SessionBackend[ID, SessionModel]):
    """Stores session data in a dictionary."""

    def __init__(self) -> None:
        self.crud = crud
        # self.data: Dict[ID, SessionModel] = {}

    async def create(self, session_id: ID, data: SessionModel):
        """Create a new session entry."""
        if await self.crud.get(session_id):
            raise BackendError("create can't overwrite an existing session")

        result = await self.crud.create(session_id, data)
        return result.to_dict()

    async def read(self, session_id: ID):
        """Read an existing session data."""
        data = await self.crud.get(session_id)
        if not data:
            return

        return data.to_dict()


    #TODO
    # async def update(self, session_id: ID, data: SessionModel) -> None:
    #     """Update an existing session."""
    #     if self.data.get(session_id):
    #         self.data[session_id] = data
    #     else:
    #         raise BackendError("session does not exist, cannot update")

    async def delete(self, session_id: ID) -> None:
        """Delete an existing session"""
        await self.crud.delete(session_id)
