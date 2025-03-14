from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app1.core.models import User


async def hook_send_new_user_notification(user: "User") -> None:
    pass
