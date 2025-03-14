import logging
from datetime import datetime

import aiohttp

from typing import TYPE_CHECKING

from app1.api.v1.users.schemas import UserRead, UserRegisteredWebhookNotification
from app1.core.settings import settings

if TYPE_CHECKING:
    from app1.core.models import User

WEBHOOK_URL = settings.webhooks.WEBHOOK_URL
log = logging.getLogger(__name__)


async def hook_send_new_user_notification(user: "User") -> None:

    webhook_data: dict = UserRegisteredWebhookNotification(
        user=UserRead.model_validate(user),
        time=str(datetime.now())
    ).model_dump()

    log.info("Notify user created with data %s", webhook_data)
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=WEBHOOK_URL,
                json=webhook_data
        ) as response:
            response_data = await response.json(content_type="application/json")
            log.info("Sent webhook, got response %s", response_data)
