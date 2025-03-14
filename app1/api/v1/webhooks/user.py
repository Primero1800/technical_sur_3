from fastapi import APIRouter

from app1.api.v1.users.schemas import UserRegisteredWebhookNotification

router = APIRouter()


@router.post("/user-registered")
def webhook_user_registered_notification(info: UserRegisteredWebhookNotification):
    """
    This webhook will be triggered, when the user is created.
    """
