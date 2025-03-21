from tools.classes import CustomSettings


class Celery(CustomSettings):
    CELERY_BROKER: str
    CELERY_RESULT: str
    CELERY_BROKER_HOST: str
    CELERY_RESULT_EXPIRES_DAYS: int

    @property
    def CELERY_BROKER_URL(self):
        return f"{self.CELERY_BROKER}://{self.CELERY_BROKER_HOST}:6379/0"

    @property
    def CELERY_BROKER_BACKEND(self):
        return f"{self.CELERY_BROKER}://{self.CELERY_BROKER_HOST}:6379/0"


class Settings(CustomSettings):
    celery: Celery = Celery()


settings = Settings()