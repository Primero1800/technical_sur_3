from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
)

from app1.api.dependencies import strategy
from app1.core.settings import settings

bearer_transport = BearerTransport(
    tokenUrl=settings.auth.TRANSPORT_TOKEN_URL
)


authentication_backend = AuthenticationBackend(
    name="access-token-db",
    transport=bearer_transport,
    get_strategy=strategy.get_database_strategy,
)
