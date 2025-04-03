import datetime
import jwt

from app1.core.settings import settings


def jwt_encode(
        payload: dict,
        secret_key: str = settings.sessions.SESSIONS_SECRET_KEY,
        algorithm: str = settings.sessions.SESSIONS_ALGORYTHM
):

    now = datetime.datetime.now(datetime.UTC)
    return jwt.encode(
        payload={
            'iat': now,
            **payload,
        },
        key=secret_key,
        algorithm=algorithm,
    )


def jwt_decode(
        token_cred: str | bytes,
        secret_key: str = settings.sessions.SESSIONS_SECRET_KEY,
        algorithm: str = settings.sessions.SESSIONS_ALGORYTHM
) -> dict:
    result: dict = jwt.decode(
        jwt=token_cred,
        key=secret_key,
        algorithms=[algorithm,],
    )
    return result
