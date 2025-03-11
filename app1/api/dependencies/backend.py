from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
)

from app1.api.dependencies import strategy


bearer_transport = BearerTransport(
    # TODO update url
    tokenUrl="auth/jwt/login"
)


authentication_backend = AuthenticationBackend(
    name="access-token-db",
    transport=bearer_transport,
    get_strategy=strategy.get_database_strategy,
)
