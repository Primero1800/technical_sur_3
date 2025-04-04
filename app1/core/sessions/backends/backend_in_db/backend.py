from typing import Generic

from fastapi_sessions.backends.session_backend import (
    BackendError,
    SessionBackend,
    SessionModel,
)
from fastapi_sessions.frontends.session_frontend import ID

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

        try:
            result = await self.crud.create(session_id, data)
        except CustomException:
            raise

        return result.to_dict()

    async def read(self, session_id: ID):
        """Read an existing session data."""
        data = await self.crud.get(session_id)
        if not data:
            return
        data = await self.crud.decode_data_to_dict(data)
        return DictWrapper(**data)

    async def update(self, session_id: ID, data: SessionModel) -> None:
        """Update an existing session."""
        try:
            await self.crud.update(session_id, data)
        except CustomException:
            raise

    async def delete(self, session_id: ID) -> None:
        """Delete an existing session"""
        try:
            await self.crud.delete(session_id)
        except CustomException:
            raise


class DictWrapper:
    def __init__(self, **kwargs):
        self._data = kwargs

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getattr__(self, item):
        if item in self._data:
            return self._data[item]
        raise AttributeError(f"'DictWrapper' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        if key == "_data":
            super().__setattr__(key, value)
        else:
            self._data[key] = value

    def __repr__(self):
        return repr(self._data)

    def items(self):
        return self._data.items()

    def model_dump(self):
        return self
