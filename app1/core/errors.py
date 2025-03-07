from sqlalchemy.exc import IntegrityError


class Missing(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class Duplicate(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class Validation(Exception):
    def __init__(self, msg: str):
        self.msg = msg


def get_message(instance):
    msg = str(instance.orig)
    return msg.split('DETAIL:')[-1].strip() if 'DETAIL' in msg else str(instance)

