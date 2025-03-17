from logging import Logger, getLogger

from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app1.core.settings import settings
from app1.scripts.scrypt_schemas.email import CustomMessageSchema

logger = getLogger(__name__)

def get_smtp_connection_config():
    return ConnectionConfig(
        MAIL_USERNAME=settings.email.MAIL_USERNAME,
        MAIL_PASSWORD=settings.email.MAIL_PASSWORD,
        MAIL_FROM=settings.email.MAIL_FROM,
        MAIL_PORT=settings.email.MAIL_PORT,
        MAIL_SERVER=settings.email.MAIL_HOST,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
    )


def get_message_params(schema: CustomMessageSchema):
    return MessageSchema(**schema.model_dump(), subtype='html')


async def send_mail(
        schema: CustomMessageSchema,
        background_tasks: BackgroundTasks = None,
        logger: Logger = logger
) -> bool:

    message = get_message_params(schema)
    fm = FastMail(get_smtp_connection_config())

    if background_tasks:
        try:
            background_tasks.add_task(fm.send_message, message, )
            logger.info("Starting mailsender as background task")
            return True
        except Exception as exc:
            logger.error(f"Mailsender as background task error: {exc}")
            return False
    else:
        try:
            await fm.send_message(message=message)
            logger.info("Starting mailsender as async task")
            return True
        except Exception as exc:
            logger.error(f"Mailsender as async task error: {exc}")
            return False

    # ClientConnectorDNSError
