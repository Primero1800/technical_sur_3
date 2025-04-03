from typing import Dict, Any, Annotated, Optional

from fastapi_sessions.frontends.implementations import (
    SessionCookie,
    CookieParameters,
)
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi import HTTPException

from uuid import UUID

from pydantic import BaseModel

from app1.core.settings import settings
from app1.core.sessions.backends import (
    InMemoryBackend,
    InDBBackend,
)


# SESSION DATA ################################

class SessionData(BaseModel):
    user_id: Annotated[Optional[int], None]
    user_email: Annotated[Optional[str], None]
    data: Annotated[Dict[str, Any], {}]


# SESSION FRONTEND ############################

class CustomCookieParameters(CookieParameters):
    max_age: int = settings.sessions.SESSIONS_MAX_AGE


cookie_params = CustomCookieParameters()


# Uses UUID
cookie = SessionCookie(
    cookie_name="x-session-id",
    identifier="general_verifier",
    auto_error=True,
    secret_key=settings.sessions.SESSIONS_SECRET_KEY,
    cookie_params=cookie_params,
)


# SESSION BACKEND ################################

backend = InDBBackend[UUID, SessionData]()


# SESSION VERIFIER ################################

class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InDBBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)
