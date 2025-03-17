from typing import List

from pydantic import BaseModel


class MailBody(BaseModel):
    to: List[str] = ['admin@primero1800.store']
    subject: str = 'Test Message'
    body: str = "Hello! You are reading test message"
