from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP

from starlette import status

from app1.core.settings import settings
from app1.scripts.scrypt_schemas.email import MailBody


def send_mail(data: dict | None = None):
    msg = MailBody(**data)
    message = MIMEText(msg.body, "html")
    message["From"] = settings.email.MAIL_USERNAME
    message["To"] = ', '.join(msg.to)
    message["Subject"] = msg.subject

    ctx = create_default_context()

    try:
        with SMTP(host=settings.email.MAIL_HOST, port=settings.email.MAIL_PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(user=settings.email.MAIL_USERNAME, password=settings.email.MAIL_PASSWORD)
            server.send_message(message)
            server.quit()
        return {
            "status": status.HTTP_200_OK,
            "detail":  "Message was sent successfully"
        }
    except Exception as exc:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": exc
        }
